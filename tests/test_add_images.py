from click.testing import CliRunner
from pathlib import Path
import deepdanbooru as dd

def test_add_read_image_directory():
    runner = CliRunner()

    with runner.isolated_filesystem():
        files = ['images/1.jpg', 'images/2/2.png', 'images/3/3/3.gif', 'images/4.tiff', 'images/5.bmp', 'images/6.txt']
        # create the temporary files

        for ff in files:
            Path(ff).parent.mkdir(parents=True, exist_ok=True)
            with open(ff, 'w+') as fp:
                fp.write(ff)

        images = list(dd.commands.read_image_directory(Path('.')))

        assert images[0] == Path('images/1.jpg')
        assert images[1] == Path('images/4.tiff')
        assert images[2] == Path('images/5.bmp')
        assert images[3] == Path('images/2/2.png')
        assert images[4] == Path('images/3/3/3.gif')

# def test_add_images():

#     runner = CliRunner()

#     with runner.isolated_filesystem():
#         files = ['images/1.jpg', 'images/2/2.png', 'images/3/3/3.gif', 'images/4.tiff', 'images/5.bmp', 'images/6.txt']
#         # create the temporary files

#         for ff in files:
#             Path(ff).parent.mkdir(parents=True, exist_ok=True)
#             with open(ff, 'w+') as fp:
#                 fp.write(ff)

#         dd.commands.read_image_directory(Path('.'))

        # dd.commands.add_images('.', Path('.'))
        # images = [ p for p in Path('images').glob('**/*') if p.is_file() ]
        # print(images)
