"""
Database utils
"""
from datetime import datetime
from typing import List, Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from .exceptions import DatabaseError

INSERT_STATEMENT = "INSERT INTO {schema_table} ({columns}) values({table_values})"


def read_sql(sql_text: str, engine: Engine, **parameters):
    """
    read SQL query from a given database engine
    :param sql_text: sql text
    :param engine: sqlalchemy engine
    :param parameters: (optional) parameters as key-value pairs
        (usage: date = test_date)
    :return: pandas Dataframe with the results or throws Database error
    """
    conn = engine.connect()
    try:
        sql_text_params = text(sql_text)
        result = conn.execute(sql_text_params, **parameters)
        columns = [col for col in result.keys()]
        out_ = pd.DataFrame(result.fetchall(), columns=columns)
        result.close()
    except DatabaseError:
        raise DatabaseError()
    finally:
        conn.close()
    return out_


def to_sql(data: pd.DataFrame, engine: Engine, table_name: str,
           schema_name: str = None, chunksize: int = 100000):
    """
    commit pandas dataframe to a table by appending the data
    :param data: pandas dataframe with data.
        The columns of the table should be same name as table columns
    :param engine: sqlalchemy engine
    :param table_name: tale name in the database
    :param chunksize: chunks commiting data to the table
    :param schema_name: schema name in which the table is location
        (default is None)
    """
    def _chunks(input_list: List[Any] or pd.DataFrame, chunk: int):
        """
        yield successive chunks from 1
        :param input_list:
        :param chunk:
        :return:
        """
        for iter_ in range(0, len(input_list), chunk):
            yield input_list[iter_: iter_ + chunk]

    start = datetime.now()
    table_ = __get_db_object(
        object_name=table_name, schema_name=schema_name,
        engine=engine
    )
    conn_ = engine.raw_connection()
    try:
        cursor_ = conn_.cursor()

        write_statement = INSERT_STATEMENT.format(
            schema_table=table_,
            columns=', '.join(data.columns.tolist()),
            table_values=', '.join([':' + s for s in data.columns.tolist()])
        )
        for _, rows_chunk in enumerate(_chunks(data, chunksize)):
            cursor_.executemany(write_statement, rows_chunk.values.tolist())
        conn_.commit()
    except DatabaseError:
        raise DatabaseError()
    finally:
        conn_.close()

    diff = datetime.now() - start
    print('commited data in {time} hours'.format(time=str(diff)))


def run_sql(sql_text: str, engine: Engine, **parameters) -> bool:
    """
    run a sql which doesn't return a value
    :param sql_text: input sql test
    :param engine: sqlalchemy engine object
    :param parameters: (optional) parameters as key-value pairs
        (usage: date = test_date)
    :return: True/False
    """
    session = Session(engine)
    flag = False
    try:
        sql_text_params = text(sql_text)
        session.execute(sql_text_params, **parameters)
        session.commit()
        flag = True
    except DatabaseError:
        session.rollback()
        print('SQL Error')
    finally:
        session.close()
    return flag


def __get_db_object(object_name: str, engine: Engine, schema_name: str = None,
                    is_table: bool = False):
    """
    postgres queries to check for schema name or table name
    :param object_name: objectname (stored procedure, table)
    :param engine: sqlalchemy engine
    :param schema_name: schema_name (if table is object)
    :param is_table: whether the object is table
    :return: str of full object_name (SCHEMA_NAME.OBJECT_NAME)
    """
    if object_name is None:
        raise Exception('Objectname cannot be null')

    # check if schema is valid
    if schema_name is not None:
        query = "SELECT schema_name FROM information_schema.schemata " \
                "where schema_name= :schema_name"
        db_schema = read_sql(sql_text=query, engine=engine, schema_name=schema_name.lower())

        if db_schema.shape[0] == 0:
            raise Exception('Schema name: {schema} not found'.format(schema=object_name))

    # check if table is valid
    if schema_name is not None:
        if is_table:
            sql_text = """
                select
                    table_schema || '.' || table_name as table_name
                from information_schema.tables
                where 
                    table_type = 'BASE TABLE' and table_schema = :schema_name and 
                    table_name = :table_name and table_schema NOT IN (
                        'pg_catalog', 'information_schema'
                    )
            """
        else:
            sql_text = """
                SELECT  proowner || '.' || proname as table_name
                FROM    pg_catalog.pg_namespace n JOIN pg_catalog.pg_proc p
                    ON pronamespace = n.oid
                WHERE 
                    nspname = 'public' and proowner = :schema_name and
                    proname = :table_name
            """
        db_table = read_sql(sql_text=sql_text, engine=engine,
                            schema_name=schema_name.lower(), table_name=object_name.lower())
    else:
        if is_table:
            sql_text = """
                select
                    table_schema || '.' || table_name as table_name
                from information_schema.tables
                where 
                    table_type = 'BASE TABLE' and  table_name = :table_name and 
                    table_schema NOT IN (
                        'pg_catalog', 'information_schema'
                    )
            """
        else:
            sql_text = """
                SELECT  proowner || '.' || proname as table_name
                FROM    pg_catalog.pg_namespace n JOIN pg_catalog.pg_proc p
                    ON pronamespace = n.oid
                WHERE 
                    nspname = 'public' and proname = :table_name
            """
        db_table = read_sql(sql_text=sql_text, engine=engine, table_name=object_name.lower())

    if db_table.shape[0] == 0:
        raise Exception('specified object not found: {object_}'.format(object_=object_name))

    table_ = db_table.iloc[0, 0]
    return table_
