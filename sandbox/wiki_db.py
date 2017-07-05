import pymysql
import re


class WikiDB:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    user='brain',
                                    db='wiki',
                                    cursorclass=pymysql.cursors.DictCursor)

    def query(self, statement):
        with self.conn.cursor() as cursor:
            cursor.execute(statement)
            result = cursor.fetchall()
        return result

    def text_from_page(self, title):
        title = title.replace(" ", "_")
        stmnt = "select old_text from page " \
                "inner join text on page.`page_latest` = text.`old_id` " \
                "where page.page_title = %r and page.page_namespace = 0" % title
        result = self.query(stmnt)
        return result[0]["old_text"]


def get_wiki_links(text):
    l = re.findall('\[\[([^\]]+)\]\]', str(text))
    ignore = [":", "\\"]
    result = [x for x in l if not any(ign in x for ign in ignore)]
    return list(set(result))


w = WikiDB()
l = get_wiki_links(w.text_from_page("Cascading Style Sheets"))
for x in l:
    print(x)