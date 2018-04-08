import pymysql

class InsertMysql():
    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', '123456', 'hooli', charset='utf8')
        # self.db = pymysql.connect('192.168.3.195', 'root', '521797', 'pythonnb', charset='utf8')
        # self.db = pymysql.connect('47.52.78.196', 'admin1', '759ce694b4', 'hooli_study', charset='utf8')
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()
