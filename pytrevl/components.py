import matplotlib.pyplot as plt
import sqlalchemy
import pandas
import os

drivername=os.getenv("drivername")
username=os.getenv("username")
password=os.getenv("password")
host=os.getenv("host")
port=os.getenv("port")
database=os.getenv("database")

class PieChart:
    def __init__(self, id: str, cube: str, x: list, y: list, filters: dict = {}):
        self.id = id
        self.cube = cube
        self.x = x
        self.y = y
        self.name = x
        self.filters = filters
    
    def show(self) -> None:
        data = self.get_data()
        fig1, ax1 = plt.subplots()
        ax1.pie(data[self.y], labels = data[self.x])
        ax1.set_title(self.id)
        ax1.axis('equal')
        plt.show()

    def get_data(self) -> dict:
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
        connection = engine.connect()
        filters_list = []
        for filter in self.filters.items():
            filters_list.append(filter[0] + " = '" + filter[1] + "'")
        filters_sql = " AND ".join(filters_list)
        query = f"SELECT {self.x}, {self.y} FROM {self.cube} WHERE {filters_sql};"
        df = pandas.read_sql_query(query, connection)
        return df