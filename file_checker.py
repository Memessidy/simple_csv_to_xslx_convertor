import glob
import os


class Filechecker:
    def __init__(self, type=""):
        self.type = type
        self.filenames = {}

    def generate_pathes(self):
        if self.type:
            filenames = {}
            type_of_file = f"*.{self.type}"
            length_of_name = len(self.type)+1
            for csvfile in glob.glob(os.path.join('.', type_of_file)):
                filename = csvfile[:-length_of_name].strip(".").strip("\\")
                file_path = csvfile
                filenames[filename] = file_path
            self.filenames = filenames

    def get_filenames_and_filepathes(self):
        if not self.type:
            raise ValueError("Type is empty!")
        if self.filenames:
            self.filenames = {}

        self.generate_pathes()
        return self.filenames
