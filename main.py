import curses

def _versions_menu(screen, version_list):
  y_pos = 0
  key = None
  cp = {
    True: curses.A_STANDOUT,
    False: curses.A_NORMAL
  }
  screen.keypad(1)
  while True:
    screen.clear()
    for i, version in enumerate(version_list):
      screen.addstr(i, 0, f"{i}: {version}", cp[i == y_pos])
    key = screen.getch()
    if key == ord('\n'):
      return version_list[y_pos]
    elif key == ord('j'):
      y_pos = (y_pos + 1) % len(version_list)
    elif key == ord('k'):
      y_pos = (y_pos - 1) % len(version_list)
    screen.refresh()


def main(screen):
  curses.start_color()
  lists = ['aaa', 'bbb', 'ccc', 'ddd']
  a = _versions_menu(screen, lists)
  screen.clear()
  screen.addstr(0, 0, a)
  screen.refresh()
  screen.getkey()

if __name__ == '__main__':
  curses.wrapper(main)