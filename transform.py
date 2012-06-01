import matrix, math

DEFAULT_FOV = 2.0 * math.pi / 3.0

def deltaz_from_fov(fov):
  return math.cot(fov / 2.0)

def stretch(point, vert_stretch = 1.0, horiz_stretch = 2.0):
  return (point[0]*vert_stretch, point[1]*horiz_stretch)

def perspective(point, fov = DEFAULT_FOV):
  deltaz = deltaz_from_fov(fov)
  phi = math.atan2(point[1] / point[0])
  r0 = math.sqrt(point[0]**2 + point[1]**2)
  r = r0 * deltaz / math.abs(point[2])
  x = r * math.cos(phi)
  y = r * math.sin(phi)
