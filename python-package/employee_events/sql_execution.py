from functools import wraps
from pathlib import Path
from sqlite3 import connect

import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path(__file__).resolve().parent / "employee_events.db"


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:

    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, sql_query):
        """Execute a query and return its result as a pandas DataFrame."""
        with connect(db_path) as connection:
            return pd.read_sql_query(sql_query, connection)

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, sql_query):
        """Execute a query and return all rows as a list of tuples."""
        with connect(db_path) as connection:
            cursor = connection.cursor()
            return cursor.execute(sql_query).fetchall()


# Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        with connect(db_path) as connection:
            cursor = connection.cursor()
            return cursor.execute(query_string).fetchall()

    return run_query
