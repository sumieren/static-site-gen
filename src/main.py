from textnode import TextNode, TextType
from shutil import rmtree
from os.path import exists, join, dirname, isfile
from os import listdir, mkdir
from shutil import copy

dir_path_static = "./static"
dir_path_public = "./public"

def main(): 
    # if this is the root call, delete the public dir
    if exists(dir_path_public):
        print("public dir found, deleting")
        rmtree(dir_path_public)

    static_to_public(dir_path_static, dir_path_public)

def static_to_public(source, destination):          
    # check if the destination has this director already
    if not exists(destination):
        print(f"{destination} not found, creating..")
        mkdir(destination)

    # check if file is directory or file, then copy it or call this function one layer deeper
    for file in listdir(source):
        source_file_path = join(source, file)
        destination_file_path = join(destination, file)
        if isfile(source_file_path):
            print(f"Copying {file} from {source_file_path} to {destination_file_path}")
            copy(source_file_path, destination_file_path)
        # else it's a dir
        else:
            print(f"Directory found. Searching for files in {file} at {source_file_path}")
            static_to_public(source_file_path, destination_file_path)
            
main()