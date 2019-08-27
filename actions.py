import curses
import os
import time

import config
import utils
from cursesmenu import CursesMenu
from ui import ScrollPane, TextDialog


def dummy_gen():
    for i in range(100):
        yield i


def find_and_add_repos(root='/home/jake/Programming'):
    stdscr = CursesMenu.stdscr
    screen_rows, screen_cols = stdscr.getmaxyx()

    width = int((screen_cols * 0.95) / 2)

    search_pane = ScrollPane(stdscr, screen_rows - 5, width, 3, 0, title="Discovered repositories")
    added_pane = ScrollPane(stdscr, screen_rows - 5, width, 3, screen_cols - width, title="New repositories")

    for path in utils.find_git_directories(root, []):

        basename = os.path.basename(path)
        search_pane.append_item(basename)

        if not utils.is_in_database(path):
            added_pane.append_item(basename)
            config.add_repo(path)

        curses.doupdate()

    # TODO Add some kind of confirmation dialog so users can read/accept what just happened
    config.update_config()
    # stdscr.clear()


def select_repo(title):
    print("Select repo")
    time.sleep(2)


def clone_repo():
    pass


def manual_add_repo():
    stdscr = CursesMenu.stdscr
    screen_rows, screen_cols = stdscr.getmaxyx()

    valid = False
    title = "Enter absolute path to repository"
    path = ''
    while not valid:
        text = TextDialog(stdscr, 3, int(screen_cols * 0.8), title)

        path = text.get_input()

        if path == '':  # Exit when an empty string is entered
            return

        if utils.is_git_repo(path):
            if not utils.is_in_database(path):
                valid = True
            else:
                title = "Already in database"
        else:
            title = "Not a valid git repo"

    config.add_repo(path)
    config.update_config()

    curses.doupdate()
