import os
from pydantic.dataclasses import dataclass
import toml

dattAMshType = dict[str, tuple[str, str, int]]

@dataclass
class CONFIG_DATA_TYPE:
    folder_loc: str = ""
    vlc_loc: str = ""
    success: bool = True  # True by default and on error `False`


def get_config_data() -> CONFIG_DATA_TYPE:
    tml_file = open("./config.toml", "r", encoding="utf-8")
    tml_data = toml.load(tml_file)
    tml_file.close()
    data = CONFIG_DATA_TYPE(**tml_data)
    if data.vlc_loc == "" or data.folder_loc == "":
        data.success = False
    if data.success:
        # Normalising path
        data.folder_loc = os.path.normpath(data.folder_loc.replace("\\", "/"))
        data.vlc_loc = os.path.normpath(data.vlc_loc.replace("\\", "/"))
    return data


CONFIG_DATA = get_config_data()


def get_dattAMsh() -> dattAMshType:
    if not CONFIG_DATA.success:
        raise FileNotFoundError(
            "Unable to fetch 'folder_loc' and 'vlc_loc' from config.toml")

    db_file_str: str = open(f'{CONFIG_DATA.folder_loc}/saYc.js',
                            mode="r", encoding="utf-8").read()
    db_file_str = db_file_str[db_file_str.index(
        "{"): db_file_str.index("}") + 1]
    db_file_data = dattAMshType(eval(db_file_str))
    return db_file_data
