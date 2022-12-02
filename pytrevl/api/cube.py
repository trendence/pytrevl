'''
Handling Cube connections
'''
import os
import sqlalchemy
import pandas as pd

# Get global env variables for SQL - connection


class Cube:
    '''
    Cube api
    '''
    def __init__(self, x: str, y: str, cube: str, filters: dict):
        self.x = x
        self.y = y
        self.cube = cube
        self.filters = filters
        self.drivername=os.getenv("DRIVERNAME")
        self.username=os.getenv("USERNAME")
        self.password=os.getenv("PASSWORD")
        self.host=os.getenv("HOST")
        self.port=os.getenv("PORT")
        self.database=os.getenv("DATABASE")

    def connect(self) -> None:
        # Creating engine
        self.engine = sqlalchemy.create_engine(
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
        self.connection = self.engine.connect()

    def get_data(self) -> pd.DataFrame:
        # Converting Plot filters to SQL format
        self.filters_list = []
        for self.filter in self.filters.items():
            self.filters_list.append(self.filter[0] + " = '" + self.filter[1] + "'")
        self.filters_sql = " AND ".join(self.filters_list)

        # Building Cube query
        self.query = f"SELECT {self.x}, {self.y} FROM {self.cube} WHERE {self.filters_sql};"

        # Receiving Data
        df = pd.read_sql_query(self.query, self.connection) # Applies SQL query and returns a DataFrame

        return df