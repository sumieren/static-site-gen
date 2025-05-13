from textnode import TextNode, TextType
from block_markdown_handler import markdown_to_html_node, extract_title
from shutil import rmtree, copy
from os.path import exists, join, dirname, isfile
from os import listdir, mkdir, makedirs
from sys import argv

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main(): 
    # get the basepath from argv
    if len(argv) > 1:
        base_path = argv[1]

    # if this is the root call, delete the public dir
    if exists(dir_path_public):
        print("public dir found, deleting")
        rmtree(dir_path_public)

    # copy all static files to equivalent locations in public
    static_to_public(dir_path_static, dir_path_public)

    # generate pages
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, base_path)

def static_to_public(source, destination):          
    # check if the destination has this directory already
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
            

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path) as md:
        markdown = md.read()
    
    with open(template_path) as tmp:
        template = tmp.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    # first add the content, then add the basepath
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    page = page.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    
    # check if the destination path exists else make it
    if not exists(dirname(dest_path)):
        makedirs(dirname(dest_path))

    with open(dest_path, "w") as file:
        print(page, file=file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    # check if the destination has this directory already
    if not exists(dest_dir_path):
        print(f"{dest_dir_path} not found, creating..")
        mkdir(dest_dir_path)

    # iterate over every file in the dir to see if its a file or a dir. Copy the file, recurse the dir
    for file in listdir(dir_path_content):
        source_path = join(dir_path_content, file)
        destination_path = join(dest_dir_path, file)

        if isfile(source_path):
            destination_path = destination_path.replace(".md", ".html")
            generate_page(source_path, template_path, destination_path, base_path)
        else:
            print(f"Directory found. Searching for files in {file} at {source_path}")
            generate_pages_recursive(source_path, template_path, destination_path, base_path)
main()