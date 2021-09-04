from .make_training_database import table_name, id_column_name, deleted_column_name
from ..project import load_context_from_project
import sqlite3

def toggle_project_images_randomly(project_path, number_of_images, to_enable = True):
  project_context = load_context_from_project(project_path)
  db_path = project_context['database_path']

  conn = sqlite3.connect(db_path)
  curr = conn.cursor()

  curr.execute(f"""
    UPDATE `{table_name}` SET `{deleted_column_name}` = ?
    WHERE {id_column_name} in (SELECT {id_column_name} FROM `{table_name}` ORDER BY random() LIMIT ?)
  """, (int(not to_enable), number_of_images))

  conn.commit()
  conn.close()
