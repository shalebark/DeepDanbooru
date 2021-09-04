import os
import hashlib
from pathlib import Path
import deepdanbooru as dd
import shutil
import sqlite3
from .make_training_database import md5_column_name, extension_column_name, tags_column_name, tag_count_general_column_name

def parse_tags(lines):
  return [
     tuple(map(lambda x: x.strip(), line.split('\t')))
     for line in lines.split('\n')
     if line.strip() and '\t' in line
  ]

def read_tag_file(filepath):
  with open(filepath, 'r') as f:
    return parse_tags(f.read())

def copy_image_to_project(project_path, image_path):
  pth = Path(image_path)
  if not (pth.exists() and pth.is_file()):
    return None

  with open(image_path, 'rb') as f:
    md5 = hashlib.md5(f.read()).hexdigest()
    dst_path = (Path(project_path) / 'images' / md5[0:2] / (md5 + Path(image_path).suffix)).resolve()
    dst_path.parent.mkdir(exist_ok=True, parents=True)

    if dst_path.exists():
      return None

    shutil.copy2(image_path, dst_path)
    return str(dst_path.resolve())

  return None

def add_images_to_project(project_path, tag_file):
  project_context = dd.project.load_context_from_project(project_path)
  database_path = project_context['database_path']

  dbcon = sqlite3.connect(database_path)
  dbcur = dbcon.cursor()

  data = read_tag_file(tag_file)
  for ddt in data:
    # unable to copy the image over, skip
    dst_path = copy_image_to_project(project_path, ddt[0])
    if not dst_path:
      continue

    pth = Path(dst_path)
    dbcur.execute(f"""
      INSERT INTO `posts`
      (`{md5_column_name}`, `{extension_column_name}`, `{tags_column_name}`, `{tag_count_general_column_name}`)
      VALUES (?, ?, ?, ?);
    """, (pth.stem, pth.suffix[1:], ddt[1], len(ddt[1].split(' '))))

  dbcon.commit()
  dbcon.close()
