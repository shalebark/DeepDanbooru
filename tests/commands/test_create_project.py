from click.testing import CliRunner
import deepdanbooru as dd
from tests.utils import generate_fixture_from_tag_file

def test_setup_project_from_tag_file():
  runner = CliRunner()
  with runner.isolated_filesystem():

    tags = """
      file1.jpg\ttag1 tag2
      file2.jpg\ttag1
      file3.jpg\ttag3
    """

    with open('./tags.txt', 'w') as f:
      f.write(tags)

    generate_fixture_from_tag_file('./tags.txt')

    dd.commands.setup_project_from_tag_file('test_project', './tags.txt')

    project_context = dd.project.load_context_from_project('test_project')
    assert project_context == {
      'database_path': 'test_project\\db.sqlite',
      'image_width': 299, 'image_height': 299, 'minimum_tag_count': 20, 'model': 'resnet_custom_v2',
      'minibatch_size': 32, 'epoch_count': 10, 'export_model_per_epoch': 10,
      'checkpoint_frequency_mb': 200, 'console_logging_frequency_mb': 10,
      'optimizer': 'adam', 'learning_rate': 0.001,
      'rotation_range': [0.0, 360.0],
      'scale_range': [0.9, 1.1],
      'shift_range': [-0.1, 0.1],
      'mixed_precision': False
    }

    assert dd.project.load_tags_from_project('test_project') == ['file1.jpg\ttag1 tag2', 'file2.jpg\ttag1', 'file3.jpg\ttag3']
    assert dd.data.load_image_records(project_context['database_path'], 0) == [
      ('test_project\\images\\eb\\ebffef8cba3ea86f0149626a579a6b2e.jpg', 'tag1 tag2'),
      ('test_project\\images\\e9\\e9bae3ce1d7ac00b0b1aa2fbddc50cfb.jpg', 'tag1'),
      ('test_project\\images\\ac\\ac00dfc2c5c111870601a37c60d31626.jpg', 'tag3')
    ]
