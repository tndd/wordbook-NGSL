import curses

from repository import VersionReository, WordRepository

def _versions_menu(screen, versions):
  y_pos = 0
  key = None
  cp = {
    True: curses.A_STANDOUT,
    False: curses.A_NORMAL
  }
  screen.keypad(True)
  while True:
    screen.clear()
    screen.addstr(0, 0, f"idx\tname\tremains\tid", curses.A_ITALIC)
    for i, version in enumerate(versions):
      screen.addstr(i + 1, 0, f"{i}\t{version.name}\t{version.remains}\t{version.id}", cp[i == y_pos])
    key = screen.getch()
    if key == ord('\n'):
      return versions[y_pos]
    elif key == ord('j'):
      y_pos = (y_pos + 1) % len(versions)
    elif key == ord('k'):
      y_pos = (y_pos - 1) % len(versions)
    screen.refresh()

def _test_loop(screen, word_repository):
  pass


def main(screen):
  curses.start_color()
  vr = VersionReository()
  versions = vr.get_versions()
  version = _versions_menu(screen, versions)
  wr = WordRepository(version.id)
  _test_loop(screen, wr)
  screen.clear()
  screen.addstr(0, 0, version.name)
  screen.refresh()
  screen.getkey()

if __name__ == '__main__':
  curses.wrapper(main)