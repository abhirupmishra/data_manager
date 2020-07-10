"""
common exceptions for the data manager
"""
import psycopg2


class DatabaseError(psycopg2.DatabaseError):
    """
    wrapper around Database Error
    """
    def __init__(self):
        """
        constructor for the class
        """
        message = 'database error'
        super(DatabaseError, self).__init__(message)
