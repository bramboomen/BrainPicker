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
        title = re.sub(r'(\.(?! ))', r'\1 ', title)
        title = title.replace(" ", "_")
        title = title.split("|")[0]
        stmnt = "select old_text from page " \
                "inner join text on page.`page_latest` = text.`old_id` " \
                "where page.page_title = %r and page.page_namespace = 0" % title
        result = self.query(stmnt)
        if not result:
            text = "empty"
        elif "# REDIRECT".lower() in str(result[0]["old_text"]).lower():
            links = re.findall('\[\[([^:\]\\\]+)\]\]', str(result[0]["old_text"]))
            text = self.text_from_page(links[0])
        else:
            text = result[0]["old_text"]
        return str(text)

    def get_wiki_links(self, subject):
        text = self.text_from_page(subject)
        links = re.findall('\[\[([^:\]\\\]+)\]\]', str(text))
        return list(set(links))


class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent


def wikipedia_game(start_subject, goal_subject):
    """
    extensive Breadth-first search
    :param start_subject: Start node
    :param goal_subject: Goal node
    :return: List of all found nodes
    """
    wiki = WikiDB()
    start_node = Node(start_subject)
    stack = [[start_node], []]
    visited = []
    depth = 0
    max_depth = 3
    results = []
    while stack:
        if not stack[depth]:
            depth += 1
            if depth > max_depth:
                break
            stack.append([])
        t = stack[depth][0]
        visited.append(t.name)
        del stack[depth][0]
        if goal(wiki, t.name, goal_subject):
            results.append({"node": t, "depth": depth})
            # return t, str(depth)
        elif depth < max_depth:
            children = wiki.get_wiki_links(t.name)
            child_nodes = []
            for child in children:
                if child not in visited:
                    child_nodes.append(Node(child, t))
            stack[depth+1].extend(child_nodes)
    return results, visited.__len__()


def goal(wiki, subject1, subject2):
    text = wiki.text_from_page(subject1)
    if subject2 in str(text):
        return True
    return False


def return_chain(node, end_node):
    chain = [end_node]
    while True:
        chain.insert(0, node.name)
        node = node.parent
        if not node:
            return chain


def test_method():
    s2 = "Johann Sebastian Bach"
    s1 = "Susan Sontag"
    best_result = {"depth": 100000}
    result, vis = wikipedia_game(s1, s2)
    if result:
        for r in result:
            if r["depth"] < best_result["depth"]:
                best_result = r
            print(str(r["depth"]) + " " + str(return_chain(r["node"], s2)))
        print("Number of page visits: " + str(vis))
        print("Number of unique paths: " + str(result.__len__()))
        print("Best path: " + str(best_result["depth"]) + " " + str(return_chain(best_result["node"], s2)))
    else:
        print("nope")
