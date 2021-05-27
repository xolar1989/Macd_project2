import os

from utils.path import determine_directory


def file_options():
    return [file.replace("result","").replace(".csv","") for file in os.listdir(path=determine_directory("datagrams")) ]
