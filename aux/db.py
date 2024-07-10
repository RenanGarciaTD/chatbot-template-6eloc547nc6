
import os
import socket

import pg8000

class Db:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    _instance = []
    def __init__(self) -> None:
        self.load_env()

    def load_env(self):
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_USER = os.environ.get("DB_USER")
        self.DB_PASSWORD = os.environ.get("DB_PASSWORD")
        self.DB_HOST = self.get_ip_address(os.environ.get("DB_HOST"))
        self.DB_PORT = os.environ.get("DB_PORT")

    def get_ip_address(self, host):
        try:
            ip_address = socket.gethostbyname(host)
            return ip_address
        except socket.gaierror:
            print("Erro ao obter ip")
            return None

    def query_insert(self, query, values):
        with pg8000.connect(host=self.DB_HOST, port=self.DB_PORT, database=self.DB_NAME, user=self.DB_USER, password=self.DB_PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor = conn.cursor()
                cursor.execute(query, values)
                obj_inserted = cursor.fetchone()
                conn.commit()
                return obj_inserted

    def query_select(self, query):
        with pg8000.connect(
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
        ) as conn:
            with conn.cursor() as cursor:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
