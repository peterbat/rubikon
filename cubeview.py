import config
import cube
import view as view
import matrix, graphics3d

import curses, time, math, copy, random

class CubeView:

  def __init__(self, win, cube, tilesize, gapsize, origin, border_color = None, camera = None):
    
    self.color_pairs = { 'U' : curses.color_pair(1), \
                         'F' : curses.color_pair(2), \
                         'R' : curses.color_pair(3), \
                         'B' : curses.color_pair(4), \
                         'L' : curses.color_pair(5), \
                         'D' : curses.color_pair(6) }
    if camera is None:
      self.camera = { 'location': None,
                      'line_of_sight': None,
                      'parallel': None }
    else:
      self.camera = camera
    self.cube = cube
    self.origin = origin
    self.win = win
    self.pvc = None
    self.tilesize = tilesize
    self.gapsize = gapsize
    self.border_color = border_color
    self.init_poly_views(win, tilesize, gapsize, origin)
    self.update_camera(camera)

  def init_poly_views(self, win, tilesize, gapsize, origin, deltaz = 1.00):
#    def make_xz_tile(tile_center, tilesize):
#      radius = 0.5 * tilesize
#      n = 4
#      dtheta = 2.0 * math.pi / n
#      points = []
#      for i in range(n):
#        points.append([tile_center[0] - radius * math.cos(i * dtheta), \
#          tile_center[1], \
#          tile_center[2] + radius * math.sin(i * dtheta)])
#      return points

    def make_xz_tile(tile_center, tilesize):
      half = 0.5 * tilesize
      points = [[tile_center[0] - half, tile_center[1], tile_center[2] + half], \
                [tile_center[0] + half, tile_center[1], tile_center[2] + half], \
                [tile_center[0] + half, tile_center[1], tile_center[2] - half], \
                [tile_center[0] - half, tile_center[1], tile_center[2] - half]]
      return points

    def make_xy_tile(tile_center, tilesize):
      half = 0.5 * tilesize
      points = [[tile_center[0] - half, tile_center[1] - half, tile_center[2]], \
                [tile_center[0] + half, tile_center[1] - half, tile_center[2]], \
                [tile_center[0] + half, tile_center[1] + half, tile_center[2]], \
                [tile_center[0] - half, tile_center[1] + half, tile_center[2]]]
      return points

    def make_yz_tile(tile_center, tilesize):
      half = 0.5 * tilesize
      points = [[tile_center[0], tile_center[1] - half, tile_center[2] - half], \
                [tile_center[0], tile_center[1] - half, tile_center[2] + half], \
                [tile_center[0], tile_center[1] + half, tile_center[2] - half], \
                [tile_center[0], tile_center[1] + half, tile_center[2] + half]]
      return points

    def operate_on_list_of_tiles(trans, tile_list, origin):
      tile_list_copy = copy.deepcopy(tile_list)
      for i in range(len(tile_list_copy)):
        tile_list_copy[i] = trans.list_operate(tile_list_copy[i], origin)
      return tile_list_copy

    self.poly_views = []
    # make top face:
    # start at back left corner
    rotx = matrix.rotx(0.5 * math.pi)
    rotxi = matrix.rotx(-0.5 * math.pi)
    rotx2 = matrix.rotx(math.pi)
    rotz = matrix.rotz(0.5 * math.pi)
    rotz2 = matrix.rotz(math.pi)
    #roty = matrix.roty(0.5 * math.pi)
    #rotyi = matrix.roty(-0.5 * math.pi)

    tile_center = [origin[0] - tilesize - gapsize, \
                   origin[1] - 1.5 * tilesize - 2 * gapsize, \
                   origin[2] + tilesize + gapsize]

    # construct vertices for top face tile polygons
    top_points_list = []
    tile_points = make_xz_tile(tile_center, tilesize)
    top_points_list.append(list(tile_points))
    tile_points = matrix.translate_points(tile_points, [tilesize + gapsize, 0.0, 0.0])
    top_points_list.append(list(tile_points))
    tile_points = matrix.translate_points(tile_points, [tilesize + gapsize, 0.0, 0.0])
    top_points_list.append(list(tile_points))
    tile_points = matrix.translate_points(tile_points, [- 2 * (tilesize + gapsize), 0.0, -(tilesize + gapsize)])
    top_points_list.append(list(tile_points))
    tile_points = matrix.translate_points(tile_points, [tilesize + gapsize, 0.0, 0.0])
    top_points_list.append(list(tile_points))
    tile_points = matrix.translate_points(tile_points, [tilesize + gapsize, 0.0, 0.0])
    top_points_list.append(list(tile_points))
    tile_points = matrix.translate_points(tile_points, [- 2 * (tilesize + gapsize), 0.0, -(tilesize + gapsize)])
    top_points_list.append(list(tile_points))
    tile_points = matrix.translate_points(tile_points, [tilesize + gapsize, 0.0, 0.0])
    top_points_list.append(list(tile_points))
    tile_points = matrix.translate_points(tile_points, [tilesize + gapsize, 0.0, 0.0])
    top_points_list.append(list(tile_points))

    # construct other faces by copying and iteratively transforming top face tile polygons
    front_points_list = copy.deepcopy(top_points_list)
    front_points_list = operate_on_list_of_tiles(rotx, front_points_list, origin)
    bottom_points_list = copy.deepcopy(front_points_list)
    bottom_points_list = operate_on_list_of_tiles(rotx, bottom_points_list, origin)
    back_points_list = copy.deepcopy(bottom_points_list)
    back_points_list = operate_on_list_of_tiles(rotx, back_points_list, origin)
    back_points_list = operate_on_list_of_tiles(rotz2, back_points_list, origin)
    right_points_list = copy.deepcopy(top_points_list)
    right_points_list = operate_on_list_of_tiles(rotz, right_points_list, origin)
    right_points_list = operate_on_list_of_tiles(rotx, right_points_list, origin)
    left_points_list = copy.deepcopy(bottom_points_list)
    left_points_list = operate_on_list_of_tiles(rotz, left_points_list, origin)
    left_points_list = operate_on_list_of_tiles(rotxi, left_points_list, origin)

    facedict = { 'U': top_points_list, \
                 'F': front_points_list, \
                 'R': right_points_list, \
                 'B': back_points_list, \
                 'L': left_points_list, \
                 'D': bottom_points_list }

    self.pvc = view.PolyViewCollection([], win, origin, deltaz = 0.5, camera = self.camera)
    for face_name in ['U', 'F', 'R', 'B', 'L', 'D']:
      face = facedict[face_name]
      for points in face:
        if self.border_color == None:
          bc = self.color_pairs[face_name] # no border
        else:
          bc = self.border_color
        self.pvc.append(view.PolyView(win, graphics3d.Poly3d(points), deltaz = deltaz, \
                        border_color = bc, \
                        fill_color = self.color_pairs[face_name], \
                        char = ' '))

  def reset(self):
    self.cube.reset()
    self.__init__(self.win, self.cube, self.tilesize, self.gapsize, self.origin, self.border_color, self.camera)
    self.clear()
    self.display()

  def update_camera(self, camera):
    self.pvc.update_camera(camera)

  def get_trans_from_string(self, s):
    if s == "U" or s == "Y" or s == "UW":
      axis, theta = 'y', 0.5 * math.pi
    elif s == "U'" or s == "Y'" or s == "UW'":
      axis, theta = 'y', -0.5 * math.pi
    elif s == "U2" or s == "Y2":
      axis, theta = 'y', math.pi
    elif s == "F" or s == "Z" or s == "FW":
      axis, theta = 'z', 0.5 * math.pi
    elif s == "F'" or s == "Z'" or s == "FW'":
      axis, theta = 'z', -0.5 * math.pi
    elif s == "F2" or s == "Z2":
      axis, theta = 'z', math.pi
    elif s == "R" or s == "X" or s == "RW":
      axis, theta = 'x', -0.5 * math.pi
    elif s == "R'" or s == "X'" or s == "RW'":
      axis, theta = 'x', 0.5 * math.pi
    elif s == "R2" or s == "X2":
      axis, theta = 'x', -math.pi
    elif s == "B":
      axis, theta = 'z', -0.5 * math.pi
    elif s == "B'":
      axis, theta = 'z', 0.5 * math.pi
    elif s == "B2":
      axis, theta = 'z', -math.pi
    elif s == "L" or s == "LW":
      axis, theta = 'x', 0.5 * math.pi
    elif s == "L'" or s == "LW'":
      axis, theta = 'x', -0.5 * math.pi
    elif s == "L2":
      axis, theta = 'x', math.pi
    elif s == "D":
      axis, theta = 'y', -0.5 * math.pi
    elif s == "D'":
      axis, theta = 'y', 0.5 * math.pi
    elif s == "D2":
      axis, theta = 'y', -math.pi
    elif s == "M":
      axis, theta = 'x', 0.5 * math.pi
    elif s == "M'":
      axis, theta = 'x', -0.5 * math.pi
    elif s == "M2":
      axis, theta = 'x', math.pi
    elif s == "E":
      axis, theta = 'y', -0.5 * math.pi
    elif s == "E'":
      axis, theta = 'y', 0.5 * math.pi
    elif s == "E2":
      axis, theta = 'y', -math.pi
    elif s == "S":
      axis, theta = 'z', 0.5 * math.pi
    elif s == "S'":
      axis, theta = 'z', -0.5 * math.pi
    elif s == "S2":
      axis, theta = 'z', math.pi
    return axis, theta

  def set_cube(self, cube):
    self.cube = cube

  def print_face(self, face_name):
    win = self.windows[face_name]
    tiles = self.cube.faces[face_name].tiles
    for i in range(3):
      for j in range(3):
        facemap = self.cube.facemap
        tile = tiles[i][j]
        face = facemap[tile]
        cp = self.color_pairs[face]
        win.addstr(i, j*2, '  ', cp)

  def display(self):
