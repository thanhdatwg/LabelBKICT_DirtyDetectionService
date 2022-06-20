import psycopg2


class Database:
    def __init__(self, info_connect) -> None:
        self.info_connect = info_connect
        self.sql_connection = psycopg2.connect(**self.info_connect)
        self.cursor = self.sql_connection.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        self.sql_connection.commit()
