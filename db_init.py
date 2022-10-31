import os
import apsw
from apsw import Error
import sys

def initialize_database():
  try:
      conn = apsw.Connection('./tiny.db')
      c = conn.cursor()
      c.execute('''DROP TABLE IF EXISTS messages''')
      c.execute('''DROP TABLE IF EXISTS announcements''')
      c.execute('''DROP TABLE IF EXISTS users''')

      c.execute('''CREATE TABLE IF NOT EXISTS messages (
          id integer PRIMARY KEY, 
          sender TEXT NOT NULL,
          recipient TEXT,
          reply_to integer,
          message TEXT NOT NULL,
          timestamp TEXT NOT NULL);''')
      c.execute('''CREATE TABLE IF NOT EXISTS announcements (
          id integer PRIMARY KEY, 
          author TEXT NOT NULL,
          text TEXT NOT NULL);''')
      c.execute('''CREATE TABLE IF NOT EXISTS users (
          username TEXT PRIMARY KEY, 
          password TEXT NOT NULL,
          salt TEXT NOT NULL,
          token TEXT NOT NULL);''')

      c.execute('''INSERT INTO users
           VALUES ('alice', '$2b$12$Zx3O9fGC74QXGqVcArpMaubLIPhXRIUElxIuUoj/baKVjbmQCas/m',
           '$2b$12$Zx3O9fGC74QXGqVcArpMau', '6hd+3m4i87!3894@49)RF=32489');''')
    
      c.execute('''INSERT INTO users
           VALUES ('bob', '$2b$12$k4YwCPQ8MPWzJLIUApBoD.lJEtG8F6Om3mL6GbhKmjZhe9AXGYLWq',
           '$2b$12$k4YwCPQ8MPWzJLIUApBoD.', 'b8!fjj4&r))djf4øv&0cbs/d3=3');''')
      
      return conn
  except Error as e:
      print(e)
      sys.exit(1)
