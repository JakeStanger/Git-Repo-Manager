import sys
from json import loads, dumps
import curses

default_config = {
    # TODO Create default config
}

config = None


class MissingKeyError(Exception):
    pass


def get_config():
    global config
    if not config:
        # TODO Generate fresh default config if one does not exist
        with open('config.json', 'r') as f:
            config = loads(f.read())

    return config


def update_config():
    with open('config.json', 'w') as f:
        f.write(dumps(config, indent=2))


def get_modules():
    return get_config()['modules']


def get_scanner():
    return get_config()['scanner']


def get_ui():
    return get_config()['ui']


def get_menu():
    return get_config()['menu']


def get_repos():
    return get_config()['repos']


def add_repo(repo):
    if repo.endswith('/'):
        repo = repo[:-1]
    get_config()['repos'].append(repo)


def get_exclusions():
    return get_scanner()['exclude_directories']


def should_ignore_hidden():
    return get_scanner()['should_ignore_hidden']


def get_function_module():
    return sys.modules.get(get_modules()['function_module'])


def get_action_module():
    return sys.modules.get(get_action_module()['action_module'])


def should_display_selected_option_at_top():
    return get_ui()['display_selected_option_at_top']


def get_highlight_color(): # TODO Add support for hex colours
    color = get_ui()['highlight_color']
    return {
        'blue': curses.COLOR_BLUE,
        'yellow': curses.COLOR_YELLOW,
        'black': curses.COLOR_BLACK,
        'cyan': curses.COLOR_CYAN,
        'green': curses.COLOR_GREEN,
        'magenta': curses.COLOR_MAGENTA,
        'red': curses.COLOR_RED,
        "white": curses.COLOR_WHITE
    }.get(color)
