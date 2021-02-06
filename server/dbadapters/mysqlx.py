import pymysql
from .db import Db


class MySQLx(Db):
    """
    Class to connect to sqlite
    For the sake of example we use in-memory table. This can be easily changed
    x in the name is just to avoid confusion

    All tables have 'id INTEGER PRIMARY KEY AUTOINCREMENT,'.
    ON inserts the passed values should not include value for this field, it
    will be handled automatically
    """

    def __init__(self) -> None:
        super().__init__()
        conn = pymysql.connect(
            host='localhost',
            user='via',
            password='V1a|Chat',
            database='via',
            autocommit=True)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `addr` varchar(32) NOT NULL,
                `username` varchar(32) NOT NULL UNIQUE
            );
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `name` varchar(32) NOT NULL,
                UNIQUE KEY (`name`)
            );
        ''')
        # We don't have select with JOIN that's why we will not use the ids
        cur.execute('''
            CREATE TABLE IF NOT EXISTS rooms_users (
            id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            username varchar(32),
            room varchar(32),
            UNIQUE KEY (username, room),
            FOREIGN KEY (username)
                REFERENCES users (username)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION,
            FOREIGN KEY (room)
                REFERENCES rooms (name)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
            );
        ''')
        self.conn = conn
        self.cur = cur

    def select(self, table: str, conditions: dict = {}):
        """
        Get data from the table
        Only '=' as operator is supported
        """

        if conditions:
            where = ' AND '.join([f'{k} = %({k})s' for k in conditions])
            # TODO(Stoycho) - fix this
            self.cur.execute(
                f'SELECT * FROM {table} WHERE {where}', conditions)
        else:
            self.cur.execute(f'SELECT * FROM {table}')

        return self.cur.fetchall()

    def insert(self, table: str, items: list) -> bool:
        """
        Inserts records in the table. No special checks are applied.
        Items are supposed to have values for all columns in the table.
        """
        # add NULL in the values so the autoincrement to work
        for item in items:
            item.insert(0, None)
        # generate '?, ?' for VALUES (? , ?, ?)
        # in order to avoid SQL injection
        values = ','.join(['%s'] * len(items[0]))
        self.cur.executemany(f'INSERT INTO {table} VALUES ({values})', items)

    def delete(self, table: str, conditions: dict, orderby: str = '', limit: int = 0) -> bool:
        """
        Delete table by certain condtitions
        Orderby and limit should both be specified. If either is not specified both are ignored
        """
        where = ' AND '.join([f'{k} = %({k})s' for k in conditions])

        order_limit = ''
        if orderby and limit:
            order_limit = f' ORDER BY {orderby} LIMIT {limit}'

        self.cur.execute(
            f'DELETE FROM {table} WHERE {where} {order_limit}', conditions)