#    for f in ['U', 'L', 'F', 'R', 'B', 'D']:
#      self.print_face(f)
#      self.windows[f].refresh()
    self.pvc.draw()
    self.win.refresh()

  def clear(self):
    self.pvc.erase()
    self.win.clear()

# DEBUG--------------------------------------------------------------
  def debug_animate_scramble(self, scramble, debug_focus, delay=0.000):
    scramble = scramble.upper()
    scramble_list = scramble.split()
    for s in scramble_list:
      affected_tiles = [debug_focus]
      axis, theta = self.get_trans_from_string(s)
      steps = 5
      self.pvc.animate_rotation(affected_tiles, axis, theta, steps, origin = self.origin)
      self.cube.transform_using_string(s)
# -------------------------------------------------------------------

  def animate_scramble(self, scramble, delay=0.000, steps_per_turn = None):
    if steps_per_turn == None:
      steps = config.STEPS_PER_TURN
    else:
      steps = steps_per_turn
    scramble = scramble.upper()
    scramble_list = scramble.split()
    for s in scramble_list:
      affected_tiles = self.cube.get_affected_tiles(s)
      axis, theta = self.get_trans_from_string(s)
      self.pvc.animate_rotation(affected_tiles, axis, theta, steps, origin = self.origin)
      self.cube.transform_using_string(s)
