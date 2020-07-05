"""
methods to create SQL Alchemy connection strings and build db models
"""
from typing import Any


def build_orm_models(connection_string: str, output_path: str):
    """
    Method to build ORM classes for a given connection string at a given path
    :param connection_string:
    :param output_path:
    :return:
    """
    pass


def __build_connection_string(host: str, user: str, password: str, decryption_method: Any, do_decrypt: bool = False):
    """
    private method for which returns connection string either in decrypted form
    or with decrypted method
    :param host:
    :param user:
    :param password:
    :param decryption_method:
    :param do_decrypt:
    :return:
    """
    pass


def build_engine(output_path: str):
    """
    method which would create engine string at a given location
    :param output_path:
    :return:
    """
    pass


def get_db_engines(orm_flag: bool = True):
    """
    Method to build DB Models and schemas
    :param orm_flag:
    :return:
    """
    pass


if __name__ == '__main__':
    