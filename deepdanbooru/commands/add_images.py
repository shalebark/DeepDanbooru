import deepdanbooru as dd

def read_image_directory(source_path):
    is_image = lambda f: f.is_file() and f.suffix in ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
    return [ f for f in source_path.glob('**/*') if is_image(f) ]

# def feed_images_to_project(project_path):
#     dd.project.load_project(project_path)


def add_images(project_path, source_path):

    print(list(images))

    return True