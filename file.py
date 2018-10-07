import os
from datetime import datetime
import logging
import shutil
from tqdm import tqdm
import sys

from folder import recursive_list

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def filelist_delete(file_list):
    """
    Batch delete of files when handed a list, no confirmation.
    :param file_list:
    :return:
    """
    for file in tqdm(file_list):
        os.remove(file)




def flatcopy(file_list, destination_path, check_function):
    """
    Takes in a list of files and flatten them to the desintation path while ensure they are guarnteed to be unique files.
    :param file_list: the list of files from different path.
    :param destination_path:
    :param check_function: the function used to validate every single file.
    """
    logger = logging.getLogger(__name__)
    logger.info("Copying checking and checking files to destination: " + destination_path)

    from shutil import copyfile

    for file in tqdm(file_list):

        # find if the file is DICOM, if not, skip this file.
        if check_function is not None:
            check_passes, _ = check_function(file)
            if not check_passes:
                continue

        # get the final path name.
        file_name = os.path.basename(file)
        destination_path_name = os.path.join(destination_path, file_name)

        # check if the final path is unique.
        is_unique, new_name = is_name_unique(destination_path_name)

        # append date time microsecond string if the file is not unique.
        if not is_unique:
            destination_path_name = new_name

        copyfile(file, destination_path_name)

def unique_name():
    timestamp = datetime.now().isoformat(sep='T', timespec='auto')
    name = timestamp.replace(":", "_")
    return name

def is_name_unique(path):
    """
    Determine if the proposed file exist and suggest alternative name.
    :param path:
    :return:
    """
    if os.path.exists(path):
        timestamp = datetime.datetime.now().isoformat()
        timestamp = timestamp.replace(':', '')  # Remove : which are not compatible with string

        file, ext = os.path.splitext(path)

        return False, file + "_" + timestamp + "_" + ext
    else:
        return True, path

def duplicates_into_folders(filelist, output_folder, iterations):
    """
    The function takes a list of files and duplicate them with unique names X times into the output folder, then return the updated input list.
    :param filelist:
    :param output_folder:
    :param iterations:
    :return:
    """

    logger.info("Duplication files for " + str(iterations) + " iteraitons.")
    # Duplicate the folder x times
    for x in range(0, iterations):
        # each time, duplicate all the files within it
        for file in tqdm(filelist):
            # Make sure to assign UNIQUE name.
            new_file_name = os.path.join(output_folder, unique_name() + ".png")
            shutil.copyfile(file, new_file_name)

    # Make DIR if it does not already exist.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recursively list the output folder
    updated_file_list = recursive_list(output_folder)

    return updated_file_list

def zip_with_name(folder_path, output_filename):
    shutil.make_archive(output_filename, 'zip', folder_path)