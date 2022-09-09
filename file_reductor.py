import pyexcel as pe
import csv


class Reductor:
    def __init__(self, sheet_path):
        self.sheet_path = sheet_path
        self.sheet = pe.get_sheet(file_name=self.sheet_path, name_columns_by_row=0)

    def change_nicknames(self, str_id: int, nickname: str):
        cur_row = self.sheet.row[str_id]
        if nickname in cur_row[1]:
            pass
        else:
            cur_row[1] += f"{nickname}" if not cur_row[1] else f", {nickname}"
            self.sheet.row[str_id] = cur_row
            self.sheet.save_as(self.sheet_path)

    def get_names(self):
        try:
            names = self.sheet.column['name']
        except:
            names = []
        return names

    def get_id(self, string:str):
        names = self.get_names()
        string_index = names.index(string)
        return string_index

    def get_items(self):
        return list(self.sheet.rows())

    def change_nickname_per_name(self, name: str, nickname: str):
        id = self.get_id(name)
        self.change_nicknames(str_id=id, nickname=nickname)

    @staticmethod
    def get_content_from_csv(path) -> list:
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
