import sqlite3

# Make a connection to a database
conn = sqlite3.connect('emaildb.sqlite')

# Create a cursor from connection
cur = conn.cursor()

# Execute SQL statement form cursor
cur.execute('DROP TABLE IF EXISTS Counts')

# Write information to disk
conn.commit()
