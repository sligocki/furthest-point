import math

class Point:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __neg__(self):
    return Point(-self.x, -self.y, -self.z)

  def __sub__(self, other):
    return Point(self.x - other.x,
                 self.y - other.y,
                 self.z - other.z)

  def __div__(self, scalar):
    return Point(self.x / scalar,
                 self.y / scalar,
                 self.z / scalar)

  def length(self):
    return math.sqrt(self.x**2 + self.y**2 + self.z**2)

  def normalize(self):
    return self / self.length()

  def arc_dist(self, other):
    return math.acos(self.dot(other))

  def dot(self, other):
    return (self.x * other.x +
            self.y * other.y +
            self.z * other.z)

  def __repr__(self):
    return "(%r, %r, %r)" % (self.x, self.y, self.z)

def dist(p1, p2):
  return (p2 - p1).length()

def cross(p1, p2):
  return Point(p1.y * p2.z - p2.y * p1.z,
               p1.z * p2.x - p2.z * p1.x,
               p1.x * p2.y - p2.x * p1.y)

def antipodal_points(p1, p2, p3):
  """Given 3 points on a unit sphere (p1, p2, p3).
  Find the two (antipodal) points on the sphere which
  are the exact same distance from p1, p2 and p3."""
  # First we produce normal vecors to the planes going through the
  # perpedicular bisectors of p1-p2 and p1-p3.
  normal_p12 = p2 - p1
  normal_p13 = p3 - p1
  antipodal_vector = cross(normal_p12, normal_p13)
  res_p = antipodal_vector.normalize()
  return res_p, -res_p

def dist_set(x, ps):
  """dist from x to closest point in ps."""
  min_d = 3.
  for p in ps:
    min_d = min(min_d, x.arc_dist(p))
  return min_d

def extreme_point(ps):
  assert len(ps) >= 3
  best_point = None
  max_dist = 0
  for i in xrange(len(ps)):
    for j in xrange(i + 1, len(ps)):
      for k in xrange(j + 1, len(ps)):
        aps = antipodal_points(ps[i], ps[j], ps[k])
        for ap in aps:
          d = dist_set(ap, ps)
          if d > max_dist:
            best_point = ap
            max_dist = d
  return best_point, max_dist


def latlong2point(lat_d, long_d):
  lat = lat_d / 180. * math.pi
  long = long_d / 180. * math.pi
  return Point(math.cos(lat) * math.cos(long),
               math.cos(lat) * math.sin(long),
               math.sin(lat))

def point2latlong(p):
  lat  = math.asin(p.z)
  long = math.atan2(p.y / math.cos(lat),
                    p.x / math.cos(lat))
  return (lat  / math.pi * 180.,
          long / math.pi * 180.)


import sys
ps = []
for i in xrange(1, len(sys.argv), 2):
  lat = float(sys.argv[i])
  long = float(sys.argv[i+1])
  ps.append(latlong2point(lat, long))
x, d = extreme_point(ps)
print point2latlong(x), d * 6371
