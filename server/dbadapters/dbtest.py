from sqlite3x import Sqlite3x
from mysqlx import MySQLx
"""
Run these tests to verify your adapter works. The output with empty tables should be:

seed users
[(1, 'addr1', 'user1'), (2, 'addr2', 'user2')]

seed rooms
[(1, 'room1', 'user1'), (2, 'room2', 'user2')]

seed rooms_users
[(1, 'room1', 'user1'), (2, 'room1', 'user2'), (3, 'room2', 'user1'), (4, 'room2', 'user2')]

test SELECT .. WHERE
[(1, 'room1', 'user1'), (3, 'room2', 'user1')]
[(3, 'room2', 'user1')]

test DELETE ... WHERE
[(1, 'room1', 'user1'), (2, 'room1', 'user2'), (3, 'room2', 'user1')]

test DELETE ... WHERE .. ORDER BY x LIMIT y
[(2, 'room1', 'user2'), (3, 'room2', 'user1')]

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

db = Sqlite3x()
# db = MySQLx()

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

# test delete with multiple conditions
print('\ntest DELETE ... WHERE')
db.delete('rooms_users', {'username': 'user2', 'room': 'room2'})
print(list(db.select('rooms_users')))

# test delete with orderby + limit
print('\ntest DELETE ... WHERE .. ORDER BY x LIMIT y')
db.delete('rooms_users', {'username': 'user1'}, 'id', 1)
print(list(db.select('rooms_users')))
