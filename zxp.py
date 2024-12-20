import os
import json
import curses
from curses import wrapper
import consts
import readline
import glob
import logging
import argparse
import sys
from shutil import rmtree

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log', action='store_true', help='Enable logging (stores file where executable is)')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.2.0')
args = parser.parse_args()

if args.log:
    logging.basicConfig(
        filename="zxp.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO
    )

emojis = json.load(
    open(os.path.join(os.path.dirname(__file__), "emojis.json")))


def draw_menu(stdscr, files, current_dir, current_input):
    curses.init_pair(1, consts.ACCENT_COLOR, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, consts.ACCENT_COLOR)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    BLUE_AND_BLACK = curses.color_pair(1)
    HIGHLIGHT = curses.color_pair(2)
    WHITE_AND_BLACK = curses.color_pair(3)

    stdscr.clear()
    h, w = stdscr.getmaxyx()

    #if consts.SHOW_HELP == True:
    #    stdscr.addstr(  # Help text
    #        h - 1,
    #        w - len(consts.HELP_TEXT) - 1, consts.HELP_TEXT, curses.A_BOLD,)

    stdscr.addstr(0, 0, current_dir, HIGHLIGHT)

    pad = curses.newpad(h, w) # h, w

    current_line = 0
    current_column = 0
    longest = 0

    for i in files:
        if current_line >= h:
            current_line = 0
            current_column += 1

        if len(i) > longest:
            longest = len(i) + 1

        try:
            # Make this work while typing instad of just after enter is pressed

            if i[2:] == current_input:  # The [2:] is to remove the emoji
                pad.addstr(
                    current_line,
                    (current_column * longest) + (current_column != 0) * 2,
                    i,
                    HIGHLIGHT)
            else:
                pad.addstr(
                    current_line,
                    (current_column * longest) + (current_column != 0) * 2,
                    i,
                    BLUE_AND_BLACK if i[0] == "📂" else WHITE_AND_BLACK)
        except curses.error:
            pass  # This happens when the terminal is too small. Temporary fix.
        current_line += 1

    stdscr.refresh()
    pad.refresh(0, 0, 1, consts.INDENT, h - 2, w - consts.INDENT)
    


def complete_path(text, state):
    return (glob.glob(os.path.expanduser(text) + "*") + [None])[state]


def get_input(stdscr, current_dir):
    curses.echo()
    readline.set_completer_delims(" \t\n;")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete_path)

    h, w = stdscr.getmaxyx()

    input_win = curses.newwin(1, w - 45, h - 1, 0)
    input_win.keypad(1)

    current_input = ""
    while True:
        input_win.clear()
        input_win.addstr(0, 0, f"> {current_input}", curses.A_BOLD)
        input_win.refresh()

        try:
            char = input_win.getch()
        except KeyboardInterrupt:
            exit(0)
        if char == 219:
            exit(0)
        if char == ord("\n"):  # Enter key
            break
        elif char == ord("\t"):  # Tab key
            # Goofy autocomplete stuff

            # TODO: Make it so it can autocomplete a path that isn't the entire input
            # Example: path/to/file :m need/autocomplete/here   ignore the middle :m

            completions = glob.glob(os.path.join(
                current_dir, current_input) + "*")
            if len(completions) == 1:
                current_input = os.path.relpath(completions[0], current_dir)
            elif len(completions) > 1:
                common_prefix = os.path.commonprefix(completions)
                current_input = os.path.relpath(common_prefix, current_dir)
        elif char == curses.KEY_BACKSPACE or char == 127:
            current_input = current_input[:-1]
        elif 32 <= char <= 126:  # Printable characters
            current_input += chr(char)

    curses.noecho()
    return current_input


def format_files(directory, files):
    new = []
    for i in files:
        full_path = os.path.join(directory, i)
        if os.path.isdir(full_path):
            new.append(f"📂 {i}/")
        else:
            try:
                new.append(f"{emojis[os.path.splitext(i)[1]]} {i}")
            except KeyError:
                new.append(f"📄 {i}")

    new.sort(key=lambda x: (not x.startswith("📂 "), x))
    return new


def get_files(directory, see_hidden=False):
    if see_hidden:
        visible_files = os.listdir(directory)
    else:
        visible_files = [f for f in os.listdir(
            directory) if not f.startswith(".")]
    formatted_files = format_files(directory, visible_files)
    return formatted_files


def explorer(stdscr):
    logging.info("Starting explorer")

    current_dir = os.getcwd()
    h, w = stdscr.getmaxyx()
    see_hidden = False
    user_input = ""

    while True:
        files = get_files(current_dir, see_hidden)
        draw_menu(stdscr, files, current_dir, user_input)

        user_input = get_input(stdscr, current_dir)

        # All commands
        if user_input in [":quit", ":q"]:
            logging.info("Quitting")
            sys.exit(0)
        elif user_input in [":back", ":b", ".."]:
            current_dir = os.path.dirname(current_dir)
        elif user_input in [":hidden", ":h"]:
            see_hidden = not see_hidden

        elif user_input.startswith("$"):
            os.system(user_input[1:])  # Run command in subshell

        elif user_input in [":move", ":m", ":rename", ":r"]:
            try:
                command = user_input.split()
                source = os.path.join(current_dir, command[0])
                dest = os.path.join(current_dir, command[2])
                os.rename(source, dest)
                logging.info(f"Moved {source} to {dest}")
            except:
                logging.warning(f"Failed to move file from {source} to {dest}")

        elif user_input in [":delete", ":d", ":remove", ":rm"]:
            try:
                command = user_input.split()
                source = os.path.join(current_dir, command[0])
                if os.path.isdir(source):
                    rmtree(source)
                    logging.info(f"Deleted directory {source}")
                    continue
                else:
                    os.remove(source)
                    logging.info(f"Deleted file {source}")
            except:
                logging.warning(f"Failed to delete file {source}")

        else:
            full_path = os.path.join(current_dir, user_input)

            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    current_dir = full_path
                else:
                    os.system(f"xdg-open '{full_path}'")


def main():
    wrapper(explorer)


if __name__ == "__main__":
    main()
