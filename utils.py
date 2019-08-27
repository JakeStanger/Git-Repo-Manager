import os
from json import dumps

import actions
import config as c
from config import MissingKeyError
from cursesmenu import CursesMenu
from cursesmenu.curses_menu import MenuItem
from cursesmenu.items import FunctionItem, SubmenuItem

from git import Repo, InvalidGitRepositoryError


def get_info_for_repo(repo_path: str):
    try:
        repo = Repo(repo_path)

        if repo.bare:
            return "Bare repo."  # TODO Add bare repo support

        # TODO Get current branch/origin name

        # head = repo.active_branch
        branch = repo.active_branch.name

        print("\n" + repo_path)
        print(branch)

        commits_behind = repo.iter_commits('%s..origin/%s' % (branch, branch))
        commits_ahead = repo.iter_commits('origin/%s..%s' % (branch, branch))

        print("%r behind, %s ahead on %s (%s)" % (sum(1 for c in commits_behind), sum(1 for c in commits_ahead), branch, repo_path))
        return ''

    except InvalidGitRepositoryError:
        return "Invalid repository."


def is_in_database(path: str):
    return path in c.get_repos()


def is_git_repo(path: str):
    # Chop trailing slash because we add one in a second
    if path.endswith('/'):
        path = path[:-1]
    return os.path.isdir(path + '/.git')


def find_git_directories(path, path_list, recursive=True):
    try:  # Trapping a OSError:  File permissions problem I believe
        for entry in os.scandir(path):
            git = '.git'
            # Check against exclusion list
            if not any(exclusion in entry.path for exclusion in c.get_exclusions()) and entry.is_dir():

                # Skip hidden directories if configured to do so
                if c.should_ignore_hidden() and entry.name.startswith('.') and entry.name != git:
                    continue

                if is_git_repo(entry.path):
                    # directory = entry.path[:-len(git)]
                    directory = entry.path
                    path_list.append(directory)
                    yield directory

                elif recursive:  # Recur if directory
                    yield from find_git_directories(entry.path, path_list, recursive)

    except OSError:
        pass


def get_string(section, key, params=None):
    if key in section:
        string = section[key]

        if type(string) != str:
            raise TypeError("Value for key '%s' in '%s' is not a string." % (key, section))

        # Interpret variable strings
        if string.startswith('$'):
            func_name = string[string.find("{")+1:string.find("}")]
            return getattr(c.get_function_module(), func_name)(params)
        else:
            return string
    else:
        optional_keys = ['subtitle']

        if key not in optional_keys:
            if 'title' in section:
                message = "Key '%s' for '%s' does not exist." % (key, section['title'])
            else:
                message = "Key '%s' missing for item without title key.\n\n" + dumps(section, indent=2)

            raise MissingKeyError(message)


def generate_menu(menu=None, menu_cfg=None, parent_title=None):
    if not menu_cfg:
        menu_cfg = c.get_menu()

    if not menu:
        title = get_string(menu_cfg, 'title')
        subtitle = get_string(menu_cfg, 'subtitle', params=parent_title)

        menu = CursesMenu(title, subtitle)

    options = menu_cfg['options']

    if type(options) == str and get_string(menu_cfg, 'type') == 'submenu':
        options_list = c.get_config()[options]
        for option in options_list:
            if 'on_item_select' in menu_cfg:
                title = get_string(menu_cfg, 'title')
                subtitle = get_string(menu_cfg['on_item_select'], 'subtitle', params=option)

                submenu = CursesMenu(title, subtitle)
                option_menu = generate_menu(menu_cfg=menu_cfg['on_item_select'], parent_title=option)
                item = SubmenuItem(option, option_menu, menu=submenu)
            else:
                item = FunctionItem(option, getattr(c.get_action_module(), menu_cfg['action']), [option])  # TODO allow for customisation of module name
            menu.append_item(item)

    else:
        for option in menu_cfg['options']:

            cmd_type = get_string(option, 'type')
            title = get_string(option, 'title')
            action = get_string(option, 'action')

            subtitle = get_string(option, 'subtitle')

            if cmd_type == 'function':
                item = FunctionItem(title, getattr(actions, action))

            elif cmd_type == 'submenu':
                submenu = CursesMenu(title, subtitle)
                item = SubmenuItem(title, submenu, menu=menu)
                generate_menu(submenu, option, title)
            else:
                item = MenuItem(title)

            menu.append_item(item)

    return menu
