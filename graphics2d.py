# graphics2d.py
#
# classes and functions for drawing 2D graphics to an ncurses window

import config
import curses, math
import random, string

#
# LINE CLASS
#
class Line2d:
  def __init__(self, vertices, char = None, color_pair = None):
    self.set_vertices(vertices)
    if char == None:
      self.set_char(config.DEFAULT_CHAR)
    else:
      self.set_char(char)
    if color_pair == None:
      self.set_color_pair(curses.color_pair(1))
    else:
      self.set_color_pair(color_pair)

  def set_vertices(self, vertices, color_pair = None):
    if len(vertices) == 2:
      self.vertices = vertices
    else:
      print "Error: line must be defined by only 2 vertices"

  def set_color_pair(self, cp):
    self.color_pair = cp

  def set_char(self, char = None):
    self.char = char

  def draw(self, win, color_pair = None):
    if color_pair == None:
      cp = self.color_pair
    else:
      cp = color_pair
    draw_line(self.vertices[0], self.vertices[1], win, self.char, cp)

  def erase(self, win):
    self.draw(win, curses.color_pair(0))
    #draw_line(self.vertices[0], self.vertices[1], win, self.char, curses.color_pair(0))

#
# DRAW LINE FUNCTION
#
def draw_line(pi, pf, win, char=config.DEFAULT_CHAR, color_pair=None, erase = None):
  ch = char
  maxy, maxx = win.getmaxyx()
  if color_pair == None:
    color_pair = curses.color_pair(1)
  xi = pi[0]
  yi = pi[1]
  xf = pf[0]
  yf = pf[1]
  dx = math.fabs(xf - xi)
  dy = math.fabs(yf - yi)
  if xi < xf:
    sx = 1
  else:
    sx = -1
  if yi < yf:
    sy = 1
  else:
    sy = -1
  err = dx - dy

  x = xi
  y = yi
  while True:
    if (y > 0 and y < maxy - 1 and x > 0 and x < maxx - 1):
    #if (y > 0 and y < maxy and x > 0 and x < maxx):
      if config.IN_THE_MATRIX and not erase:
        ch = random.choice(string.printable[:-6])
      else:
        ch = char
      win.addstr(y, x, ch, color_pair)
    if (x == xf and y == yf):# or not (y > 0 and y < maxy and x > 0 and x < maxx):
      break
    e2 = 2 * err
    if e2 > -dy:
      err = err - dy
      x = x + sx
    if e2 < dx:
      err = err + dx
      y = y + sy

#
# COMPUTE LINE FUNCTION
#
def compute_line(pi, pf):
  xi = pi[0]
  yi = pi[1]
  xf = pf[0]
  yf = pf[1]
  dx = math.fabs(xf - xi)
  dy = math.fabs(yf - yi)
  if xi < xf:
    sx = 1
  else:
    sx = -1
  if yi < yf:
    sy = 1
  else:
    sy = -1
  err = dx - dy

  x = xi
  y = yi
  points = []
  while True:
    points.append((x, y))
    if x == xf and y == yf:
      break
    e2 = 2 * err
    if e2 > -dy:
      err = err - dy
      x = x + sx
    if e2 < dx:
      err = err + dx
      y = y + sy

  return points

#
# CONVEX POLY CLASS
#
class ConvexPoly:
  def __init__(self, vertices, char = None, border_color = None, fill_color = None):
    self.vertices = vertices
    if char == None:
      self.set_char(DEFAULT_CHAR)
    else:
      self.set_char(char)
    if border_color == None:
      self.set_border_color(curses.color_pair(1))
    else:
      self.set_border_color(border_color)
    if fill_color == None:
      self.set_fill_color(curses.color_pair(1))
    else:
      self.set_fill_color(fill_color)

  def set_border_color(self, cp):
    self.border_color = cp

  def set_fill_color(self, cp):
    self.fill_color = cp

  def set_char(self, char = None):
    self.char = char

  def get_minmax_xy(self):
    xs = [v[0] for v in self.vertices]
    ys = [v[1] for v in self.vertices]
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)
    return (minx, maxx, miny, maxy)

  def is_on_screen(self, win):
    h, w = win.getmaxyx()
    minx, maxx, miny, maxy = self.get_minmax_xy()
    if (maxx > w) or (minx < 0) or (maxy > h) or (miny < 0):
      return False
    else:
      return True

  def fill(self, win, fill_color = None, char = None, erase = None):
    minx, maxx, miny, maxy = self.get_minmax_xy()
    winheight, winwidth = win.getmaxyx()
    if (maxx < 0) or (minx > winwidth) or (maxy < 0) or (miny > winheight):
      return
    if char == None:
      ch = self.char
    else:
      ch = char
    if fill_color == None:
      cp = self.fill_color
    else:
      cp = fill_color
    boundary_points = []
    boundary_segments = []
    for i in range(len(self.vertices)):
      if i == len(self.vertices) - 1:
        segment = compute_line(self.vertices[i], self.vertices[0])
      else:
        segment = compute_line(self.vertices[i], self.vertices[i + 1])
      boundary_segments.append(segment)
      boundary_points += segment
    y_vals = [p[1] for p in self.vertices]
    min_bound = min(y_vals)
    max_bound = max(y_vals)
    y_dict = {}
    for p in boundary_points:
      if p[0] in y_dict:
        y_dict[p[0]].append(p[1])
      else:
        y_dict[p[0]] = [p[1]]
    for y in y_dict:
      draw_line((y, min(y_dict[y])), (y, max(y_dict[y])), win, ch, cp, erase)

  def erase_fill(self, win):
    self.fill(win, curses.color_pair(0), char = ' ', erase = True)

  def draw(self, win, border_color = None, char = None):
    if char == None:
      ch = self.char
    else:
      ch = char
    if border_color == None:
      cp = self.border_color
    else:
      cp = border_color
    for i in range(len(self.vertices)):
      if i == len(self.vertices) - 1:
        draw_line(self.vertices[i], self.vertices[0], win, ch, cp)
      else:
        draw_line(self.vertices[i], self.vertices[i + 1], win, ch, cp)

  def erase(self, win):
    self.draw(win, curses.color_pair(0))
#
# TESTING FUNCTION
#
def test_graphics2d(screen):
  def wait_for_keypress():
    while True:
      if screen.getch() != -1:
        break

  def clean_up_and_exit(screen):
    curses.curs_set(1)
    curses.nocbreak(); screen.nodelay(0); screen.keypad(0); curses.echo(); curses.endwin()

  curses.noecho()
  curses.cbreak()
  screen.keypad(1)
  screen.nodelay(1)
  curses.start_color()
  curses.curs_set(0)

  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
  curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)

  poly1 = ConvexPoly([(1,1), (30,30), (50, 20)], ' ', curses.color_pair(1))
  poly1.draw(screen)
  screen.refresh()
  wait_for_keypress()

  poly2 = ConvexPoly([(1,60), (10, 80), (50, 70), (5, 55)], ' ', curses.color_pair(2))
  poly2.fill(screen)
  screen.refresh()
  wait_for_keypress()

  line1 = Line2d([(50, 50), (60, 80)], color_pair = curses.color_pair(2))
  line1.draw(screen)
  screen.refresh()
  wait_for_keypress()

  clean_up_and_exit(screen)

#
# MAIN BLOCK
#
if __name__ == '__main__':
  curses.wrapper(test_graphics2d)
