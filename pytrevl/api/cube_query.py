'''
Handling Cube connections
'''
import os
import sqlalchemy
import pandas as pd
from typing import List
from pytrevl import Cube, Filter

# Get global env variables for SQL - connection

SQL_CUBE_OPERATORS = {
    "equals": " = ",
    ">=": " >= ",
    "<=": " <= "
"""
Add more in the future
"""
}


class CubeQuery:
    '''
    Cube api
    '''
    def __init__(self, queries: List, cube: Cube, filters: List = None):
        self.queries = queries
        self.cube = cube
        self.filters = filters
        self.drivername=os.getenv("DRIVERNAME")
        self.username=os.getenv("USERNAME")
        self.password=os.getenv("PASSWORD")
        self.host=os.getenv("HOST")
        self.port=os.getenv("PORT")
        self.database=os.getenv("DATABASE")

    def get_data(self) -> pd.DataFrame:
        connection = self._connect()

        query_sql = ", ".join(self.queries)

        if self.filters:
            filters_list = []
            for filter in self.filters:
                filters_list.append(filter.variable + SQL_CUBE_OPERATORS.get(filter.operator) + "'" + filter.value + "'")
            filters_sql = " AND ".join(filters_list)

            # Building Cube query
            query = f"SELECT {query_sql} FROM {self.cube.name} WHERE {filters_sql};"
        else:
            query = f"SELECT {query_sql} FROM {self.cube.name};"

        # Receiving Data
        df = pd.read_sql_query(query, connection) # Applies SQL query and returns a DataFrame

        return df

    def _connect(self) -> None:
        # Creating engine
        engine = sqlalchemy.create_engine(
                    sqlalchemy.engine.url.URL(
                        drivername=self.drivername,
                        username=self.username,
                        password=self.password,
                        host=self.host,
                        port=self.port,
                        database=self.database,
                    ),
                    echo_pool=True,
        )

        print("Connecting with Cube...")

        # Connecting to engine
        connection = engine.connect()
        return connection
