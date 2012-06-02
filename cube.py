import sys

face_names = ['U', 'F', 'R', 'B', 'L', 'D']

class Face:

  def __init__(self):
    self.tiles = [ [-1, -1, -1], [-1, -1, -1], [-1, -1, -1] ]

  def __init__(self, tile_matrix):
    self.tiles = tile_matrix

  def get_row(self, m):
    return list(self.tiles[m])

  def get_row_reverse(self, m):
    tmp = list(self.tiles[m])
    tmp.reverse()
    return tmp

  def set_row(self, m, rowvec):
    self.tiles[m] = list(rowvec)

  def get_col(self, n):
    colvec = []
    for i in range(len(self.tiles)):
       colvec.append(self.tiles[i][n])
    return colvec

  def get_col_reverse(self, n):
    colvec = []
    for i in range(len(self.tiles)):
      colvec.append(self.tiles[len(self.tiles)-1-i][n])
    return colvec

  def set_col(self, n, colvec):
    for i in range(len(self.tiles)):
      self.tiles[i][n] = colvec[i]

  def set(self, tile_matrix):
    self.tiles = []
    for i in range(len(tile_matrix)):
      self.tiles.append(list(tile_matrix[i]))

  def print_face(self, facemap, colorscheme):
    for row in self.tiles:
      print str(colorscheme[facemap[row[0]]]) + \
            str(colorscheme[facemap[row[1]]]) + \
            str(colorscheme[facemap[row[2]]])

  def print_face_raw(self):
    for row in self.tiles:
      print str(row[0]) + ' ' + \
            str(row[1]) + ' ' + \
            str(row[2])

