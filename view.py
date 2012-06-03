import config
from graphics2d import *
from graphics3d import *
import matrix
import curses
import time

def project_to_window(win, vec, deltaz = None, location = None, line_of_sight = None, parallel = None):
  maxy, maxx = win.getmaxyx()
  centery, centerx = int(maxy/2), int(maxx/2)
  if location == None or line_of_sight == None or parallel == None:
    persp_vec = perspective(vec, deltaz = deltaz)
  else:
    persp_vec = camera_transform(location, line_of_sight, parallel, deltaz, vec)
  # virtual 3d screen <----> real screen
  #    1 : 1          <---->   maxy : maxy
  # (most terminals are wider than they are tall)
  win_vec = [int(maxy * persp_vec[0]), int(maxy * persp_vec[1])]
  win_vec = stretch(win_vec)
  win_vec = [centerx + win_vec[0], centery + win_vec[1]]
  return win_vec

def project_points_to_window(win, points, deltaz = None, location = None, line_of_sight = None, parallel = None):
  win_points = []
  for p in points:
    win_point = project_to_window(win, p, deltaz = deltaz, location = location, \
      line_of_sight = line_of_sight, parallel = parallel)
    win_points.append(win_point)
  return win_points

class PolyView:

  def __init__(self, win, poly3d, deltaz = None, border_color = None, fill_color = None, char = None, camera = None):
    self.win = win
    self.poly3d = poly3d
    self.deltaz = deltaz
    if camera is None:
      self.camera = { 'location': None, 'line_of_sight': None, 'parallel': None, 'deltaz': None }
    else:
      self.camera = camera
    if char == None:
      self.char = graphics2d.DEFAULT_CHAR
    else:
      self.char = char
    self.poly2d = ConvexPoly(project_points_to_window(win, poly3d.vertices, deltaz, \
      self.camera['location'], self.camera['line_of_sight'], self.camera['parallel']), \
      self.char, border_color, fill_color)
    self.border_color = border_color
    self.fill_color = fill_color

  def update_window_projection(self, camera = None):
    if camera is not None:
      self.camera = camera
    self.poly2d.vertices = project_points_to_window(self.win, self.poly3d.vertices, self.deltaz, \
      self.camera['location'], self.camera['line_of_sight'], self.camera['parallel'])

  def transform(self, trans, origin = None):
    self.poly3d.vertices = [trans.operate(v, origin) for v in self.poly3d.vertices]
    self.update_window_projection()

  def draw(self):
    self.poly2d.fill(self.win)
    self.poly2d.draw(self.win)

  def erase(self):
    self.poly2d.erase_fill(self.win)
  
  def compute_centroid(self):
    xcentroid = sum([v[0] for v in self.poly3d.vertices]) / len(self.poly3d.vertices)
    ycentroid = sum([v[1] for v in self.poly3d.vertices]) / len(self.poly3d.vertices)
    zcentroid = sum([v[2] for v in self.poly3d.vertices]) / len(self.poly3d.vertices)
    return (xcentroid, ycentroid, zcentroid)

  def translate(self, displacement):
    self.poly3d.vertices = matrix.translate_points(self.poly3d.vertices, displacement)

  def update_camera(self, camera):
    self.camera = camera
    self.update_window_projection()