#    if len(scramble_list) < 2:
#      self.cube.transform(scramble_list[0])
#      self.display()
#    else:
#      self.cube.transform(scramble_list[0])
#      self.display()
#      for t in scramble_list[1:]:
#        self.sleep(delay)
#        self.cube.transform(t)
#        self.display()

  def animate_scramble_in_one_step(self, scramble, delay=0.000, steps_per_turn = 20):
    if steps_per_turn == None:
      steps = config.STEPS_PER_TURN
    else:
      steps = steps_per_turn
    scramble = scramble.upper()
    scramble_list = scramble.split()
    transform_dict = {}
    for s in scramble_list:
      affected_tiles = self.cube.get_affected_tiles(s)
      self.cube.transform_using_string(s)
      axis, theta = self.get_trans_from_string(s)
      axis = axis.lower()
      r = None
      if axis == 'x':
        r = matrix.rotx(theta)
      elif axis == 'y':
        r = matrix.roty(theta)
      elif axis == 'z':
        r = matrix.rotz(theta)
      if r == None:
        print "Error: rotation about invalid axis: ", axis
        return
      for t in affected_tiles:
        if t not in transform_dict.keys():
          transform_dict[t] = matrix.Matrix(list(r.data))
        else:
          transform_dict[t] = matrix.multiply(matrix.Matrix(list(r.data)), transform_dict[t])
    for tile in transform_dict.keys():
      total_transform = transform_dict[tile]
      axis, angle = matrix.get_axis_and_angle_from_rot(total_transform)
      dtheta = angle / steps
      transform_dict[tile] = matrix.rotv(axis, dtheta)
    for s in range(steps):
      self.pvc.erase()
      for tile in transform_dict.keys():
        self.pvc.views[tile].transform(transform_dict[tile], self.origin)
      self.display()
