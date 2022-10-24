import os
import apsw
from apsw import Error
import sys

def initialize_database():
  try:
      os.remove("tiny.db")
      conn = apsw.Connection('./tiny.db')
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS messages (
          id integer PRIMARY KEY, 
          sender TEXT NOT NULL,
          message TEXT NOT NULL);''')
      c.execute('''CREATE TABLE IF NOT EXISTS announcements (
          id integer PRIMARY KEY, 
          author TEXT NOT NULL,
          text TEXT NOT NULL);''')
      c.execute('''CREATE TABLE IF NOT EXISTS users (
          id integer PRIMARY KEY,
          username TEXT UNIQUE, 
          password TEXT NOT NULL,
          salt TEXT NOT NULL,
          token TEXT NOT NULL);''')

      c.execute('''INSERT INTO users
          VALUES ('1', 'alice', '$2b$12$Zx3O9fGC74QXGqVcArpMaubLIPhXRIUElxIuUoj/baKVjbmQCas/m',
          '$2b$12$Zx3O9fGC74QXGqVcArpMau', 'tiktok');''')

      return conn
  except Error as e:
      print(e)
      sys.exit(1)
