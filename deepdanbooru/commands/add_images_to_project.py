import os
import hashlib
from pathlib import Path
import deepdanbooru as dd
import shutil
import sqlite3

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
    dbcur.execute('INSERT INTO `posts` (`md5`, `file_ext`, `tag_string`, `tag_count_general`) VALUES (?, ?, ?, ?);', (pth.stem, pth.suffix[1:], ddt[1], len(ddt[1].split(' '))))

  dbcon.commit()
  dbcon.close()







# def copy_image_to_project_images( imagepath):


# def add_tags_to_database(sqlite_path, data):
#   if not os.path.exists(sqlite_path):
#     raise Exception(f'SQLite database is not exists : {sqlite_path}')

#   connection = sqlite3.connect(sqlite_path)
#   cursor = connection.cursor()

#   cursor.execute('INSERT INTO `posts` (`md5`, `file_ext`, `tag_string`) VALUES (?, ?, ?);', )


#   image_folder_path = os.path.join(os.path.dirname(sqlite_path), 'images')

#   cursor.execute(
#     "SELECT md5, file_ext, tag_string FROM posts WHERE (file_ext = 'png' OR file_ext = 'jpg' OR file_ext = 'jpeg') AND (tag_count_general >= ?) ORDER BY id",
#     (minimum_tag_count,))

#   rows = cursor.fetchall()


# import deepdanbooru as dd

# def read_image_directory(source_path):
#   is_image = lambda f: f.is_file() and f.suffix in ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
#   return [ f for f in source_path.glob('**/*') if is_image(f) ]

# # def feed_images_to_project(project_path):
# #   dd.project.load_project(project_path)


# def add_images(project_path, source_path):

#   print(list(images))

#   return True

# def load_image_to_database(sqlite_path, image_path, tags_string):
#   if not os.path.exists(sqlite_path):
#     raise Exception(f'SQLite database is not exists : {sqlite_path}')

#   connection = sqlite3.connect(sqlite_path)
#   connection.row_factory = sqlite3.Row
#   cursor = connection.cursor()

#   image_folder_path = os.path.join(os.path.dirname(sqlite_path), 'images')

#   cursor.execute(
#     "SELECT md5, file_ext, tag_string FROM posts WHERE (file_ext = 'png' OR file_ext = 'jpg' OR file_ext = 'jpeg') AND (tag_count_general >= ?) ORDER BY id",
#     (minimum_tag_count,))

#   rows = cursor.fetchall()

#   image_records = []

#   for row in rows:
#     md5 = row['md5']
#     extension = row['file_ext']
#     image_path = os.path.join(
#       image_folder_path, md5[0:2], f'{md5}.{extension}')
#     tag_string = row['tag_string']

#     image_records.append((image_path, tag_string))

#   connection.close()

# def read_tags_file(tags_path):
#   with open(tags_path, 'r') as f:
#     lines = f.readlines()
#     data = [tuple(line.split('\t')) for line in lines]
#     return data


