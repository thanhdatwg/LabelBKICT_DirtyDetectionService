import psycopg2


class SQLService:
    def __init__(self, info_connect) -> None:
        self.info_connect = info_connect
        self.sql_connection = psycopg2.connect(**self.info_connect)
        self.cursor = self.sql_connection.cursor()

    def get(self, table_name):
        pass

    def insert(self, table_name, values):
        pass

    def update(self, query):
        self.cursor.execute(query)
        self.sql_connection.commit()
