from json import load, dump
from os.path import isfile
from random import randint

_path = './res/settings.json'
_default = {
    "name": f"UNNAMED-{randint(0, 999999):06d}",
    "room_title": "Room",
    "port": "31872",
    "host": "localhost"
}


def update(key, value):
    """
    Updates the settings file with the given key and value, and saves it to disk.
    :param key: the key to update
    :param value: the value to update the key with
    """
    global settings
    settings[key] = value
    save()


def save():
    """ Saves the settings to disk. """
    with open('./res/settings.json', 'w', encoding='utf-8') as file_:
        dump(settings, file_)


if isfile(_path):
    with open(_path, 'r', encoding='utf-8') as file:
        settings = load(file)
else:
    settings = _default.copy()
    save()
