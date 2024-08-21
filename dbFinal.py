from sqlite3 import connect

conn = connect('py3.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

name = input('Enter file name: ')
if len(name) < 1:
    name = 'mbox-short.txt'
fh = open(name)
for line in fh:
    if not line.startswith('From '): continue
    pieces = line.split()
    email = pieces[1]

    piece = email.split('@')
    org = piece[1]

    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))

conn.commit()

# https://www.sqlite.org/lang_select.html
query = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(query):
    print(str(row[0]), row[1])

cur.close()
