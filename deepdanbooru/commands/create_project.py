import os
import shutil
import deepdanbooru as dd
from pathlib import Path
import sqlite3

def create_project(project_path, project_context=None):
    """
    Create new project with default parameters.
    """
    dd.io.try_create_directory(project_path)
    project_context_path = os.path.join(project_path, 'project.json')
    dd.io.serialize_as_json(
        dd.project.DEFAULT_PROJECT_CONTEXT if project_context is None else project_context, project_context_path)

    print(f'New project was successfully created. ({project_path})')

def setup_project_from_tag_file(project_path, tag_file, project_context=None):
  # setup project using db_path defaulted to tags.txt
  projp = Path(project_path)
  dd.commands.create_project(projp,
    {
      'database_path': str((projp / 'db.sqlite').resolve()),
      **(
        {
          k: v for k, v in (project_context if project_context else dd.project.DEFAULT_PROJECT_CONTEXT).items() if v is not None
        }
      ),
    }
  )

  project_context = dd.project.load_context_from_project(projp)
  db_path = project_context['database_path']

  conn = sqlite3.connect(db_path)
  curr = conn.cursor()
  dd.commands.make_posts_table(conn, curr)

  conn.commit()
  conn.close()

  dd.commands.add_images_to_project(projp, tag_file)

  shutil.copyfile(tag_file, projp / 'tags.txt')

