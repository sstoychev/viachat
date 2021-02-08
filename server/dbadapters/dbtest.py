from configparser import ConfigParser
from sqlite3x import Sqlite3x
from mysqlx import MySQLx
"""
Run these tests to verify your adapter works. The output with empty tables should be:

seed users
[(1, 'addr1', 'user1'), (2, 'addr2', 'user2')]

seed rooms
[(1, 'room1', 'user1'), (2, 'room2', 'user2')]

seed rooms_users
[(1, 'room1', 'user1'), (3, 'room2', 'user1'), (2, 'room1', 'user2'), (4, 'room2', 'user2')]

test SELECT .. WHERE
[(1, 'room1', 'user1'), (3, 'room2', 'user1')]
[(3, 'room2', 'user1')]

test SELECT COUNT
[(4,)]

test SELECT .. WHERE
[(2,)]
[(1,)]

test DELETE ... WHERE
[(1, 'room1', 'user1'), (3, 'room2', 'user1'), (2, 'room1', 'user2')]

test DELETE ... WHERE .. ORDER BY x LIMIT y
[(3, 'room2', 'user1'), (2, 'room1', 'user2')]
"""
users = [
    ['addr1', 'user1'],
    ['addr2', 'user2'],
]
rooms = [
    ['room1', 'user1'],
    ['room2', 'user2'],
]
rooms_users = [
    ['room1', 'user1'],
    ['room1', 'user2'],
    ['room2', 'user1'],
    ['room2', 'user2'],
]

CONFIG_FILE = '../../config.ini'

config = ConfigParser()
config.read(CONFIG_FILE)


db = Sqlite3x(config)
# db = MySQLx(config)

# seed the database and test 'insert' and 'select *'
print('\nseed users')
db.insert('users', users)
print(list(db.select('users')))

print('\nseed rooms')
db.insert('rooms', rooms)
print(list(db.select('rooms')))

print('\nseed rooms_users')
db.insert('rooms_users', rooms_users)
print(list(db.select('rooms_users')))

# test select with one and multiple conditions
print('\ntest SELECT .. WHERE')
print(list(db.select('rooms_users', {'username': 'user1'})))
print(list(db.select('rooms_users', {'username': 'user1', 'room': 'room2'})))

# test select COUNT
print('\ntest SELECT COUNT')
print(list(db.select('rooms_users', {}, True)))

# test select COUNT with one and multiple conditions
print('\ntest SELECT .. WHERE')
print(list(db.select('rooms_users', {'username': 'user1'}, True)))
print(list(db.select('rooms_users', {'username': 'user1', 'room': 'room2'}, True)))

# test delete with multiple conditions
print('\ntest DELETE ... WHERE')
db.delete('rooms_users', {'username': 'user2', 'room': 'room2'})
print(list(db.select('rooms_users')))

# test delete with orderby + limit
print('\ntest DELETE ... WHERE .. ORDER BY x LIMIT y')
db.delete('rooms_users', {'username': 'user1'}, 'id', 1)
print(list(db.select('rooms_users')))
