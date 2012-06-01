import config
import matrix, math

def deltaz_from_fov(fov):
  return 1.0 / math.tan(fov / 2.0)

def stretch(point, vert_stretch = 1.0, horiz_stretch = 2.0):
  return [int(round(point[0]*horiz_stretch)), int(round(point[1]*vert_stretch))]

def perspective(point, fov = config.DEFAULT_FOV, deltaz = None):
  if deltaz == None:
    deltaz = deltaz_from_fov(fov)
  phi = math.atan2(point[1], point[0])
  r0 = math.sqrt(point[0]**2 + point[1]**2)
  r = r0 * deltaz / abs(point[2])
  x = r * math.cos(phi)
  y = r * math.sin(phi)
  return [x, y]

def camera_transform(location, line_of_sight, parallel, deltaz, point):
  r = [point[i] - location[i] for i in range(len(point))]
  dist_to_cam = matrix.dot(r, line_of_sight)
  horiz_coord = deltaz * matrix.dot(r, parallel) / dist_to_cam
  z = matrix.cross(parallel, line_of_sight)
  vert_coord = deltaz * matrix.dot(r, matrix.cross(line_of_sight, parallel)) / dist_to_cam
  return [horiz_coord, vert_coord]

def move_camera(camera, camera_control, origin, amount = None):
  location = camera['location']
  line_of_sight = camera['line_of_sight']
  parallel = camera['parallel']
  if camera_control in ['backward', 'forward']:
    if amount is None:
      amount = 0.25
    if camera_control == 'forward':
      location = [location[i] + amount * line_of_sight[i] for i in range(len(location))]
    elif camera_control == 'backward':
      location = [location[i] - amount * line_of_sight[i] for i in range(len(location))]
    camera['location'] = location
    return camera
  if amount is None:
    amount = 2.0 * math.pi / 100.0
  if camera_control == 'up':
    rot = matrix.rotv(parallel, -amount)
  elif camera_control == 'down':
    rot = matrix.rotv(parallel, amount)
  elif camera_control == 'left':
    rot = matrix.rotv(matrix.cross(parallel, line_of_sight), -amount)
  elif camera_control == 'right':
    rot = matrix.rotv(matrix.cross(parallel, line_of_sight), amount)
  line_of_sight = rot.operate(line_of_sight, origin = [0., 0., 0.])
  parallel = rot.operate(parallel, origin = [0., 0., 0.])
  location = rot.operate(location, origin = origin)
  camera = {'location': location, 'line_of_sight': line_of_sight, 'parallel': parallel}
  return camera

#
# POINT3D CLASS
#
class Point3d(list):
  def __init__(self, coords = None):
    if coords == None:
      self.data = [0.0, 0.0, 0.0]
      return
    if type(coords) == Point3d:
      self.data = Point3d[:]
      return
    if (len(coords) > 3) or (len(coords) < 1):
      print "ERROR: point must contain 3 and only 3 coordinates"
      return
    for i in range(len(coords)):
      if not (type(coords[i]) == float):
        if type(coords[i]) == int:
          coords[i] = float(coords[i])
        else:
          print "ERROR: value must be a real number"
          return
    self.data = list(coords)
  
  def __setitem__(self, key, value):
    if (not type(key) == int) and ((key > 2) or (key < 0)):
      print "ERROR: key must be an integer between 0 and 2"
      return
    if not type(value) == float:
      if type(value) == int:
        value = float(value)
      else:
        print "ERROR: value must be a real number"
        return
    self.data[key] = value

  def __getitem__(self, key):
    if not ((type(key) == int) and (key >= 0) and (key <= 2)):
      print "ERROR: key must be an integer between 0 and 2"
      return
    else:
      return self.data[key]

  def __getslice__(self, i, j):
    return self.data[i:j]

  def __setslice__(self, i, j, val):
    self.data[i:j] = val
  
  def __str__(self):
    return str(self.data)

class Poly3d:
  def __init__(self, vertices):
    self.vertices = vertices

def test_graphics3d():
  # test perspective transformation
  vec = [1.0, 1.0, 2.0]
  persp_vec = perspective(vec, deltaz = 1.0)
  print vec
  print persp_vec

if __name__ == '__main__':
  test_graphics3d()
