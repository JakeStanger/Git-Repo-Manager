import utils
import sys
import os
# TODO Write function/method comments throughout

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generator = utils.find_git_directories('/home/jake/Programming', [])
        for i in generator:
            print(i)
            print(os.path.basename(os.path.dirname(i)))
            print(i[-48:])

    else:
        menu = utils.generate_menu()
        # print(menu)
        menu.show()

