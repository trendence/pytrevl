import plotly.express as px
import sqlalchemy
import pandas as pd
import os

# Get global env variables for SQL - connection
drivername=os.getenv("DRIVERNAME")
username=os.getenv("USERNAME")
password=os.getenv("PASSWORD")
host=os.getenv("HOST")
port=os.getenv("PORT")
database=os.getenv("DATABASE")

class Plot:
    '''
    Plot parent class 
    '''
    def __init__(self):
        pass

    # Connecting to Cube.js
    def get_data(self) -> pd.DataFrame:

        engine = sqlalchemy.create_engine(
                    sqlalchemy.engine.url.URL(
                        drivername=drivername,
                        username=username,
                        password=password,
                        host=host,
                        port=port,
                        database=database,
                    ),
                    echo_pool=True,
        )

        print("Connecting with Cube.js...")

        connection = engine.connect() # Connecting to engine

        # Converting Plot filters to SQL format
        filters_list = []
        for filter in self.filters.items():
            filters_list.append(filter[0] + " = '" + filter[1] + "'")
        filters_sql = " AND ".join(filters_list)

        query = f"SELECT {self.x}, {self.y} FROM {self.cube} WHERE {filters_sql};"

        df = pd.read_sql_query(query, connection) # Applies SQL query and returns a DataFrame

        return df

class PieChart(Plot):

    def __init__(self, id: str, cube: str, title: str, x: list, y: list, filters: dict = {}):
        self.id = id
        self.title = title
        self.cube = cube
        self.x = x
        self.y = y
        self.name = x
        self.filters = filters
        self.type = "pie"
    
    def show(self) -> None:
        data = self.get_data()
        fig = px.pie(data, values=self.y, names=self.x, title=self.title)
        fig.show()

    

class BarChart(Plot):

    def __init__(self, id: str, cube: str, title: str, x: list, y: list, filters: dict = {}, orientation: str = "h"):
        self.id = id
        self.title = title
        self.cube = cube
        self.x = x
        self.y = y
        self.name = x
        self.filters = filters
        self.orientation = orientation
        self.type = "column"
    
    def show(self) -> None:
        data = self.get_data()
        fig = px.bar(data, x=self.x, y=self.y, title=self.title, orientation=self.orientation)
        fig.show()