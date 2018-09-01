import os

def is_empty(input_folder):

    # when folder does not exist
    if not os.path.exists(input_folder):
        return True

    # the the folder is not empty.
    if len(os.listdir(input_folder)) > 0:
        return False

    # must be empty then
    return True

def recursive_list(root_dicom_path):
    """
    load all the files, validate and then pass to decompress or anonimize.
    :param root_dicom_path:
    :return:
    """
    global file_list
    file_list = []

    for root, directories, filenames in os.walk(root_dicom_path):
        #for directory in directories:
            #file_list.append(os.path.join(root, directory))
        for filename in filenames:
            file_list.append(os.path.join(root,filename))
    return file_list

def create(input_folder):
    """
    Create a folder intellgently throw error if needed be.
    :param input_folder:
    :return:
    """
    if os.path.exists(input_folder) and is_empty(input_folder):
        return
    elif os.path.exists(input_folder) and not is_empty(input_folder):
        raise ValueError("Folder exist and not empty!")
    elif not os.path.exists(input_folder):
        os.mkdir(input_folder)
    else:
        raise ValueError
