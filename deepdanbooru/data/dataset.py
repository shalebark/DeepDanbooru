import os
import sqlite3


def load_tags(tags_path):
    with open(tags_path, 'r') as tags_stream:
        tags = [tag for tag in (tag.strip() for tag in tags_stream) if tag]
        return tags


def load_image_records(sqlite_path, minimum_tag_count, use_validation=False):
    if not os.path.exists(sqlite_path):
        raise Exception(f'SQLite database is not exists : {sqlite_path}')

    connection = sqlite3.connect(sqlite_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    image_folder_path = os.path.join(os.path.dirname(sqlite_path), 'images')

    cursor.execute(
        "SELECT md5, file_ext, tag_string FROM posts WHERE (file_ext = 'png' OR file_ext = 'jpg' OR file_ext = 'jpeg') AND (tag_count_general >= ?) AND `is_deleted` = 0 AND `validation` = ? ORDER BY id",
        (minimum_tag_count, 1 if use_validation else 0 ))

    rows = cursor.fetchall()

    image_records = []

    for row in rows:
        md5 = row['md5']
        extension = row['file_ext']
        image_path = os.path.join(
            image_folder_path, md5[0:2], f'{md5}.{extension}')
        tag_string = row['tag_string']

        image_records.append((image_path, tag_string))

    connection.close()

    return image_records
