from json import load

with open('./res/const.json', 'r', encoding='utf-8') as file:
    _const = load(file)

with open('./res/lang.json', 'r', encoding='utf-8') as file:
    _lang = load(file)


def lang(path: str) -> str:
    """
    Get language string from json file.
    :param path: path to language string devided by '.'
    :return:
    """
    value = _lang
    path = path.split('.')
    while path:
        value = value[path.pop(0)]
    return value


TITLE = _const['title']
VERSION = _const['version']
CAPTION = TITLE + ' ' + VERSION
ICON = _const['icon']

_color = _const['color']
BLACK = _color['black']
WHITE = _color['white']
RED = _color['red']
GREEN = _color['green']
BLUE = _color['blue']

_font = _const['font']
PRETENDARD_REGULAR = _font['pretendard-regular']
PRETENDARD_BOLD = _font['pretendard-bold']