class PolyViewCollection:

  def __init__(self, polygon_views, win = None, origin = None, deltaz = None, camera = None):
    self.views = polygon_views
    self.win = win
    self.origin = origin
    self.deltaz = deltaz
    if camera is None:
      self.camera = {'location': None, 'line_of_sight': None, 'parallel': None}
    else:
      self.camera = camera

  def __z_compare(self, polyview1, polyview2):
    if self.camera == None:
      centroidz1 = sum([v[2] for v in polyview1.poly3d.vertices]) / len(polyview1.poly3d.vertices)
      centroidz2 = sum([v[2] for v in polyview2.poly3d.vertices]) / len(polyview2.poly3d.vertices)
    else:
      los = self.camera['line_of_sight']
      centroidz1 = sum([matrix.dot(v, los) for v in polyview1.poly3d.vertices]) / len(polyview1.poly3d.vertices)
      centroidz2 = sum([matrix.dot(v, los) for v in polyview2.poly3d.vertices]) / len(polyview2.poly3d.vertices)
    if centroidz1 < centroidz2:
      return -1
    elif centroidz1 == centroidz2:
      return 0
    elif centroidz1 > centroidz2:
      return 1

  def update_window_projections(self):
    for view in self.views:
      view.update_window_projection(self.camera)

  def transform(self, trans, origin = None):
    for view in self.views:
      view.transform(trans, origin)

  def transform_subset(self, subset_indices, trans, origin = None):
    for i in subset_indices:
      self.views[i].transform(trans, origin)

  def translate(self, displacement):
    for view in self.views:
      view.poly3d.vertices = matrix.translate_points(view.poly3d.vertices, displacement)

  def update_camera(self, camera):
    self.camera = camera
    self.erase()
    self.update_window_projections()
    self.draw()
    self.win.refresh()

  def __sort_views_by_z(self):
    #self.views.sort(cmp = self.__z_compare, reverse = True)
    return sorted(self.views, cmp = self.__z_compare, reverse = True)

  def append(self, polyview):
    self.views.append(polyview)

  def draw(self):
    sorted_views = self.__sort_views_by_z()
    for view in sorted_views:
      view.draw()

  def erase(self):
    for view in self.views:
      view.erase()

  def animate_rotation(self, view_subset, axis, theta, steps, origin = None, delay = 0.001):
    dtheta = theta / steps
    rot = None
    axis = axis.lower()
    if axis == 'x':
      rot = matrix.rotx(dtheta)
    elif axis == 'y':
      rot = matrix.roty(dtheta)
    elif axis == 'z':
      rot = matrix.rotz(dtheta)
    run_already = True
    for i in range(steps):
      if run_already:
        self.erase()
      self.transform_subset(view_subset, rot, origin)
      self.draw()
      self.win.refresh()
      if i < (steps - 1):
        time.sleep(delay)
      run_already = True

  def animate_explosion(self, delay = 0.000):
    import random
    rotation_list = []
    dr_list = []
    bulk_velocity = [random.gauss(0.0, 0.2), random.gauss(0.0, 0.2), 12.0 * abs(random.gauss(0.0, 0.1))]
    bv_norm = math.sqrt(sum([bvi**2 for bvi in bulk_velocity]))
    bulk_velocity = [bvi / bv_norm * 0.2 for bvi in bulk_velocity]
    dtheta = 0.04 * 2.0 * math.pi
    numsteps = 200
    
    for v in self.views:
      centroid = v.compute_centroid()
      displacement = [centroid[0] - self.origin[0], centroid[1] - self.origin[1], centroid[2] - self.origin[2]]
      norm = math.sqrt(sum([di**2 for di in displacement]))
      orientation = [di / norm for di in displacement]
      speed = 0.1 * random.random()
      dr = [speed * ori for ori in orientation]
      dr = [dr[i] + bulk_velocity[i] for i in range(len(dr))]
      dr_list.append(dr)
      rotvec = [random.random(), random.random(), random.random()]
      rotation_list.append(matrix.rotv(rotvec, dtheta + random.gauss(0.0, 0.1)))

    for i in range(numsteps):
      self.erase()
      for v in range(len(self.views)):
        centroid = self.views[v].compute_centroid()
        self.views[v].transform(rotation_list[v], origin = centroid)
        self.views[v].translate(dr_list[v])
      self.draw()
      self.win.refresh()
      time.sleep(delay)

  def animate_beamup(self, delay = 0.000):
    steps = 50
    dy = 0.15
    dtheta = 2.0 * math.pi / 100.0
    rot = matrix.roty(-dtheta)
    for s in range(steps):
      self.erase()
      for v in self.views:
        v.transform(rot, self.origin)
        v.translate([0.0, -dy, 0.0])
      self.draw()
      self.win.refresh()
      time.sleep(delay)

