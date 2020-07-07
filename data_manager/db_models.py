"""
Build sqlalchemy ORM models using sqlacodegen to a specified directory.
Methods to create SQL Alchemy connection strings and build db models
"""
# pylint: disable=too-many-locals, too-many-arguments
import os
from typing import Any, List, Dict, Tuple

import pandas as pd

HEADER_MESSAGE = '\n\"\"\"\n' \
                 'Database engine connections that the application ' \
                 'would connect to.' \
                 'AUTO-GENERATED, please run: \n\n' \
                 'from data_manager import db_models \n ' \
                 'get_db_engines(<options>) \n' \
                 'to generate connection strings and orm objects'
PYLINT_MSG = '\n # pylint: skip-file \n'
IMPORT_STRINGS = 'import os \n from sqlalchemy import create_engine'
CONNECTION_STRING = 'postgres://{user}:{password}@{host}:5432/{database}'


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
    pass
