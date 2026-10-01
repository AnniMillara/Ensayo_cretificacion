import pymysql.cursors


class MySQLConnection:
    """
    Administra la conexión entre Python y MySQL.
    """

    def __init__(self, db):
        self.db = db

    def query_db(self, query, data=None):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database=self.db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

        with connection.cursor() as cursor:
            try:
                query_debug = cursor.mogrify(query, data)
                print("Running Query:", query_debug)

                cursor.execute(query, data)

                q = query.strip().lower()

                if q.startswith("select"):
                    return cursor.fetchall()

                if q.startswith("insert"):
                    return cursor.lastrowid

                return cursor.rowcount

            except Exception as e:
                print("Ups, algo ha salido mal :(", e)
                return False

            finally:
                connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)