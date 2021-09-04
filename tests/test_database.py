import deepdanbooru as dd
from click.testing import CliRunner
import sqlite3

def test_make_posts_table():
  runner = CliRunner()
  conn = sqlite3.connect(':memory:')
  cur = conn.cursor()
  dd.commands.make_posts_table(conn, cur)

  cur.execute('SELECT sql  FROM `sqlite_master` WHERE `type` = "table";')
  table = cur.fetchone()[0]

  std = lambda s: list(map(lambda l: l.strip(), s.split('\n')))

  assert std(table) == std("""CREATE TABLE posts (
      id INTEGER NOT NULL PRIMARY KEY,
      md5 TEXT,
      file_ext TEXT,
      tag_string TEXT,
      tag_count_general INTEGER DEFAULT 0,
      is_deleted BOOLEAN DEFAULT 0,
      validation BOOLEAN DEFAULT 0
    )""")

