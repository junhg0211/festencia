from json import load, dump

with open('./res/settings.json', 'r', encoding='utf-8') as file:
    settings = load(file)


def update(key, value):
    global settings
    settings[key] = value
    save()


def save():
    with open('./res/settings.json', 'w', encoding='utf-8') as file_:
        dump(settings, file_)
