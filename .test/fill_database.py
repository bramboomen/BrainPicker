import sqlite3
connection = sqlite3.connect('brain.db')

c = connection.cursor()

c.execute('''INSERT INTO article VALUES (
          "https://www.brainpickings.org/2017/03/14/einstein-grieving-father-letter/",
          "Einstein’s Remarkable Letter to a Grief-Stricken Father Who Had Just Lost His Son"
          )
          ''')

c.execute('''INSERT INTO article VALUES (
          "https://www.brainpickings.org/2012/04/09/dear-professor-einstein-girl/",
          "Women in Science: Einstein’s Advice to a Little Girl Who Wants to Be a Scientist"
          )
          ''')

c.execute('''INSERT INTO article VALUES (
          "https://www.brainpickings.org/2017/03/13/letters-of-consolation/",
          "Living and Loving Through Loss: Beautiful Letters of Consolation from Great Artists, Writers, and Scientists"
          )
          ''')

c.execute('''INSERT INTO reference VALUES (
          1,
          "https://www.brainpickings.org/2017/03/14/einstein-grieving-father-letter/",
          "https://www.brainpickings.org/2012/04/09/dear-professor-einstein-girl/"
          )
          ''')

c.execute('''INSERT INTO reference VALUES (
          2,
          "https://www.brainpickings.org/2017/03/14/einstein-grieving-father-letter/",
          "https://www.brainpickings.org/2017/03/13/letters-of-consolation/"
          )
          ''')

connection.commit()
connection.close()