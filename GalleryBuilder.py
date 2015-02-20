import os
import time
import sys
from PIL import Image

img_types = [".jpg", ".png", ".gif", ".bmp"]

def make_img_tag(file_name, dimensions = None):
    tag = ""
    if(dimensions != None):
        tag = "<img src=\"" + file_name
        tag = tag + "\" width=\"" + str(dimensions[0])
        tag = tag + "\" height=\"" + str(dimensions[1]) 
        tag = tag + "\">" + "<br><br>\n"
    else:
        tag = "<img src=\"" + file_name + "\">" + "<br><br>\n"
    return tag

def make_link_tag(name):
    return "<a href=\"" + name + "\"><h1>" + name + "</h1></a><br>\n"

def make_dir_link(dir_name):
    return "<a href=\"" + dir_name + "/index.html\"><h1>" + dir_name + "</h1></a><br>\n"

def get_size(size_list):
    width = size_list[0]
    height = size_list[1]

    while(width > 900 or height > 1500):
        width = width * .99
        height = height * .99

    return (int(width), int(height))

def is_image_file(file_name):
    for ext in img_types:
        if(str(file_name).lower().endswith(ext)):
            return True

def write_gallery(root, html_file):
    gallery_file = open(root + "/index.html", "w")
    gallery_file.write("Last updated: " + time.strftime("%d/%m/%Y") + "\n<br><br>\n\n" + html_file)
    gallery_file.close()

def traverse_dirs(current_dir):
    html_file = ""
    total_images = 0
    total_size = 0
    for root, dirs, files in os.walk(current_dir): # Walk directory tree
        num_pics = 0
        folder_size = 0
        for d in dirs:
            print "--[LOG]-- Creating href link for: " + d
            html_file = make_dir_link(d) + html_file
        for f in files:
            if(is_image_file(f)):
                try:
                    im = Image.open(root + "/" + f)
                    html_file = html_file + make_img_tag(f, get_size(im.size))
                except Exception:
                    print "--[LOG]-- Unable to resize: " + f
                    html_file = html_file + make_img_tag(f)
                num_pics = num_pics + 1
                folder_size = folder_size + os.stat(root + "/" + f).st_size
            elif f == "index.html":
                os.remove(root + "/" + f)
            else:
                print "--[LOG]-- Creating href link for: " + f
                html_file = make_link_tag(f)+ html_file
        if(html_file != ""):
            write_gallery(root, html_file)
            html_file = ""
            print "--[LOG]-- Found " + str(num_pics) + " (" + str(folder_size / 1000000) + "MB) pictures in " + root
        total_images = total_images + num_pics
        total_size = total_size + folder_size
    print "--[LOG]-- Build done, found " + str(total_images) + " (" + str(total_size/ 1000000) + "MB) images"

if __name__ == "__main__":
    sys.stdout = open('log.txt', 'a')
    print "--[LOG]-- " + time.strftime("%d/%m/%Y")
    traverse_dirs(os.path.dirname(os.path.abspath(__file__)))
    print ''
