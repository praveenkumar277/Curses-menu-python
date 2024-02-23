import curses

def main(stdscr):
    dir = ''
    def manage_menu_items(items):
        return items
    # Turn off cursor blinking
    curses.curs_set(0)

    # Disable automatic echoing of keys and line buffering
    curses.noecho()
    curses.cbreak()

    # Tell curses not to worry about cursor position when refreshing
    stdscr.leaveok(True)

    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()

    # Initialize colors
    curses.start_color()
    # Overwrite default colors
    curses.init_color(curses.COLOR_RED, 1000, 333, 333)  # Red
    curses.init_color(curses.COLOR_GREEN, 313, 980, 482)  # Green
    curses.init_color(curses.COLOR_YELLOW, 945, 980, 550)  # Yellow
    curses.init_color(curses.COLOR_BLUE, 738, 574, 972)  # Blue
    curses.init_color(curses.COLOR_MAGENTA, 1000, 474, 776)  # Magenta
    curses.init_color(curses.COLOR_CYAN, 545, 913, 992)  # Cyan
    curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)  # White
    curses.init_color(curses.COLOR_BLACK, 100, 100, 100)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # Create a window for the menu
    menu_win = curses.newwin(sh - 1, sw, 0, 0)  # Adjust height by 1 less than screen height

    # Enable keypad input for the menu window
    menu_win.keypad(True)

    # Define menu items with colors
    menu_items = [
        ["Option 1", curses.color_pair(1), 0, ''],
        ["Option 2", curses.color_pair(2), 0, ''],
        ["Option 3", curses.color_pair(3), 0, '']
        ]  # Example: 3 options with different colors

    # Highlight the first item by default
    selected_item = 0

    # Define variables for scrolling
    start_row = 0
    visible_rows = min(sh - 1, len(menu_items))  # Adjust for screen height

    # List to store selected options
    selected_options = []
    bar = curses.newwin(1, sw, sh - 1, 0)

    # Main loop
    while True:
        # Clear the menu window
        percent = (selected_item+1) * 100 // len(menu_items)
        menu_win.clear()
        bar.addstr(0, 0, dir)
        bar.addstr(0, sw-5, "{}%".format(percent))
        bar.refresh()


        # Display the visible menu items with colors
        for i in range(start_row, min(start_row + visible_rows, len(menu_items))):
            option_text, option_color, option_highlight, Type= menu_items[i]
            if i == selected_item:
                menu_win.addstr(i - start_row, 0,"> " + option_text, option_color | option_highlight)
            else:
                menu_win.addstr(i - start_row, 2, option_text, option_color | option_highlight)

        # Refresh the menu window
        menu_win.refresh()

        # Get user input
        key = menu_win.getch()

        # Handle user input
        if key == curses.KEY_UP:
            selected_item = max(0, selected_item - 1)
            if selected_item < start_row:
                start_row -= 1
                menu_win.refresh()  # Refresh menu window after scrolling
                percent = selected_item
        elif key == curses.KEY_DOWN:
            selected_item = min(len(menu_items) - 1, selected_item + 1)
            if selected_item >= start_row + visible_rows:
                start_row += 1
                menu_win.refresh()  # Refresh menu window after scrolling
        elif key == ord('q'):
            # If 'q' is pressed, create a new window at the last line and exit
            break
        elif key == curses.KEY_ENTER or key in [10, 13]:
            menu_items[selected_item][2] = 0 if menu_items[selected_item][2] !=0 else curses.A_UNDERLINE
            if selected_item not in selected_options:
                selected_options.append(selected_item)  # Add selected option to list
            else:
                selected_options.remove(selected_item)  # Remove if already selected
        elif key == curses.KEY_HOME:
            selected_item = 0
        elif key == curses.KEY_END:
            selected_item = len(menu_items)-1


    # Clean up
    curses.endwin()
    return selected_options

if __name__ == "__main__":
    print(curses.wrapper(main))
