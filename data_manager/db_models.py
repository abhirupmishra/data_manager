"""
Build sqlalchemy ORM models using sqlacodegen to a specified directory.
Methods to create SQL Alchemy connection strings and build db models
"""
# pylint: disable=too-many-locals, too-many-arguments
import os
from dataclasses import dataclass
from typing import Any, List


HEADER_MESSAGE = '\n\"\"\"\n' \
                 'Database engine connections that the application ' \
                 'would connect to. \n' \
                 'AUTO-GENERATED, please run: \n\n' \
                 'from data_manager import db_models \n ' \
                 'get_db_engines(<options>) \n' \
                 'to generate connection strings and orm objects'
PYLINT_MSG = '\n # pylint: skip-file \n'
IMPORT_STRINGS = 'import os \n from sqlalchemy import create_engine'
CONNECTION_STRING = 'postgres://{user}:{password}@{host}:5432/{database}'
CONNECTION_STRING_VARS = "create_engine(postgres://' + os.environ['{user}'] + ':' +  os.environ['{password}'] + \
                         '@' + os.environ['{host}'] + ' + :5432/' + os.environ['{database}'])"
ENGINE_STRING = '{engine_name} = {connection_string}\n\n'


@dataclass
class DBModelItem:
    """
    class for keeping inputs to database models creation
    """
    db_host: str
    db_user: Any
    db_password: Any
    db_database: str
    db_schemas: List[str] = None


def __build_orm_models(db_model_item: DBModelItem, output_path: str, engine_string: str):
    """
    Method to build ORM classes for a given connection string at a given path
    :param db_model_item: DB Model item details
    :param output_path: output path
    :param engine_string: sqlalchemy engine string
    :return:
    """
    command = None
    if db_model_item.db_schemas is None:
        orm_name = db_model_item.db_database.lower() + '_models.py'
        orm_classes_path = output_path + orm_name
        command = 'sqlacodegen --outfile ' + orm_classes_path + \
                  '--nojoined --noindexes --noviews --noconstraints ' \
                  ' ' + engine_string
    else:
        for schema in db_model_item.db_schemas:
            orm_name = db_model_item.db_database.lower() + '_' + schema.lower() + '_models.py'
            orm_classes_path = output_path + orm_name
            command = 'sqlacodegen --outfile ' + orm_classes_path + \
                      '--nojoined --noindexes --noviews --noconstraints ' \
                      '--schema' + schema + ' ' + engine_string

    os.system(command)


def __build_connection_string(host: str, user: str, password: str, database: str,
                              use_environment_vars: bool = True) -> str:
    """
    private method which returns connection string
    :param host: name of host variable in os.environment or host
    :param user: name of user variable in os.environment or user
    :param password: name of password variable in os.environment or password
    :param database: name of password variable in os.environment or database name
    :param use_environment_vars: boolean variable
    :return:
    """
    connection_string = CONNECTION_STRING
    if use_environment_vars:
        connection_string = CONNECTION_STRING_VARS

    result_string = connection_string.format(
        user=user, password=password, host=host,
        database=database
    )
    return result_string


def __build_engine_file(output_path: str, db_model_items: List[DBModelItem]):
    """
    method which would create engine file __init__.py at a given location
    :param output_path:
    :return:
    """
    engine_strings = list()
    for db_model_item in db_model_items:
        connection_string = __build_connection_string(
            host=db_model_item.db_host, user=db_model_item.db_user,
            password=db_model_item.db_password, database=db_model_item.db_database
        )
        engine_variable = db_model_item.db_database + '_engine'
        engine_string = ENGINE_STRING.format(engine_name=engine_variable,
                                             connection_string=connection_string)
        engine_strings.append(engine_string)

    # writing to __init__.py file
    with open(output_path + '__init__.py', 'w') as file_:
        file_.write(HEADER_MESSAGE)
        file_.write(PYLINT_MSG)
        file_.write(IMPORT_STRINGS)

        for eng_ in engine_strings:
            file_.write(eng_)


def generate_db_details(db_model_items: List[DBModelItem], export_path: str,
                        orm_flag: bool = True, orm_classes_path: str = None):
    """
    Method to build DB Models and schemas
    :param export_path: path where the db engine string would be generated
    :param db_model_items: database and schema details
        for which the models need to be built
    :param orm_flag: flag on whether to build orm classes or not
    :param orm_classes_path: path to store ORM classes
    """
    __build_engine_file(output_path=export_path, db_model_items=db_model_items)

    if orm_flag:
        for db_model_item in db_model_items:
            host = os.environ[db_model_item.db_host]
            user = os.environ[db_model_item.db_user]
            password = os.environ[db_model_item.db_password]
            database = os.environ[db_model_item.db_database]

            engine_string = __build_connection_string(
                host=host, user=user, password=password,
                database=database, use_environment_vars=False
            )
            __build_orm_models(db_model_item=db_model_item, output_path=orm_classes_path,
                               engine_string=engine_string)
