# import python modules
import os


def do_get_files(path: str):
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


def do_delete_file(path: str):
    os.remove(path)


if __name__ == "__main__":
    do_get_files("/home/chris/projects/ml/rag/ragline/.cache/docs")
