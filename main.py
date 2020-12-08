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

def _test_loop(screen, word_repository):
  words = word_repository.get_words()
  for word in words:
    screen.clear()
    screen.addstr(0, 0, "[<-]: I didn't know, [->]: I knew", curses.A_DIM)
    screen.addstr(1, 0, word.word, curses.A_BOLD)
    screen.getch()
    screen.addstr(3, 0, word.translation)
    while True:
      key = screen.getch()
      if key == curses.KEY_LEFT:
        word_repository.regist_test_result(word, False)
        break
      elif key == curses.KEY_RIGHT:
        word_repository.regist_test_result(word, True)
        break
      else:
        continue
  screen.clear()

def main(screen):
  curses.start_color()
  vr = VersionReository()
  versions = vr.get_versions()
  version = _versions_menu(screen, versions)
  wr = WordRepository(version.id)
  _test_loop(screen, wr)
  screen.addstr(0, 0, 'Complete Test!')
  screen.getkey()

if __name__ == '__main__':
  curses.wrapper(main)