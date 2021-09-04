from click.testing import CliRunner
import deepdanbooru as dd
from deepdanbooru.commands.add_images_to_project import parse_tags, read_tag_file, copy_image_to_project, add_images_to_project
import pytest
from pathlib import Path
import sqlite3
from unittest.mock import MagicMock, Mock, patch

def test_parse_tags():
  # can parse one liners
  data = parse_tags("""filepath\ttag1 tag2""")
  assert data == [('filepath', 'tag1 tag2')]

  # can parse multi liners
  data = parse_tags("""
    file1\ttag1 tag2
    file2\ttag1 tag2
  """)
  assert data == [
    ('file1', 'tag1 tag2'),
    ('file2', 'tag1 tag2')
  ]

  # skip lines that have no tab separator
  data = parse_tags("""
    file1\ttag1 tag2
    file2
  """)
  assert data == [
    ('file1', 'tag1 tag2'),
  ]

  # preserve empty tag name
  data = parse_tags("""
    file1\t
  """)
  assert data == [
    ('file1', ''),
  ]

def test_read_tag_file():
  runner = CliRunner()
  with runner.isolated_filesystem():

    with open('./tags.txt', 'w') as f:
      f.write("file1\ttag1 tag2\n")

    assert read_tag_file('./tags.txt') == [('file1', 'tag1 tag2')]

def test_copy_image_to_project():
  runner = CliRunner()

  # can copy image to project directory
  with runner.isolated_filesystem():
    tags = """
    file1.jpg\ttag1 tag2
    """
    data = parse_tags(tags)
    for ddt in data:
      with open(ddt[0], 'w') as f:
        f.write(ddt[1])

    dst_path = Path(copy_image_to_project('project', data[0][0])).resolve()
    images_path = Path('project/images').resolve()
    assert dst_path.relative_to(images_path) == Path('eb/ebffef8cba3ea86f0149626a579a6b2e.jpg')

  # skips image if already exists in project directory
  with runner.isolated_filesystem():
    tags = """
    file1.jpg\ttag1 tag2
    """
    data = parse_tags(tags)
    for ddt in data:
      with open(ddt[0], 'w') as f:
        f.write(ddt[1])

    images_path = Path('project/images').resolve()
    already_exists = (images_path / 'eb/ebffef8cba3ea86f0149626a579a6b2e.jpg')
    already_exists.parent.mkdir(exist_ok=True, parents=True)
    already_exists.touch()

    assert copy_image_to_project('project', data[0][0]) == None

def test_add_images_to_project():
  runner = CliRunner()

  with runner.isolated_filesystem():
    tags = """
    file1.jpg\ttag1 tag2
    """
    data = parse_tags(tags)
    for ddt in data:
      with open(ddt[0], 'w') as f:
        f.write(ddt[1])

    with open('tags.txt', 'w') as f:
      f.write(tags)

    project_context = {**dd.project.DEFAULT_PROJECT_CONTEXT, **{'database_path': 'db.sqlite'}}
    dd.commands.create_project('project_path', project_context)
    project_context = dd.project.load_context_from_project('project_path')
    database_path = project_context['database_path']

    con = sqlite3.connect(database_path)
    cur = con.cursor()
    dd.commands.make_posts_table(con, cur)
    con.close()

    add_images_to_project('project_path', 'tags.txt')

    con = sqlite3.connect(database_path)
    cur = con.cursor()
    result = list(cur.execute("SELECT * FROM `posts`"))
    con.close()

    assert result == [(1, 'ebffef8cba3ea86f0149626a579a6b2e', 'jpg', 'tag1 tag2', 2, 0, 0)]
    assert [p for p in Path('project_path/images').glob('**/*') if p.is_file()] == [Path('project_path/images/eb/ebffef8cba3ea86f0149626a579a6b2e.jpg')]

# def test_make_database_from_tag_file():
#   runner = CliRunner()

#   with runner.isolated_filesystem():
#     tags = """
#     file1.jpg\ttag1 tag2
#     """
#     data = parse_tags(tags)
#     for ddt in data:
#       with open(ddt[0], 'w') as f:
#         f.write(ddt[1])

#     with open('tags.txt', 'w') as f:
#       f.write(tags)

#     dd.commands.create_project('test_project')
#     dd.commands.create_database_from_tag_file('test_project', 'tags.txt')
#     project_context = dd.project.load_context_from_project('test_project')
#     database_path = project_context['database_path']

#     con = sqlite3.connect(database_path)
#     cur = con.cursor()
#     result = list(cur.execute("SELECT * FROM `posts`"))
#     con.close()

#     assert result == [(1, 'ebffef8cba3ea86f0149626a579a6b2e', 'jpg', 'tag1 tag2', 2, 0, 0)]
#     assert [p for p in Path('project_path/images').glob('**/*') if p.is_file()] == [Path('project_path/images/eb/ebffef8cba3ea86f0149626a579a6b2e.jpg')]
