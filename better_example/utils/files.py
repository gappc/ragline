# import python modules
import os
import shutil
from typing import BinaryIO

from llama_index import SimpleDirectoryReader
from logger.custom_logger import logger
from server.auth import fake_users_db
from utils.index import index_add_documents, index_delete_by_path
from utils.paths import (
    compute_docs_path,
    compute_tmp_path,
    compute_user_path,
    create_user_paths,
)

# Initialize: create paths for users if they dont exist
for username in fake_users_db:
    create_user_paths(username)


def do_get_files(username: str):
    path = compute_user_path(username)
    # get the path p, sub_directory sub_dir,
    # and filename files from the given path
    walk_method = os.walk(path)

    # using exception handling to remove
    # the stop iteration from generator object
    # which we get the output from os.walk() method.
    while True:
        try:
            p, sub_dir, files = next(walk_method)
            break
        except:
            break

    # Create a list of files in directory along with the size
    size_of_file = [(f, os.stat(os.path.join(path, f)).st_size) for f in files]

    # get the size of the sub_dir of the given path
    for sub in sub_dir:
        i = os.path.join(path, sub)
        size = 0
        for k in os.listdir(i):
            size += os.stat(os.path.join(i, k)).st_size
        size_of_file.append((sub, size))

    # Iterate over list of files along with size
    # and print them one by one.
    # now we have print the result by
    # sorting the size of the file
    # so, we have call sorted function
    # to sort according to the size of the file

    # in this case we have use its file paths.
    # for f, s in sorted(size_of_file, key=lambda x: x[1]):
    #     print("{} : {}MB".format(os.path.join(path, f), round(s / (1024 * 1024), 3)))
    files = list(map(lambda s: {"name": s[0], "size": s[1]}, size_of_file))
    return files


def do_upsert_file(username: str, filename: str, file: BinaryIO):
    tmp_file_path = compute_tmp_path(username, filename)
    dest_file_path = compute_docs_path(username, filename)
    logger.info("Creating file: {}", tmp_file_path)
    with open(tmp_file_path, "wb") as f:
        shutil.copyfileobj(file, f)

        logger.info("File created: {}, now ingesting", tmp_file_path)

        documents = SimpleDirectoryReader(input_files=[tmp_file_path]).load_data()
        index_add_documents(username, documents)

        logger.info(
            "Indexing complete for file {}, now moving to folder ",
            tmp_file_path,
        )

        shutil.move(
            tmp_file_path,
            dest_file_path,
        )


def do_delete_file(username: str, filename: str):
    path = compute_docs_path(username, filename)

    logger.info("Deleting file from filesystem: {}", path)

    os.remove(path)

    logger.info("File deleted filesystem: {}, now removing from index", path)

    delete_result = index_delete_by_path(username, filename)

    logger.info("Removed from index with result: ", delete_result)


if __name__ == "__main__":
    do_get_files("./docs")
