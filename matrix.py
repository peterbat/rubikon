import math

class Matrix:
  def __init__(self, a):
    if len(a) == 9:
      self.data = a
    else:
      print('ERROR: failed to initialize matrix with wrong dimensional data.')
  
  def lmultiply(self, b):
    data2 = [0] * 9
    data2[0] = self.data[0] * b.data[0] + self.data[1] * b.data[3] + self.data[2] * b.data[6]
    data2[1] = self.data[0] * b.data[1] + self.data[1] * b.data[4] + self.data[2] * b.data[7]
    data2[2] = self.data[0] * b.data[2] + self.data[1] * b.data[5] + self.data[2] * b.data[8]
    data2[3] = self.data[3] * b.data[0] + self.data[4] * b.data[3] + self.data[5] * b.data[6]
    data2[4] = self.data[3] * b.data[1] + self.data[4] * b.data[4] + self.data[5] * b.data[7]
    data2[5] = self.data[3] * b.data[2] + self.data[4] * b.data[5] + self.data[5] * b.data[8]
    data2[6] = self.data[6] * b.data[0] + self.data[7] * b.data[3] + self.data[8] * b.data[6]
    data2[7] = self.data[6] * b.data[1] + self.data[7] * b.data[4] + self.data[8] * b.data[7]
    data2[8] = self.data[6] * b.data[2] + self.data[7] * b.data[5] + self.data[8] * b.data[8]
    self.data = data2

  def operate(self, u, origin = None):
    if origin != None:
      w = [u[i] - origin[i] for i in range(len(origin))]
    else:
      w = u
    v = [0] * 3
    v[0] = self.data[0] * w[0] + self.data[1] * w[1] + self.data[2] * w[2]
    v[1] = self.data[3] * w[0] + self.data[4] * w[1] + self.data[5] * w[2]
    v[2] = self.data[6] * w[0] + self.data[7] * w[1] + self.data[8] * w[2]
    if origin != None:
      return [v[i] + origin[i] for i in range(len(origin))]
    else:
      return v

  def list_operate(self, ulist, origin = None):
    return [self.operate(u, origin) for u in ulist]

  def transpose(self):
    data2 = [0] * 9
    data2[0] = self.data[0]
    data2[1] = self.data[3]
    data2[2] = self.data[6]
    data2[3] = self.data[1]
    data2[4] = self.data[4]
    data2[5] = self.data[7]
    data2[6] = self.data[2]
    data2[7] = self.data[5]
    data2[8] = self.data[8]
    return Matrix(data2)

def dot(v1, v2):
  return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def cross(v1, v2):
  return [v1[1] * v2[2] - v1[2] * v2[1], \
          v1[2] * v2[0] - v1[0] * v2[2], \
          v1[0] * v2[1] - v1[1] * v2[0]]

def norm(v):
  return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def multiply(m1, m2):
  m3 = [0] * 9
  m3[0] = m1.data[0] * m2.data[0] + m1.data[1] * m2.data[3] + m1.data[2] * m2.data[6]
  m3[1] = m1.data[0] * m2.data[1] + m1.data[1] * m2.data[4] + m1.data[2] * m2.data[7]
  m3[2] = m1.data[0] * m2.data[2] + m1.data[1] * m2.data[5] + m1.data[2] * m2.data[8]
  m3[3] = m1.data[3] * m2.data[0] + m1.data[4] * m2.data[3] + m1.data[5] * m2.data[6]
  m3[4] = m1.data[3] * m2.data[1] + m1.data[4] * m2.data[4] + m1.data[5] * m2.data[7]
  m3[5] = m1.data[3] * m2.data[2] + m1.data[4] * m2.data[5] + m1.data[5] * m2.data[8]
  m3[6] = m1.data[6] * m2.data[0] + m1.data[7] * m2.data[3] + m1.data[8] * m2.data[6]
  m3[7] = m1.data[6] * m2.data[1] + m1.data[7] * m2.data[4] + m1.data[8] * m2.data[7]
  m3[8] = m1.data[6] * m2.data[2] + m1.data[7] * m2.data[5] + m1.data[8] * m2.data[8]
  return Matrix(m3)

def rotx(theta):
  m = [0] * 9
  m[0] = 1.
  m[1] = 0.
  m[2] = 0.
  m[3] = 0.
  m[4] = math.cos(theta)
  m[5] = -math.sin(theta)
  m[6] = 0.
  m[7] = math.sin(theta)
  m[8] = math.cos(theta)
  return Matrix(m)

def roty(theta):
  m = [0] * 9
  m[0] = math.cos(theta)
  m[1] = 0.
  m[2] = math.sin(theta)
  m[3] = 0.
  m[4] = 1
  m[5] = 0.
  m[6] = -math.sin(theta)
  m[7] = 0.
  m[8] = math.cos(theta)
  return Matrix(m)

def rotz(theta):
  m = [0] * 9
  m[0] = math.cos(theta)
  m[1] = -math.sin(theta)
  m[2] = 0.
  m[3] = math.sin(theta)
  m[4] = math.cos(theta)
  m[5] = 0.
  m[6] = 0.
  m[7] = 0.
  m[8] = 1.
  return Matrix(m)

def rotv(v, theta):
  t1 = rotz(math.acos(dot([v[0], v[1], 0.], [0., 1., 0.]) / math.sqrt(v[0]*v[0] + v[1]*v[1])))
  t2 = rotx(math.acos(dot(v, [0., 0., 1.]) / math.sqrt(dot(v, v))))
  T = multiply(t2, t1)
  r = rotz(theta)
  return multiply(T.transpose(), multiply(r, T))

def translate_point(p, displacement):
  return [p[i] + displacement[i] for i in range(len(p))]

def translate_points(points, displacement):
  return [translate_point(p, displacement) for p in points]

def test():
  print "z rotation of pi/3"
  r = rotz(math.pi / 3.)
  v = [1., 0., 1.]
  w = r.operate(v)
  print v
  print w
  print "y rotation of pi/3"
  r = roty(math.pi / 3.)
  v = [0., 1., 1.]
  w = r.operate(v)
  print v
  print w
  print "x rotation of pi/3"
  r = rotx(math.pi / 3.)
  v = [1., 1., 0.]
  w = r.operate(v)
  print v
  print w
  print "z rotation of -pi/3"
  r = rotz(-math.pi / 3.)
  v = [1., 0., 1.]
  w = r.operate(v)
  print v
  print w
  print "y rotation of -pi/3"
  r = roty(-math.pi / 3.)
  v = [0., 1., 1.]
  w = r.operate(v)
  print v
  print w
  print "x rotation of -pi/3"
  r = rotx(-math.pi / 3.)
  v = [1., 1., 0.]
  w = r.operate(v)
  print v
  print w
  #----
  v = [1./math.sqrt(3.), 1./math.sqrt(3.), 1./math.sqrt(3.)]
  print "rotation about a vector v = [%f, %f, %f]" % (v[0], v[1], v[2])
  w1 = [1., 0., 0.]
  r = rotv(v, 2.*math.pi/3.)
  w2 = r.operate(w1)
  print w1
  print w2
  print "a second time"
  w2 = r.operate(w2)
  print w2
  print "cross product"
  v1 = [1.0, 0.0, 0.0]
  v2 = [0.0, 1.0, 0.0]
  v3 = cross(v1, v2)
  print v1
  print v2
  print v3

if __name__ == '__main__':
  test()
