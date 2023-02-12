import sqlite3
from sqlite3 import Error
from urllib.error import URLError
from urllib.request import urlopen, Request
import re
import pandas as pd
import datetime


class URLMining:

    doc_name = ''

    def __init__(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect("urls.db")
            print("connection successful")
        except Error as e:
            print(f"the error '{e}' occurred")

    def parse_verify(self, text, doc_name):
        self.doc_name = doc_name
        regex = re.compile(r'(https?://\S+)', flags=re.IGNORECASE)
        links_list = regex.findall(text)
        print(links_list)
        cursor = self.connection.cursor()
        create_table = """
            CREATE TABLE IF NOT EXISTS """ + str(doc_name) + """(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            result TEXT,
            date TEXT
            );
        """
        cursor.execute(create_table)
        self.connection.commit()
        for i in range(len(links_list)):
            req = Request(links_list[i])
            zap = """
            INSERT INTO """ + doc_name + """(link, result, date)
            VALUES (?, ?, ?)
            """
            try:
                urlopen(req)
                cursor.execute(zap, (links_list[i], "ok", datetime.datetime.now()))
                self.connection.commit()
            except URLError as e:
                cursor.execute(zap, (links_list[i], str(e), datetime.datetime.now()))
                self.connection.commit()
        self.connection.close()

    def get_table(self):
        self.connection = sqlite3.connect("urls.db")
        q = """
        SELECT * FROM """ + self.doc_name + """;
        """
        df = pd.read_sql(q, self.connection)
        df.to_csv(str(self.doc_name)+".csv", index=False)
        self.connection.close()




