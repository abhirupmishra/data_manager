"""
Database utils
"""
from sqlalchemy.engine.base import Engine
import pandas as pd


def read_sql(sql_text: str, engine: Engine, **parameters):
    """
    read SQL query
    :param sql_text: sql text
    :param engine: sqlalchemy engine
    :param parameters:
    :return:
    """
    pass


def to_sql(data: pd.DataFrame, engine: Engine, table_name: str):
    """
    commit dataframe to a table
    :param data:
    :param engine:
    :param table_name:
    :return:
    """
    pass


def run_sql(sql_text: str, engine: Engine, **parameters):
    """
    run a sql which doesn't return a value
    :param sql_text:
    :param engine:
    :param parameters:
    :return:
    """
    pass