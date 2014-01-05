#!/usr/bin/python
""" A script designed to reformat files and move them across directories.

Asks the user for the formatting style for file names, the way to recognize
said files and transfers them to another directory.

Date: 2014-01-03
Author: Alexander Roth
"""

import os
import shutil
import sys
import glob
from datetime import datetime


def locate(directory):
    """Returns the location of a file system directory.

    Args:
        directory: The name of the directory being searched for.

    Returns:
        The string location of the found directory.

    Raises:
        IOError: The directory does not exist
    """
    #TODO make more general, currently specific to my file hierachy.
    search_term = "find /Users/aisaacroth/Documents -name " + directory
    search_result = os.popen(search_term)
    location = search_result.readline().strip()

    if (location):
        return location
    else:
        raise IOError("Directory does not exist")


def move(src_dir, dst_dir, src_files, dst_files):
    """Moves files from one directory to another.

    Args:
        src_dir: The source directory where the files will be moved from.
        dst_dir: The destination directory where the files will be moved to.
        src_files: The list of source files being renamed.
        dst_files: The list of destination files that are being created.
    """
    for src, dst in zip(src_files, dst_files):
        src_file, dst_file = (src, dst)
        src_path = src_dir + "/" + src_file.strip()
        dst_path = dst_dir + "/" + dst_file.strip()

        shutil.move(src_path, dst_path)


def recognize(src_names=None):
    """Recognizes file names from user input.

    Args:
        src_name: The name of the files that will be recognized, if None then
            it will pick up all the files in the directory.

    Returns:
        A list of Strings containing all the file names in the present working
        directory.

    Raises:
        ValueError: raises a ValueError when file_list is empty.
    """
    file_list = []
    if src_names:
        file_list = src_names.split(",")
        print file_list
    else:
        types = ('*.pdf', '*.png', '*.doc')
        for src in types:
            file_list.extend(glob.glob(src))

    if not file_list:
        raise ValueError("There are no files in the source directory.")

    return file_list


def reformat(src_list, style=None):
    """Reformats files to a given style, as stated by the user.

    Args:
        src_list: The list of source files.
        style: The representation that the user wanted. If none,
            it will reformat according to the Date and Time of the notes.

    Returns:
        A list of Strings that contain the names of the destination files.
    """
    dst_list = []
    count = 1
    if style:
        for src in src_list:

            index = src.index(".")
            extension = src[index:]
            dst_list.append(style + ", " + str(count) + extension)
            count += 1
    else:
        for src in src_list:
            index = src.index(".")
            extension = src[index:]
            dst_list.append(str(get_modification_date(src.strip())) + 
                            extension)
    return dst_list


def get_modification_date(filename):
    """Returns the creation date and time of the file. """
    temp = os.path.getctime(filename)
    return datetime.fromtimestamp(temp)


def main():

    # Store the home directory.
    home = os.getcwd() 
    src = raw_input("What is the source directory?\n")
    dst = raw_input("What is the destination directory?\n")

    # Locate both source and destination directory.
    start = locate(src)
    end = locate(dst)

    # Change to source directory to manipulate files.
    os.chdir(start)
    file_response = raw_input("If you know all the names of the files you are "
                              "looking for,\nplease enter them now. If you "
                              "want to move all files in the\nsource "
                              "directory, please press ENTER\n")

    if file_response:
        src_files = recognize(file_response)
    else:
        src_files = recognize()

    style_response = raw_input("Please input a custom response style with an "
                               "incremented value at the end.\nOtherwise, the "
                               "default will be a timestamp of the file's "
                               "creation time\n")
    try:
        if style_response:
            dst_files = reformat(src_files, style_response)
        else:
            dst_files = reformat(src_files)
    except OSError as e:
        sys.exit("OS error({0}): {1}".format(e.errno, e.strerror))

    # Return to the home directory.
    os.chdir(home)

    move(start, end, src_files, dst_files)
    print "Script Completed!"


if __name__ == '__main__':
    status = main()
    sys.exit(status)
