from textnode import TextNode, TextType
from block_markdown_handler import markdown_to_html_node, extract_title
from shutil import rmtree
from os.path import exists, join, dirname, isfile
from os import listdir, mkdir, makedirs
from shutil import copy

dir_path_static = "./static"
dir_path_public = "./public"

template_path = "./template.html"

def main(): 
    # if this is the root call, delete the public dir
    if exists(dir_path_public):
        print("public dir found, deleting")
        rmtree(dir_path_public)

    # copy all static files to equivalent locations in public
    static_to_public(dir_path_static, dir_path_public)

    # generate a page
    generate_page("./content/index.md", template_path, "./public/index.html")

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
            

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path) as md:
        markdown = md.read()
    
    with open(template_path) as tmp:
        template = tmp.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    # check if the destination path exists else make it
    if not exists(dirname(dest_path)):
        makedirs(dest_path)

    with open(dest_path, "w") as file:
        print(page, file=file)
main()