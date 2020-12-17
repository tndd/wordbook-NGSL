import curses
import random

from repository import VersionReository, WordRepository, TestCategory

def _versions_menu(screen, version_repository):
  versions = version_repository.get_versions()
  y_pos = 0
  key = None
  cp = {
    True: curses.A_STANDOUT,
    False: curses.A_NORMAL
  }
  screen.keypad(True)
  while True:
    screen.clear()
    height, width = screen.getmaxyx()
    screen.addstr(0, 0, f"idx\tname\tid", curses.A_ITALIC)
    for i, version in enumerate(versions):
      screen.addstr(i + 1, 0, f"{i}\t{version.name}\t{version.id}", cp[i == y_pos])
    screen.addstr(height-2, 0, "[j]: down, [j]: up, [enter]: select")
    screen.addstr(height-1, 0, "[c]: create new test,[i]: Inherit test, [r]: review test")
    key = screen.getch()
    if key == ord('\n'):
      return versions[y_pos]
    elif key == ord('j'):
      y_pos = (y_pos + 1) % len(versions)
    elif key == ord('k'):
      y_pos = (y_pos - 1) % len(versions)
    elif key == ord('c'):
      _create_new_version(screen, version_repository)
      versions = version_repository.get_versions()
    elif key == ord('i'):
      _create_child_version(screen, versions[y_pos], version_repository)
      versions = version_repository.get_versions()

def _create_child_version(screen, version, version_repository):
  screen.clear()
  screen.addstr(0, 0, f'Source name:\t{version.name}', curses.A_DIM)
  screen.addstr(1, 0, f'Id:\t\t{version.id}', curses.A_DIM)
  screen.addstr(3, 0, "Input be inherited test name: ")
  curses.echo()
  test_name = screen.getstr().decode(encoding="utf-8")
  curses.noecho()
  screen.clear()
  created_version = version_repository.create_child_version(version, test_name)
  screen.addstr(0, 0, f"Created hereditary test!: {created_version.name}")
  screen.addstr(1, 0, f"Version ID: {created_version.id}")
  screen.getch()
  return created_version

def _create_new_version(screen, version_repository):
  screen.clear()
  screen.addstr(0, 0, "Create new test.")
  screen.addstr(1, 0, "Input name: ")
  curses.echo()
  # Test name
  name = screen.getstr().decode(encoding="utf-8")
  screen.addstr(2, 0, "Select test category. [1]ngsl, [2]nawl: [3]bsl, [4]tsl: ")
  curses.noecho()
  # Select test category
  while True:
    key = screen.getch()
    if key == ord('1'):
      category = TestCategory.NGLS
      break
    elif key == ord('2'):
      category = TestCategory.NAWL
      break
    elif key == ord('3'):
      category = TestCategory.BSL
      break
    elif key == ord('4'):
      category = TestCategory.TSL
      break
  screen.clear()
  created_version = version_repository.create_version(name, category)
  screen.addstr(0, 0, f"NEW TEST IS CREATED!")
  screen.addstr(1, 0, f"Name\t{created_version.name}")
  screen.addstr(2, 0, f"Version ID\t{created_version.id}")
  screen.addstr(3, 0, f"Test category\t{created_version.category.name}")
  screen.getch()
  return created_version


def _test_loop(screen, word_repository):
  words = word_repository.get_words_unanswered()
  random.shuffle(words)
  for i, word in enumerate(words):
    screen.clear()
    screen.addstr(0, 0, "[<-]: I didn't know, [->]: I knew", curses.A_DIM)
    screen.addstr(1, 0, f"Remains: {len(words) - i}", curses.A_DIM)
    screen.addstr(3, 0, word.english, curses.A_BOLD)
    screen.getch()
    screen.addstr(5, 0, word.translation)
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
  version = _versions_menu(screen, vr)
  wr = WordRepository(version)
  _test_loop(screen, wr)
  screen.addstr(0, 0, 'Complete Test!')
  screen.getkey()

if __name__ == '__main__':
  curses.wrapper(main)