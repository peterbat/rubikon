import curses, time, random, sys, math
import config
import matrix, graphics3d

from cube import *
import scrambler
import cubeview

def is_nontrivial_move(scramble):
  for c in "UFRBLDMES":
    if c in scramble:
      return True
  return False

def switch_colors(blind):
  if blind:
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)
  else:
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)

def main(screen):
  # initialize terminal
  curses.noecho()
  curses.cbreak()
  screen.keypad(1)
  #screen.nodelay(1)
  screen.timeout(-1)
  curses.start_color()
  curses.curs_set(0)
  maxy, maxx = screen.getmaxyx()

  # initialize color pairs
  if curses.can_change_color():
    curses.init_color(curses.COLOR_MAGENTA, 1000, 549, 0)
    curses.init_color(curses.COLOR_CYAN, 200, 200, 200)

  if config.IN_THE_MATRIX:
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
  else:
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)


  scramble_len = 40
  tilesize = 1.0
  gapsize = 0.35
  origin = [0.0, 0.0, 7.5]
  #origin = [0.0, 0.0, 5.5]
  cam_location = [0.0, 0.0, 0.0]
  cam_line_of_sight = [0.0, 0.0, 1.0]
  cam_parallel = [1.0, 0.0, 0.0]
  camera = { 'location': cam_location, \
             'line_of_sight': cam_line_of_sight, \
             'parallel': cam_parallel }
  camera = graphics3d.move_camera(camera, 'up', origin, amount = math.pi / 5.0)
  height, width = screen.getmaxyx()
  c = Cube()
  scramble = scrambler.gen_scramble_str(scramble_len)
  #screen.addstr(0, 0, scramble)
  #screen.refresh()
  #c.transform_using_string(scramble)
  #view = cubeview.CubeView((2,4), c)
  view = cubeview.CubeView(screen, c, tilesize, gapsize, origin, border_color = curses.color_pair(7), camera = camera)
  view.update_camera(camera)
  view.display()
  time.sleep(1.0)
  #view.animate_scramble(scramble)
  keymap = { 'i' : "R", \
             'k' : "R'", \
             'e' : "L'", \
             'd' : "L", \
             'h' : "F", \
             'g' : "F'", \
             'j' : "U", \
             'f' : "U'", \
             'w' : "B", \
             'o' : "B'", \
             's' : "D", \
             'l' : "D'", \
             '8' : "M'", \
             ',' : "M", \
             '2' : "S'", \
             '0' : "S", \
             'z' : "E'", \
             '/' : "E", \
             'q' : "Z'", \
             'p' : "Z", \
             'a' : "Y'", \
             ';' : "Y", \
             'y' : "X", \
             'n' : "X'" }
  camera_controls = {'I': 'up', 'J': 'left', 'K': 'down', 'L': 'right', '*': 'forward', '<': 'backward'}
  if len(sys.argv) > 1 and sys.argv[1] == "blind":
    blind = True
  else:
    blind = False
  currently_blind = False
  no_keypress_yet = True
  no_nontrivial_keypress = True
  while True:
    if c.is_solved() and not no_keypress_yet:
      screen.addstr(1, 1, "SOLVED!")
      if blind and currently_blind:
        currently_blind = False
        switch_colors(currently_blind)
#      screen.refresh()
#      time.sleep(0.5)
#      view.pvc.animate_explosion()
#      screen.clear()
#      screen.addstr(maxy/2, maxx/2 - 10, "Congratulations! Hit any key to reset.")
#      while screen.getch() == -1:
#        pass
#      screen.clear()
      no_keypress_yet = True
      no_nontrivial_keypress = True
#      c.reset()
#      view.reset()
    else:
      screen.addstr(1, 1, "       ")
    T = -1
    while T == -1:
      T = screen.getch()
    no_keypress_yet = False
    if T == 27:
      clean_up_and_exit(screen)
    elif T == ord('`'):
      no_keypress_yet = True
      c.reset()
      view.reset()
    elif T == ord(']'):
      scramble = scrambler.gen_scramble_str(scramble_len)
      #c.transform_using_string(scramble)
      view.animate_scramble(scramble)
    elif chr(T) in keymap.keys():
      #affected_tiles = c.get_affected_tiles(str(T))
      #axis, theta = view.get_trans_from_string(str(T))
      #steps = 25
      #view.pvc.animate_rotation(affected_tiles, axis, theta, steps, origin = view.origin)
      #c.transform_using_string(keymap[chr(T)])
      #view.set_cube(c)
      if blind and no_nontrivial_keypress and is_nontrivial_move(keymap[chr(T)]):
        currently_blind = True
        switch_colors(currently_blind)
        no_nontrivial_keypress = False
      view.animate_scramble(keymap[chr(T)])
    elif chr(T) in camera_controls:
      camera = graphics3d.move_camera(camera, camera_controls[chr(T)], origin)
      view.update_camera(camera)
    elif T == ord('T'):
      view.animate_scramble("R U R' U' R' F R2 U' R' U' R U R' F'")
    elif T == ord('Y'):
      view.animate_scramble("F R U' R' U' R U R' F' R U R' U' R' F R F'")
    elif T == ord('}'):
      no_keypress_yet = True
      view.pvc.animate_explosion()
      screen.clear()
    # DEBUG-----------------------------------
#    elif T == ord('='):
#      if debug_focus < 53:
#        debug_focus += 1
#        disp_debug(debug_focus)
#    elif T == ord('-'):
#      if debug_focus > 0:
#        debug_focus -= 1
#        disp_debug(debug_focus)
#    elif chr(T) in debug_keymap.keys():
#      view.debug_animate_scramble(debug_keymap[chr(T)], debug_focus)
    # ----------------------------------------
    #view.set_cube(c)
    #view.display()

  # Clean up terminal before exiting...
  clean_up_and_exit(screen)

def clean_up_and_exit(screen):
  curses.curs_set(1)
  curses.nocbreak(); screen.nodelay(0); screen.keypad(0); curses.echo(); curses.endwin()
  sys.exit(1)

if __name__ == '__main__':
  curses.wrapper(main)
