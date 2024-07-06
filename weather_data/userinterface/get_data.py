import mysql.connector


class Database:
    host = "127.0.0.1"
    port = "3306"
    user = username
    password = pwd

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database="weatherdata"
        )

    def execute_sql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result


def temperature():
    db = Database()
    query = "SELECT * FROM temperatures"
    result = db.execute_sql(query)
    return result


def precipitation():
    db = Database()
    query = "SELECT * FROM precipitation"
    result = db.execute_sql(query)
    return result
