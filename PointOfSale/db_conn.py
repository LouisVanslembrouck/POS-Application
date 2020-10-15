import pyodbc

class LocalDB:

    """ Set up MSSQL Database Connection. """

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                    'Server=DESKTOP-MDG6IE7;'
                                    'Database=PointOfSale;'
                                    'Trusted_Connection=yes;')

        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class CentralDB:

    """ Set up MSSQL Database Connection. """

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                    'Server=DESKTOP-MDG6IE7;'
                                    'Database=Central_Database;'
                                    'Trusted_Connection=yes;')

        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()