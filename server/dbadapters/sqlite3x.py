import sqlite3
from .db import Db


class Sqlite3x(Db):
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
        conn = sqlite3.connect("file::memory:")
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
        cur.executescript('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                addr TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE
            );

            CREATE TABLE rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_by TEXT NOT NULL,
                UNIQUE (name),
                FOREIGN KEY (created_by)
                    REFERENCES users (username)
                        ON DELETE CASCADE
                        ON UPDATE NO ACTION
            );

            /*
            We don't have select with JOIN that's why we will not use the ids
            */
            CREATE TABLE rooms_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT,
            username TEXT,
            UNIQUE (username, room),
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
            where = ' AND '.join([f'{k} = :{k}' for k in conditions])
            # TODO(Stoycho) - fix this
            for row in self.cur.execute(f'SELECT * FROM {table} WHERE {where}', conditions):
                yield row
        else:
            for row in self.cur.execute(f'SELECT * FROM {table}'):
                yield row

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
        values = ','.join(['?'] * len(items[0]))
        self.cur.executemany(f'INSERT INTO {table} VALUES ({values})', items)

    def delete(self, table: str, conditions: dict, orderby: str = '', limit: int = 0) -> bool:
        """
        Delete table by certain condtitions
        Orderby and limit should both be specified. If either is not specified both are ignored
        """
        where = ' AND '.join([f'{k} = :{k}' for k in conditions])

        order_limit = ''
        if orderby and limit:
            order_limit = f' ORDER BY {orderby} LIMIT {limit}'

        self.cur.execute(
            f'DELETE FROM {table} WHERE {where} {order_limit}', conditions)
