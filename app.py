import csv
import pyexcel as p
import glob
import os


def get_data(path: str) -> list:
    data = []
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            tag = row[0]
            if tag.startswith("*") or "\ufeff" in tag:
                pass
            else:
                data.append(row)
    return data


def save_data(data: list, name: str):
    p.save_as(array=data, dest_file_name=f"{name}.xlsx")


def get_files():
    filenames = {}
    for csvfile in glob.glob(os.path.join('.', '*.csv')):
        filename = csvfile[:-4].strip(".").strip("\\")
        file_path = csvfile
        filenames[filename] = file_path
    return filenames


def prepare_data(data: list, custom_name) -> list:
    data.sort(key=lambda x: x[0].split()[1] if len(x[0].split()) > 1 else x[0])
    for item in data:
        if "Full Name" in item:
            first_string_index = data.index(item)
            first_string = data.pop(first_string_index)
            data.insert(0, first_string)

        elif custom_name in item:
            second_string_index = data.index(item)
            second_string = data.pop(second_string_index)
            data.insert(1, second_string)
    return data


if __name__ == '__main__':
    names_and_pathes = get_files()
    for name, path in names_and_pathes.items():
        data = get_data(path=path)
        data = prepare_data(data, custom_name="")
        save_data(data=data, name=name)
        os.remove(path)
