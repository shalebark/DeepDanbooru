from click.testing import CliRunner
import deepdanbooru as dd
from deepdanbooru.commands.add_images_to_project import parse_tags, read_tag_file, copy_image_to_project, add_images_to_project
from pathlib import Path
import sqlite3

def test_toggle_project_images():
    runner = CliRunner()

    with runner.isolated_filesystem():
      # code to bootstrap test project
      dd.commands.create_project('test_project',
        {
          **dd.project.DEFAULT_PROJECT_CONTEXT,
          'database_path': str(Path('test_project') / 'db.sqlite')
        }
      )
      project_context = dd.project.load_context_from_project('test_project')
      db_path = project_context['database_path']

      conn = sqlite3.connect(db_path)
      curr = conn.cursor()
      dd.commands.make_posts_table(conn, curr)

      conn.commit()
      conn.close()

      # generate a dummy tags file to feed to database
      tags = """
        file1.jpg\ttag1 tag2
        file2.jpg\ttag1
        file3.jpg\ttag3
      """

      with open('./tags.txt', 'w') as f:
        f.write(tags)

      data = parse_tags(tags)
      for ddt in data:
        with open(ddt[0], 'w') as f:
          f.write(ddt[1])

      dd.commands.add_images_to_project('test_project', 'tags.txt')

      # actual tests
      dd.commands.toggle_project_images_randomly('test_project', 1, to_enable=False)
      assert len(dd.data.load_image_records(db_path, 0)) == 2