class Cube:

  def __init__(self):
    self.face0 = Face([ [0, 1, 2], [3, 4, 5], [6, 7, 8] ])
    self.face1 = Face([ [9, 10, 11], [12, 13, 14], [15, 16, 17] ])
    self.face2 = Face([ [18, 19, 20], [21, 22, 23], [24, 25, 26] ])
    self.face3 = Face([ [27, 28, 29], [30, 31, 32], [33, 34, 35] ])
    self.face4 = Face([ [36, 37, 38], [39, 40, 41], [42, 43, 44] ])
    self.face5 = Face([ [45, 46, 47], [48, 49, 50], [51, 52, 53] ])

    self.faces = { 'U' : self.face0, \
                   'F' : self.face1, \
                   'R' : self.face2, \
                   'B' : self.face3, \
                   'L' : self.face4, \
                   'D' : self.face5 }

    self.facemap = []
    for i in range(54):
      self.facemap.append(face_names[i/9])
  
 
  def print_faces(self, colorscheme):
    print
    for f in face_names:
      self.faces[f].print_face(self.facemap, colorscheme)
      print
  
  def print_faces_raw(self):
    print
    for f in face_names:
      self.faces[f].print_face_raw()
      print

  def print_cube(self, colorscheme):
    print
    # print the top face
    for i in range(3):
      sys.stdout.write(colorscheme["X"]*3)
      row = self.faces["U"].get_row(i)
      rowstr = colorscheme[self.facemap[row[0]]] + \
               colorscheme[self.facemap[row[1]]] + \
               colorscheme[self.facemap[row[2]]]
      print rowstr
    for i in range(3):
      rowstr = ''.join(map(lambda x: colorscheme[self.facemap[x]], \
                           self.faces["L"].get_row(i) + \
                           self.faces["F"].get_row(i) + \
                           self.faces["R"].get_row(i) + \
                           self.faces["B"].get_row(i)))
      print rowstr
    for i in range(3):
      sys.stdout.write(colorscheme["X"]*3)
      row = self.faces["D"].get_row(i)
      rowstr = colorscheme[self.facemap[row[0]]] + \
               colorscheme[self.facemap[row[1]]] + \
               colorscheme[self.facemap[row[2]]]
      print rowstr
    print

  def reset(self):
    self.face0.__init__([ [0, 1, 2], [3, 4, 5], [6, 7, 8] ])
    self.face1.__init__([ [9, 10, 11], [12, 13, 14], [15, 16, 17] ])
    self.face2.__init__([ [18, 19, 20], [21, 22, 23], [24, 25, 26] ])
    self.face3.__init__([ [27, 28, 29], [30, 31, 32], [33, 34, 35] ])
    self.face4.__init__([ [36, 37, 38], [39, 40, 41], [42, 43, 44] ])
    self.face5.__init__([ [45, 46, 47], [48, 49, 50], [51, 52, 53] ])

  def get_affected_tiles(self, trans):
    tiles = []
    if 'U' in trans:
      tiles.extend(self.faces['F'].get_row(0))
      tiles.extend(self.faces['R'].get_row(0))
      tiles.extend(self.faces['B'].get_row(0))
      tiles.extend(self.faces['L'].get_row(0))
      tiles.extend(self.faces['U'].get_row(0))
      tiles.extend(self.faces['U'].get_col(0))
      tiles.extend(self.faces['U'].get_row(2))
      tiles.extend(self.faces['U'].get_col(2))
      tiles.extend(self.faces['U'].get_row(1))
      if 'W' in trans:
        tiles.extend(self.faces['F'].get_row(1))
        tiles.extend(self.faces['R'].get_row(1))
        tiles.extend(self.faces['B'].get_row(1))
        tiles.extend(self.faces['L'].get_row(1))
    if 'F' in trans:
      tiles.extend(self.faces['U'].get_row(2))
      tiles.extend(self.faces['L'].get_col(2))
      tiles.extend(self.faces['D'].get_row(0))
      tiles.extend(self.faces['R'].get_col(0))
      tiles.extend(self.faces['F'].get_row(0))
      tiles.extend(self.faces['F'].get_col(0))
      tiles.extend(self.faces['F'].get_row(2))
      tiles.extend(self.faces['F'].get_col(2))
      tiles.extend(self.faces['F'].get_row(1))
      if 'W' in trans:
        tiles.extend(self.faces['U'].get_row(1))
        tiles.extend(self.faces['R'].get_col(1))
        tiles.extend(self.faces['D'].get_row(1))
        tiles.extend(self.faces['L'].get_col(1))
    if 'R' in trans:
      tiles.extend(self.faces['U'].get_col(2))
      tiles.extend(self.faces['F'].get_col(2))
      tiles.extend(self.faces['D'].get_col(2))
      tiles.extend(self.faces['B'].get_col(0))
      tiles.extend(self.faces['R'].get_row(0))
      tiles.extend(self.faces['R'].get_col(0))
      tiles.extend(self.faces['R'].get_row(2))
      tiles.extend(self.faces['R'].get_col(2))
      tiles.extend(self.faces['R'].get_row(1))
      if 'W' in trans:
        tiles.extend(self.faces['U'].get_col(1))
        tiles.extend(self.faces['F'].get_col(1))
        tiles.extend(self.faces['D'].get_col(1))
        tiles.extend(self.faces['B'].get_col(1))
    if 'B' in trans:
      tiles.extend(self.faces['U'].get_row(0))
      tiles.extend(self.faces['R'].get_col(2))
      tiles.extend(self.faces['D'].get_row(2))
      tiles.extend(self.faces['L'].get_col(0))
      tiles.extend(self.faces['B'].get_row(0))
      tiles.extend(self.faces['B'].get_col(0))
      tiles.extend(self.faces['B'].get_row(2))
      tiles.extend(self.faces['B'].get_col(2))
      tiles.extend(self.faces['B'].get_row(1))
    if 'L' in trans:
      tiles.extend(self.faces['U'].get_col(0))
      tiles.extend(self.faces['F'].get_col(0))
      tiles.extend(self.faces['D'].get_col(0))
      tiles.extend(self.faces['B'].get_col(2))
      tiles.extend(self.faces['L'].get_row(0))
      tiles.extend(self.faces['L'].get_col(0))
      tiles.extend(self.faces['L'].get_row(2))
      tiles.extend(self.faces['L'].get_col(2))
      tiles.extend(self.faces['L'].get_row(1))
      if 'W' in trans:
        tiles.extend(self.faces['U'].get_col(1))
        tiles.extend(self.faces['F'].get_col(1))
        tiles.extend(self.faces['D'].get_col(1))
        tiles.extend(self.faces['B'].get_col(1))
    if 'D' in trans:
      tiles.extend(self.faces['F'].get_row(2))
      tiles.extend(self.faces['R'].get_row(2))
      tiles.extend(self.faces['B'].get_row(2))
      tiles.extend(self.faces['L'].get_row(2))
      tiles.extend(self.faces['D'].get_row(0))
      tiles.extend(self.faces['D'].get_col(0))
      tiles.extend(self.faces['D'].get_row(2))
      tiles.extend(self.faces['D'].get_col(2))
      tiles.extend(self.faces['D'].get_row(1))
    if 'M' in trans:
      tiles.extend(self.faces['U'].get_col(1))
      tiles.extend(self.faces['F'].get_col(1))
      tiles.extend(self.faces['D'].get_col(1))
      tiles.extend(self.faces['B'].get_col(1))
    if 'E' in trans:
      tiles.extend(self.faces['F'].get_row(1))
      tiles.extend(self.faces['R'].get_row(1))
      tiles.extend(self.faces['B'].get_row(1))
      tiles.extend(self.faces['L'].get_row(1))
    if 'S' in trans:
      tiles.extend(self.faces['U'].get_row(1))
      tiles.extend(self.faces['R'].get_col(1))
      tiles.extend(self.faces['D'].get_row(1))
      tiles.extend(self.faces['L'].get_col(1))
    if ('X' in trans) or ('Y' in trans) or ('Z' in trans):
      tiles = range(54)
    tiles = list(set(tiles))
    return tiles

  def transform(self, trans, times=1):
    for i in range(times):
      if trans == "U":
        tmp_vec = self.faces['F'].get_row(0)
        self.faces['F'].set_row(0, self.faces['R'].get_row(0))
        self.faces['R'].set_row(0, self.faces['B'].get_row(0))
        self.faces['B'].set_row(0, self.faces['L'].get_row(0))
        self.faces['L'].set_row(0, tmp_vec)
        tmp_vec = self.faces['U'].get_row(0)
        self.faces['U'].set_row(0, self.faces['U'].get_col_reverse(0))
        self.faces['U'].set_col(0, self.faces['U'].get_row(2))
        self.faces['U'].set_row(2, self.faces['U'].get_col_reverse(2))
        self.faces['U'].set_col(2, tmp_vec)
      elif trans == "U'":
        self.transform("U", 3)
      elif trans == "U2":
        self.transform("U", 2)
      elif trans == "F":
        tmp_vec = self.faces['U'].get_row(2)
        self.faces['U'].set_row(2, self.faces['L'].get_col_reverse(2))
        self.faces['L'].set_col(2, self.faces['D'].get_row(0))
        self.faces['D'].set_row(0, self.faces['R'].get_col_reverse(0))
        self.faces['R'].set_col(0, tmp_vec)
        tmp_vec = self.faces['F'].get_row(0)
        self.faces['F'].set_row(0, self.faces['F'].get_col_reverse(0))
        self.faces['F'].set_col(0, self.faces['F'].get_row(2))
        self.faces['F'].set_row(2, self.faces['F'].get_col_reverse(2))
        self.faces['F'].set_col(2, tmp_vec)
      elif trans == "F'":
        self.transform("F", 3)
      elif trans == "F2":
        self.transform("F", 2)
      elif trans == "R":
        tmp_vec = self.faces['U'].get_col_reverse(2)
        self.faces['U'].set_col(2, self.faces['F'].get_col(2))
        self.faces['F'].set_col(2, self.faces['D'].get_col(2))
        self.faces['D'].set_col(2, self.faces['B'].get_col_reverse(0))
        self.faces['B'].set_col(0, tmp_vec)
        tmp_vec = self.faces['R'].get_row(0)
        self.faces['R'].set_row(0, self.faces['R'].get_col_reverse(0))
        self.faces['R'].set_col(0, self.faces['R'].get_row(2))
        self.faces['R'].set_row(2, self.faces['R'].get_col_reverse(2))
        self.faces['R'].set_col(2, tmp_vec)
      elif trans == "R'":
        self.transform("R", 3)
      elif trans == "R2":
        self.transform("R", 2)
      elif trans == "B":
        tmp_vec = self.faces['U'].get_row_reverse(0)
        self.faces['U'].set_row(0, self.faces['R'].get_col(2))
        self.faces['R'].set_col(2, self.faces['D'].get_row_reverse(2))
        self.faces['D'].set_row(2, self.faces['L'].get_col(0))
        self.faces['L'].set_col(0, tmp_vec)
        tmp_vec = self.faces['B'].get_row(0)
        self.faces['B'].set_row(0, self.faces['B'].get_col_reverse(0))
        self.faces['B'].set_col(0, self.faces['B'].get_row(2))
        self.faces['B'].set_row(2, self.faces['B'].get_col_reverse(2))
        self.faces['B'].set_col(2, tmp_vec)
      elif trans == "B'":
        self.transform("B", 3)
      elif trans == "B2":
        self.transform("B", 2)
      elif trans == "L":
        tmp_vec = self.faces['U'].get_col(0)
        self.faces['U'].set_col(0, self.faces['B'].get_col_reverse(2))
        self.faces['B'].set_col(2, self.faces['D'].get_col_reverse(0))
        self.faces['D'].set_col(0, self.faces['F'].get_col(0))
        self.faces['F'].set_col(0, tmp_vec)
        tmp_vec = self.faces['L'].get_row(0)
        self.faces['L'].set_row(0, self.faces['L'].get_col_reverse(0))
        self.faces['L'].set_col(0, self.faces['L'].get_row(2))
        self.faces['L'].set_row(2, self.faces['L'].get_col_reverse(2))
        self.faces['L'].set_col(2, tmp_vec)
      elif trans == "L'":
        self.transform("L", 3)
      elif trans == "L2":
        self.transform("L", 2)
      elif trans == "D":
        tmp_vec = self.faces['F'].get_row(2)
        self.faces['F'].set_row(2, self.faces['L'].get_row(2))
        self.faces['L'].set_row(2, self.faces['B'].get_row(2))
        self.faces['B'].set_row(2, self.faces['R'].get_row(2))
        self.faces['R'].set_row(2, tmp_vec)
        tmp_vec = self.faces['D'].get_row(0)
        self.faces['D'].set_row(0, self.faces['D'].get_col_reverse(0))
        self.faces['D'].set_col(0, self.faces['D'].get_row(2))
        self.faces['D'].set_row(2, self.faces['D'].get_col_reverse(2))
        self.faces['D'].set_col(2, tmp_vec)
      elif trans == "D'":
        self.transform("D", 3)
      elif trans == "D2":
        self.transform("D", 2)
      elif trans == "M":
        tmp_vec = self.faces['U'].get_col(1)
        self.faces['U'].set_col(1, self.faces['B'].get_col_reverse(1))
        self.faces['B'].set_col(1, self.faces['D'].get_col_reverse(1))
        self.faces['D'].set_col(1, self.faces['F'].get_col(1))
        self.faces['F'].set_col(1, tmp_vec)
      elif trans == "M'":
        self.transform("M", 3)
      elif trans == "M2":
        self.transform("M", 2)
      elif trans == "E":
        tmp_vec = self.faces['F'].get_row(1)
        self.faces['F'].set_row(1, self.faces['L'].get_row(1))
        self.faces['L'].set_row(1, self.faces['B'].get_row(1))
        self.faces['B'].set_row(1, self.faces['R'].get_row(1))
        self.faces['R'].set_row(1, tmp_vec)
      elif trans == "E'":
        self.transform("E", 3)
      elif trans == "E2":
        self.transform("E", 2)
      elif trans == "S":
        tmp_vec = self.faces['U'].get_row(1)
        self.faces['U'].set_row(1, self.faces['L'].get_col_reverse(1))
        self.faces['L'].set_col(1, self.faces['D'].get_row(1))
        self.faces['D'].set_row(1, self.faces['R'].get_col_reverse(1))
        self.faces['R'].set_col(1, tmp_vec)
      elif trans == "S'":
        self.transform("S", 3)
      elif trans == "S2":
        self.transform("S", 2)
      elif trans == "RW":
        self.transform("M'")
        self.transform("R")
      elif trans == "RW'":
        self.transform("RW", 3)
      elif trans == "LW":
        self.transform("M")
        self.transform("L")
      elif trans == "LW'":
        self.transform("LW", 3)
      elif trans == "UW":
        self.transform("E")
        self.transform("U")
      elif trans == "UW'":
        self.transform("UW", 3)
      elif trans == "FW":
        self.transform("F")
        self.transform("S")
      elif trans == "FW'":
        self.transform("FW", 3)
      elif trans == "X":
        self.transform("R")
        self.transform("M'")
        self.transform("L'")
      elif trans == "X'":
        self.transform("X", 3)
      elif trans == "X2":
        self.transform("X", 2)
      elif trans == "Y":
        self.transform("U")
        self.transform("E'")
        self.transform("D'")
      elif trans == "Y'":
        self.transform("Y", 3)
      elif trans == "Y2":
        self.transform("Y", 2)
      elif trans == "Z":
        self.transform("F")
        self.transform("S")
        self.transform("B'")
      elif trans == "Z'":
        self.transform("Z", 3)
      elif trans == "Z2":
        self.transform("Z", 2)

  def transform_using_string(self, s):
    s = s.upper()
    for t in s.split():
      self.transform(t)

  def is_solved(self):
    for f in self.faces.values():
      if len(set([int(t/9) for row in f.tiles for t in row])) > 1:
        return False
    return True
#      old_face = None
#      for t in [t for row in f.tiles for t in row]:
#        if old_face == None:
#          old_face = int(t/9)
#          continue
#        elif int(t/9) != old_face:
#          return False
#      return True
