## Load and log shape of different file/data in the folder

import os
import pickle as pk
import numpy as np
import h5py as h5

def log(string, log_file):
    with open(log_file, "a") as f:
        f.write(string+"\n")

# get user's directory input
loop = True
while loop:
    dir_ = input("Please enter a directory for scaning here: ")
    if os.path.isdir(dir_):
        dir_ = os.path.abspath(dir_)
        print("Registered files from: {}...".format(os.path.abspath(dir_)))
        files_paths = [os.path.join(dir_,f) for f in os.listdir(dir_) if f[0] != "."]
        print("Proceeding reading data information from the following files:\n{}".format(files_paths))

        loop=False
    else:
        print("Path does not exist. The current directory is: {}".format(os.getcwd()))
        print("Re-enter a directory name or press Ctrl-C to exit.")


## Unpickle reading info and writing log
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)
log_dir = os.path.abspath("../logs")
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)
    print("Creating log directory at {}.".format(log_dir))
log_file = os.path.join(log_dir, os.path.basename(dir_)+".txt")

# remove existing file
if os.path.isfile(log_file):
    os.remove(log_file)

# Loading data from the list
for file in files_paths:
    # verify that the file is pkl file
    file_size = os.path.getsize(file)
    b_name = os.path.basename(file)
    if file_size > 0:
        print("Reading: {}...".format(b_name))
        ext = b_name.split(".")[-1]
        if ext == "pkl":
            with open(file, "rb") as pk_data:
                data_=pk.load(pk_data)
            log("File name: {}; Data shape: {}".format(b_name, data_.shape), log_file)
        elif ext == "h5":
            # read h5 file
            log("File name: {}".format(b_name), log_file)
            data_=h5.File(file, 'r')
            for key in list(data_.keys()):
                if type(data_[key]) is h5.Dataset:
                    log("    Key: {}; Data shape: {}".format(key, data_[key].shape), log_file)
                elif type(data_[key]) is h5.Group:
                    log("    Parent Key: {}".format(key), log_file)
                    def log_group(name, obj):
                        if type(obj) is h5.Dataset:
                            log("        Key: {}; Data shape: {}".format(name, obj.shape), log_file)
                    data_[key].visititems(log_group)
        else:
            print("Extension unknown, skip current file.")
    else:
        log("File name: {}; File size: {}".format(b_name, file_size), log_file)
if os.path.getsize(log_file) > 0:
    print("Files' informations are saved in {}.".format(log_file))
else:
    print("Cannot unpickle files from list. Verify the file has the right extension.")