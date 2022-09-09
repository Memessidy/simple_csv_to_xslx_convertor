import name_validator
from name_validator import get_name_val
from file_reductor import Reductor


class Application:
    def __init__(self, csv_sheet, associations_sheet):
        self.path = csv_sheet
        self.associations_sheet = associations_sheet

        self.reductor = Reductor(self.associations_sheet)
        self.content_lists = self.reductor.get_content_from_csv(self.path)
        self.nicknames_and_statuses = []
        self.nicknames_true_status = []
        self.nicknames_false_status = []

    def get_nicknames_and_statuses(self):
        for item in self.content_lists:
            name_and_surname = item[0]
            if "Full Name" in name_and_surname:
                continue
            name_and_surname, status = get_name_val(name_and_surname)
            self.nicknames_and_statuses.append((name_and_surname, status))

    def status_filter(self):
        for item in self.nicknames_and_statuses:
            name = item[0]
            status = item[1]
            if not status:
                self.nicknames_false_status.append(name)
            else:
                self.nicknames_true_status.append(name)

    def add_nicknames(self):
        good_names = self.reductor.get_names()
        cur_names = {}

        for name in good_names:
            cur_names[name] = []

        for good_name in good_names:
            for nickname_item in self.nicknames_true_status:
                nickname_lowercase = nickname_item[1]
                nickname_default = nickname_item[0]
                nickname_default = nickname_default.strip()
                addable = name_validator.check_addable(nickname=nickname_lowercase, good_name=good_name)
                if addable:
                    cur_names[good_name].append(nickname_default)

        for k, v in cur_names.items():
            for i in v:
                self.reductor.change_nickname_per_name(name=k, nickname=i)

    def make_name_associations(self):
        self.get_nicknames_and_statuses()
        self.status_filter()
        self.add_nicknames()
