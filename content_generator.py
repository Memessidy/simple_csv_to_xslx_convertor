from file_reductor import Reductor
import settings


class Content_generator:
    def __init__(self, associated_sheet="", csv_sheet=""):
        self.associated_sheet = associated_sheet
        self.csv_sheet = csv_sheet
        self.reductor = Reductor(self.associated_sheet)
        self.content = self.reductor.get_content_from_csv(self.csv_sheet)
        self.nicknames_and_names = self.reductor.get_items()
        self.custom_name = settings.custom_name if settings.custom_name else ""

    def generate_content(self):
        for val in self.content:
            if not "Full Name" in val:
                nickname = val[0]
                for names_string in self.nicknames_and_names:
                    name = names_string[0]
                    nicknames = names_string[1:]
                    if nickname in nicknames:
                        val[0] = name

    def prepare_data(self):
        self.content.sort(key=lambda x: x[0].split()[1] if len(x[0].split()) > 1 else x[0])
        for item in self.content:
            if "Full Name" in item:
                first_string_index = self.content.index(item)
                first_string = self.content.pop(first_string_index)
                self.content.insert(0, first_string)

            elif self.custom_name:
                if self.custom_name in item:
                    second_string_index = self.content.index(item)
                    second_string = self.content.pop(second_string_index)
                    self.content.insert(1, second_string)

    def get_content(self):
        self.generate_content()
        self.prepare_data()
        return self.content