#
# SET UP CURSES
#
def set_up_curses(screen):
  curses.noecho()
  curses.cbreak()
  screen.keypad(1)
  screen.nodelay(1)
  curses.start_color()
  curses.curs_set(0)
 
#
# CLEAN UP AND EXIT CURSES
#
def clean_up_and_exit(screen):
  curses.curs_set(1)
  curses.nocbreak(); screen.nodelay(0); screen.keypad(0); curses.echo(); curses.endwin()

#
# TEST FUNCTION
#
def test_view(screen):
  set_up_curses(screen)
  if curses.can_change_color():
    curses.init_color(curses.COLOR_MAGENTA, 1000, 549, 0)
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
  curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
  curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
  curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
  curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)
  curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
  curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)

  points1 = [[-1.0, 1.0, 3.5], \
            [1.0, 1.0, 3.5], \
            [1.0, -1.0, 3.5], \
            [-1.0, -1.0, 3.5]]
  points2 = [[1.5, 1.0, 4.0], \
             [1.5, 1.0, 6.0], \
             [1.5, -1.0, 6.0], \
             [1.5, -1.0, 4.0]]
  points3 = [[1.0, 1.0, 6.5], \
             [-1.0, 1.0, 6.5], \
             [-1.0, -1.0, 6.5], \
             [1.0, -1.0, 6.5]]
  points4 = [[-1.5, 1.0, 6.0], \
             [-1.5, 1.0, 4.0], \
             [-1.5, -1.0, 4.0], \
             [-1.5, -1.0, 6.0]]
  points5 = [[-1.0, 1.5, 4.0], \
             [1.0, 1.5, 4.0], \
             [1.0, 1.5, 6.0], \
             [-1.0, 1.5, 6.0]]
  points6 = [[-1.0, -1.5, 4.0],
             [1.0, -1.5, 4.0],
             [1.0, -1.5, 6.0],
             [-1.0, -1.5, 6.0]]
  points_list = [points1, points2, points3, points4, points5, points6]
  polygons = [Poly3d(points) for points in points_list]
  polygon_views = [PolyView(screen, polygons[i], deltaz = 1.0, border_color = curses.color_pair(i+1), fill_color = curses.color_pair(i+1)) for i in range(6)]
  pvc = PolyViewCollection(polygon_views, screen)
  thetasteps = 100
  dtheta = 2.0 * math.pi / thetasteps
  #rot = matrix.rotz(dtheta)
  rot = matrix.rotv([1.0, 0.5, 0.0], dtheta)
  origin = [0.0, 0.0, 5.0]
  run_already = None
  delay = 0.005
  while True:
    if run_already is not None:
      pvc.erase()
    pvc.transform(rot, origin)
    pvc.draw()
    screen.refresh()
    time.sleep(delay)
    c = screen.getch()
    if c != -1 and c <= 255:
      if chr(c) == 'q':
        break
      elif chr(c) == 'j':
        pvc.translate([0.0, 0.0, -0.5])
        origin = matrix.translate_point(origin, [0.0, 0.0, -0.5])
      elif chr(c) == 'k':
        pvc.translate([0.0, 0.0, +0.5])
        origin = matrix.translate_point(origin, [0.0, 0.0, +0.5])
      elif chr(c) == 'h':
        delay += 0.005
      elif chr(c) == 'l':
        delay -= 0.005
        if delay < 0.0:
          delay = 0.00
      elif chr(c) == 'p':
        while screen.getch() == -1:
          pass
    run_already = True
  clean_up_and_exit(screen)

#
# MAIN BLOCK
#
if __name__ == '__main__':
  curses.wrapper(test_view)
