import sqlite3
connection = sqlite3.connect('brain.db')

c = connection.cursor()

c.execute('''CREATE TABLE article
                (
                    url VARCHAR(250) PRIMARY KEY,
                    title VARCHAR(250)
                )
          ''')

c.execute('''CREATE TABLE reference
                (
                    id INT PRIMARY KEY,
                    url VARCHAR(250),
                    ref VARCHAR(250),
                    CONSTRAINT reference FOREIGN KEY (ref) REFERENCES article (url)
                )
          ''')

connection.commit()
connection.close()