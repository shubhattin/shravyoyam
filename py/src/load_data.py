import os

import toml

dattAMshType = dict[str, tuple[str, str, int]]


class CONFIG_DATA_TYPE:
    folder_loc: str = ""
    vlc_loc: str = ""


def get_config_data() -> CONFIG_DATA_TYPE:
    tml_file = open("./config.toml", "r", encoding="utf-8")
    toml_data = toml.load(tml_file)
    tml_file.close()
    data = CONFIG_DATA_TYPE()
    try:
        data.folder_loc = os.path.normpath(
            toml_data["folder_loc"].replace("\\", "/"))
        data.vlc_loc = os.path.normpath(
            toml_data["vlc_loc"].replace("\\", "/"))
    except:
        raise FileNotFoundError(
            "Unable to fetch 'folder_loc' and 'vlc_loc' from config.toml")
    if not os.path.isfile(data.vlc_loc) or not os.path.isdir(data.folder_loc):
        raise FileNotFoundError(
            "folder location or vlc location does not exists")
    return data


CONFIG_DATA = get_config_data()


def get_dattAMsh() -> dattAMshType:
    db_file_str: str = open(f'{CONFIG_DATA.folder_loc}/saYc.js',
                            mode="r", encoding="utf-8").read()
    db_file_str = db_file_str[db_file_str.index(
        "{"): db_file_str.index("}") + 1]
    db_file_data = dattAMshType(eval(db_file_str))
    return db_file_data
