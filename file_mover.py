#!/usr/bin/python
""" A simple script to move files between two directories.

Asks for the user's input to search different directories and locate where
the file originates from and where it is to be placed. Renames the file
in the process.

Date: 2014-01-01
Author: Alexander Roth
"""

#TODO Add multiple file implementation

import shutil
import os
import sys


def move(src, dst):
    """Moves files from one directory to another.

    Args:
       src: The name of the source file directory.
       dst: The name of the destination file directory.
    """

    src_fname = raw_input("What file are you looking for? ")
    dst_fname = raw_input("What should the new name be? ")

    src_path = src.strip() + "/" + src_fname.strip()
    dst_path = dst.strip() + "/" + dst_fname.strip()

    while not os.path.isfile(src_path):
        print "The source file does not exist."
        correction = raw_input("Please input the correct file name: ")
        src_path = src.strip() + "/" + correction.strip()

    shutil.move(src_path, dst_path)


def locate(path, directory):
    """Returns the location of a file system directory.

    Args:
        path: The path to the directory being searched for.
        directory: The name of the directory being searched for.

    Returns:
        The string location of the found directory.

    Raises:
        IOError: The directory does not exist
    """
    search_term = "find {search} -name {dir} ".format(search = path, dir = directory)
    search_result = os.popen(search_term)
    location = search_result.readline()

    if (location):
        return location
    else:
        raise IOError("Directory does not exist")


def main():
    src = raw_input("What is the source directory?\n")
    src_path = raw_input("What is the path to the source directory?\n")
    dst = raw_input("What is the destination directory?\n")
    dst_path = raw_input("What is the path to the destination directory?\n")
    start = locate(src_path, src)
    end = locate(dst_path, dst)
    move(start, end)

if __name__ == '__main__':
    status = main()
    sys.exit(status)
