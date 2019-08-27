import curses


class GuiObject:
    def __init__(self, stdscr, height, width, y, x, title=None):
        self.stdscr = stdscr

        self.window = curses.newwin(height, width, y, x)

        self.height = height
        self.width = width

        self.y = y
        self.x = x

        self.title = title

        self.draw()

    def draw(self):
        self.window.clear()
        self.window.border(0)

        if self.title:
            self.window.addstr(0, 1, self.title, curses.A_BOLD)

    def refresh(self):
        self.window.noutrefresh()

    def set_title(self, title):
        self.title = title


class ScrollPane(GuiObject):
    def __init__(self, stdscr, height, width, y, x, title=None, items=None):
        self.items = items if items else []
        self.display_items = self.items.copy()

        super(ScrollPane, self).__init__(stdscr, height, width, y, x, title)

    def append_item(self, item):
        self.items.append(item)
        self.display_items.append(item)

        max_row = self.window.getmaxyx()[0] - 1

        num_items = len(self.display_items)
        if num_items + 1 > max_row:
            self.display_items.pop(0)

        self.draw()

    def draw(self):
        super(ScrollPane, self).draw()
        for index, item in enumerate(self.display_items):
            self.window.addstr(index + 1, 1, str(item))

        self.refresh()


class TextDialog(GuiObject):
    def __init__(self, stdscr, height, width, title=None):
        term_height, term_width = stdscr.getmaxyx()
        y = int(term_height/2 - height/2)
        x = int(term_width/2 - width/2)

        super(TextDialog, self).__init__(stdscr, height, width, y, x, title)
        self.inputting = True
        self.input = ''

    def draw(self):
        super(TextDialog, self).draw()
        # textbox = curses.textpad.Textbox(self.window, insert_mode=True)
        # self.stdscr.keypad(1)
        # self.window.addstr(3, 3, '')
        # # textbox.edit()
        # text = textbox.gather()

        # last = self.window.getch()
        # if last == curses.KEY_ENTER:
        #     self.inputting = False

        self.refresh()

    def get_input(self):
        self.window.keypad(1)
        curses.curs_set(1)
        curses.echo()

        string = self.window.getstr(1, 2).decode(encoding="utf-8")

        self.window.keypad(0)
        curses.curs_set(0)
        curses.noecho()

        return string
