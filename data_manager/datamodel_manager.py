"""
DataManager class to handle raw sql as well as have data objects
"""
from typing import Any, Tuple
from sqlalchemy.orm.session import Session


class DataModelManager:

    def __init__(self, data_models: Tuple[str, Any or Session.query] = None):
        """
        constructor
        :param data_models: optional data-models or queries
        to be run during initialization
        """
        pass

    def __initialize(self):
        """
        initialize
        :return:
        """
        pass
