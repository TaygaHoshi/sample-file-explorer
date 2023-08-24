import os
from simple_log import log
from info_gather import run, threaded_run

def get_files():
    all = get_all()

    result = []
    for item in all:
        if os.path.isfile(item):
            result.append(item)
    
    return result

def get_directories():
    all = get_all()

    result = []
    for item in all:
        if os.path.isdir(item):
            result.append(item)
    
    return result

def get_all():
    try:
        return os.listdir()
    except:
        log("Unable to get files from current working directory.", "e")
        return []

def get_current_dir():
    return os.getcwd()

def open_path(path):
    if os.path.isdir(path):
        change_dir(path)
        return 0
    elif os.path.isfile(path):
        open_file(path)
        return 1

def change_dir(newpath):
    try:
        os.chdir(newpath)
        log(f"Current dir changed to '{get_current_dir()}'")
    except:
        log("Unable change current working directory.", "e")

def open_file(path):
    threaded_run(f'xdg-open "{path}" > /dev/null')

def make_directory(dir_name):
    # makes a new directory

    initial_wd = get_current_dir()

    if "/" in dir_name: # if the directory name includes a /, create directories recursively.
        subdirs = dir_name.split("/")
        _temp_path = initial_wd + "/" + subdirs[0]
        try:
            os.mkdir(initial_wd + "/" + subdirs[0])
            log(f"Created directory {_temp_path}")
        except:
            log(f"Unable to create a directory {_temp_path}.", "e")
        
        change_dir(subdirs[0])
        make_directory("/".join(subdirs[1:]))
    else: # create the directory normally if the directory name doesn't include a /
        _temp_path = initial_wd + "/" + dir_name
        try:
            os.mkdir(get_current_dir() + "/" + dir_name)
            log(f"Created directory {_temp_path}")
        except:
            log(f"Unable to create a directory {_temp_path}.", "e")
        
    change_dir(initial_wd)

# change_dir("/home/taygahoshi/Anime")