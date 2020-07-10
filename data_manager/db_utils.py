"""
Database utils
"""
from datetime import datetime

import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from .exceptions import DatabaseError


def read_sql(sql_text: str, engine: Engine, chunksize: int = 100000, **parameters):
    """
    read SQL query from a given database engine
    :param sql_text: sql text
    :param engine: sqlalchemy engine
    :param chunksize: (optional) the chunk of rows that would be fetched
        per round in query
    :param parameters: (optional) parameters as key-value pairs
        (usage: date = test_date)
    :return: pandas Dataframe with the results or throws Database error
    """
    conn = engine.raw_connection()
    try:
        cursor_ = conn.cursor()
        cursor_.arraysize = chunksize
        result = cursor_.execute(sql_text, **parameters).fetchall()
        result = pd.DataFrame(result)
        if result.shape[0] > 0:
            result.columns = [row[0] for row in cursor_.description]
        cursor_.close()
    except DatabaseError:
        raise DatabaseError()
    finally:
        conn.close()
    return result


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
    start = datetime.now()
    # ToDo:  This would be written
    diff = datetime.now() - start
    print('commited data in {time} hours').format(time=str(diff))


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
        session.execute(sql_text, **parameters)
        session.commit()
        flag = True
    except DatabaseError:
        session.rollback()
        print('SQL Error')
    finally:
        session.close()
    return flag
