import sys

import click

import deepdanbooru as dd

__version__ = '1.0.0'


@click.version_option(prog_name='DeepDanbooru', version=__version__)
@click.group()
def main():
  '''
  AI based multi-label girl image classification system, implemented by using TensorFlow.
  '''
  pass


@main.command('create-project')
@click.argument('project_path', type=click.Path(exists=False, resolve_path=True, file_okay=False, dir_okay=True))
def create_project(project_path):
  dd.commands.create_project(project_path)


@main.command('download-tags')
@click.option('--limit', default=10000, help='Limit for each category tag count.')
@click.option('--minimum-post-count', default=500, help='Minimum post count for tag.')
@click.option('--overwrite', help='Overwrite tags if exists.', is_flag=True)
@click.argument('path', type=click.Path(exists=False, resolve_path=True, file_okay=False, dir_okay=True))
def download_tags(path, limit, minimum_post_count, overwrite):
  dd.commands.download_tags(path, limit, minimum_post_count, overwrite)


@main.command('make-training-database')
@click.argument('source_path', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False), nargs=1, required=True)
@click.argument('output_path', type=click.Path(exists=False, resolve_path=True, file_okay=True, dir_okay=False), nargs=1, required=True)
@click.option('--start-id', default=1, help='Start id.', )
@click.option('--end-id', default=sys.maxsize, help='End id.')
@click.option('--use-deleted', help='Use deleted posts.', is_flag=True)
@click.option('--chunk-size', default=5000000, help='Chunk size for internal processing.')
@click.option('--overwrite', help='Overwrite tags if exists.', is_flag=True)
@click.option('--vacuum', help='Execute VACUUM command after making database.', is_flag=True)
def make_training_database(source_path, output_path, start_id, end_id, use_deleted, chunk_size, overwrite, vacuum):
  dd.commands.make_training_database(source_path, output_path, start_id, end_id,
                     use_deleted, chunk_size, overwrite, vacuum)


@main.command('train-project')
@click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.option('--source-model', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False))
def train_project(project_path, source_model):
  dd.commands.train_project(project_path, source_model)


@main.command('evaluate-project', help='Evaluate the project. If the target path is folder, it evaulates all images recursively.')
@click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.argument('target_path', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True))
@click.option('--threshold', help='Threshold for tag estimation.', default=0.5)
def evaluate_project(project_path, target_path, threshold):
  dd.commands.evaluate_project(project_path, target_path, threshold)


@main.command('grad-cam', help='Experimental feature. Calculate activation map using Grad-CAM.')
@click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.argument('target_path', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True))
@click.argument('output_path', type=click.Path(resolve_path=True, file_okay=False, dir_okay=True), default='.')
@click.option('--threshold', help='Threshold for tag estimation.', default=0.5)
def grad_cam(project_path, target_path, output_path, threshold):
  dd.commands.grad_cam(project_path, target_path, output_path, threshold)


@main.command('evaluate', help='Evaluate model by estimating image tag.')
@click.argument('target_paths', nargs=-1, type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=True))
@click.option('--project-path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True),
        help='Project path. If you want to use specific model and tags, use --model-path and --tags-path options.')
@click.option('--model-path', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False))
@click.option('--tags-path', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False))
@click.option('--threshold', default=0.5)
@click.option('--allow-gpu', default=False, is_flag=True)
@click.option('--compile/--no-compile', 'compile_model', default=False)
@click.option('--allow-folder', default=False, is_flag=True, help='If this option is enabled, TARGET_PATHS can be folder path and all images (using --folder-filters) in that folder is estimated recursively. If there are file and folder which has same name, the file is skipped and only folder is used.')
@click.option('--folder-filters', default='*.[Pp][Nn][Gg],*.[Jj][Pp][Gg],*.[Jj][Pp][Ee][Gg],*.[Gg][Ii][Ff]', help='Glob pattern for searching image files in folder. You can specify multiple patterns by separating comma. This is used when --allow-folder is enabled. Default:*.[Pp][Nn][Gg],*.[Jj][Pp][Gg],*.[Jj][Pp][Ee][Gg],*.[Gg][Ii][Ff]')
@click.option('--verbose', default=False, is_flag=True)
def evaluate(target_paths, project_path, model_path, tags_path, threshold, allow_gpu, compile_model, allow_folder, folder_filters, verbose):
  dd.commands.evaluate(target_paths, project_path, model_path, tags_path, threshold, allow_gpu, compile_model, allow_folder, folder_filters, verbose)

@main.command('add-images-to-project', help='Adds images from a directory to the project data')
@click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.argument('tags_path', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False))
def add_images_to_project(project_path, tags_path):
  dd.commands.add_images_to_project(project_path, tags_path)

@main.command('measure-project')
@click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.option('--use-validation', is_flag=True, default=False)
def measure_project(project_path, use_validation):
  dd.commands.measure_project(project_path, use_validation)

@main.group()
def utils():
  pass

@utils.command('toggle-data-set', help='Toggle a Number of DataSet as Enabled or Disabled Randomly')
@click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.argument('number_of_images', type=int)
@click.option('--to-enable/--to-disable', default=True, is_flag=True)
def toggle_data_set(project_path, number_of_images, to_enable=True):
  dd.commands.toggle_project_images_randomly(project_path, number_of_images, to_enable=to_enable)

@utils.command('toggle-validation-data-set', help='Toggle a Number of DataSet as Validation or Training Set Randomly')
@click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.argument('number_of_images', type=int)
@click.option('--to-train/--to-validate', default=True, is_flag=True)
def toggle_validation_data_set(project_path, number_of_images, to_train=False):
  dd.commands.toggle_project_validate_images_randomly(project_path, number_of_images, to_validation=(not to_train))

if __name__ == '__main__':
  main()
