import file_checker
import pyexcel as p
import settings
from associations_adder import Application
from content_generator import Content_generator


def prepare_program_files():
    """
    Проверяем и подгатавливаем програмные файлы
    """

    # проверяем settings.txt (на создание)
    f = file_checker.Filechecker()
    f.type = "txt"
    names = f.get_filenames_and_filepathes()

    if "settings" in names:
        settings_path = names.get("settings")
    else:
        settings_path = "./settings.txt"
        with open(settings_path, "w") as somefile:
            somefile.write("* program settings")


    # проверяем names (на создание)
    f = file_checker.Filechecker(type="xlsx")
    f1 = file_checker.Filechecker(type="xls")

    files = f.get_filenames_and_filepathes()
    files1 = f1.get_filenames_and_filepathes()

    all_files = files | files1

    if "names" in all_files:
        system_names_and_associations = all_files.get("names")
        sheet = p.get_sheet(file_name=system_names_and_associations)
        row0 = sheet.row[0]
        if row0 != ["name", "nickname"]:
            sheet.row[0] = ["name", "nickname"]
            sheet.save_as(system_names_and_associations)
    else:
        data = [["name", "nickname"]]
        sheet = p.Sheet(data)
        sheet.name_columns_by_row(0)
        system_names_and_associations = "./names.xlsx"
        sheet.save_as(system_names_and_associations)


    # проверяем settings, добавляем names and nicknames
    with open(file=settings_path, mode="r+", encoding="utf-8") as f:
        lines = f.readlines()
        if "* program settings" not in " ".join(lines):
            f.seek(0, 2)
            f.write("\n")
            f.write("* program settings")
        if "names and nicknames sheet" not in " ".join(lines):
            f.seek(0, 2)
            f.write("\n")
            f.write("names and nicknames sheet : ")

    # проверяем settings, обновляем names and nicknames
    with open(file=settings_path, mode="r+", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if "names and nicknames sheet" in line:
                line_name, line_val = line.split(":")
                line_val = line_val.strip()
                if not line_val:
                    system_names_and_associations = system_names_and_associations.replace("\\", "/")
                    f.seek(0, 2)
                    f.write(system_names_and_associations)

    # добавляем custom name
    with open(file=settings_path, mode='r+', encoding="utf-8") as f:
        if "custom name" not in " ".join(lines):
            f.seek(0, 2)
            f.write("\n")
            f.write("custom name : ")

    # добавляем в settings custom name (если оно указано)
    with open(file=settings_path, mode="r", encoding="utf-8") as f:
        if "custom name" in " ".join(lines):
            lines = f.readlines()
            for line in lines:
                if "custom name" in line:
                    line_name, line_val = line.split(":")
                    line_val = line_val.strip()
                    if line_val:
                        settings.custom_name = line_val


    settings.names_and_nicknames_sheet = system_names_and_associations


if __name__ == '__main__':

    prepare_program_files()

    f = file_checker.Filechecker(type="csv")
    csv_files = f.get_filenames_and_filepathes()

    for k, v in csv_files.items():
        app = Application(csv_sheet=v, associations_sheet=settings.names_and_nicknames_sheet)
        app.make_name_associations()

        gen = Content_generator(associated_sheet=settings.names_and_nicknames_sheet,
                                    csv_sheet=v)

        content = gen.get_content()
        p.save_as(array=content, dest_file_name=f"{k}.xlsx")
