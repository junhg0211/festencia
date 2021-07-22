from json import load

with open('./res/settings.json', 'r', encoding='utf-8') as file:
    settings = load(file)

name = settings['name']
