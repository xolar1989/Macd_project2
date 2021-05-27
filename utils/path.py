import os



def determine_directory(directory):
    root_path_array = str(os.path.dirname(os.path.abspath(__file__))).split("\\")
    root_path_array = root_path_array[:len(root_path_array)-1]
    root_path_array.append(directory)
    result = ""
    for element in root_path_array:
        result += f"{element}\\"
    return result


def determine_absolute_path(path, file):
    if not isinstance(path,str) or not isinstance(file,str):
        raise TypeError("Some values might be not string")
    if not os.path.exists(f"{path}\\{file}"):
        raise FileNotFoundError(f"File not found in path = {path}")
    return f"{path}\{file}"