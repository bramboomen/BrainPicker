import datetime as dt

class Logger:
    def __init__(self):
        now = dt.datetime.now()
        self.path = "log/" + \
                    str(now.year) + "-" + \
                    str(now.month) + "-" + \
                    str(now.day) + ":" + \
                    str(now.hour) + "." + \
                    str(now.minute) + ".txt"

    def write_log(self, content):
        file = open(self.path, "a")
        file.write(content + "\n")
        file.close()


log = Logger()
