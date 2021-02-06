from sqlite3x import Sqlite3x
from mysqlx import MySQLx
"""
Run these tests to verify your adapter works. The output with empty tables should be:

[(1, 'addr1', 'user1'), (2, 'addr2', 'user2')]
[(1, 'room1'), (2, 'room2')]
[(1, 'user1', 'room1'), (2, 'user2', 'room1'), (3, 'user1', 'room2'), (4, 'user2', 'room2')]
[(1, 'user1', 'room1'), (3, 'user1', 'room2')]
[(3, 'user1', 'room2')]
[(1, 'user1', 'room1'), (2, 'user2', 'room1'), (3, 'user1', 'room2')]
[(2, 'user2', 'room1'), (3, 'user1', 'room2')]

"""
users = [
    ['addr1', 'user1'],
    ['addr2', 'user2'],
]
rooms = [
    ['room1'],
    ['room2'],
]
rooms_users = [
    ['user1', 'room1'],
    ['user2', 'room1'],
    ['user1', 'room2'],
    ['user2', 'room2'],
]

# db = Sqlite3x()
db = MySQLx()

# seed the database and test 'insert' and 'select *'
db.insert('users', users)
print(list(db.select('users')))

db.insert('rooms', rooms)
print(list(db.select('rooms')))

db.insert('rooms_users', rooms_users)
print(list(db.select('rooms_users')))

# test select with one and multiple conditions
print(list(db.select('rooms_users', {'username': 'user1'})))
print(
    list(db.select('rooms_users', {'username': 'user1', 'room': 'room2'})))

# test delete with multiple conditions
db.delete('rooms_users', {'username': 'user2', 'room': 'room2'})
print(list(db.select('rooms_users')))

# test delete with orderby + limit
db.delete('rooms_users', {'username': 'user1'}, 'id', 1)
print(list(db.select('rooms_users')))
