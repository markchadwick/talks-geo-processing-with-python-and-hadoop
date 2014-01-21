from mrjob.job import MRJob
from shapely.geometry import Point
from shapely.ops import cascaded_union


UNKNOWN_LOCATION = '00000000000000000000000000000000'
BUFFER = 0.5


class UserPlaygrounds(MRJob):

  def mapper(self, _, line):
    parts = line.split('\t')
    if len(parts) != 5 or parts[-1] == UNKNOWN_LOCATION or not parts[-1]:
      return

    uid, ts, lat, lng, loc = parts
    try:
      lat, lng = float(lat), float(lng)
      yield uid, (lng, lat)
    except:
      import sys
      sys.stderr.write('- ' * 30)
      sys.stderr.write('\n')
      sys.stderr.write('line: %r, parts %r' % (line, parts))
      sys.stderr.write('\n')
      sys.stderr.write('- ' * 30)
      sys.stderr.write('\n')
      raise

  def reducer(self, uid, locs):
    polys      = self._locs_to_polys(locs)
    playground = cascaded_union(list(polys))

    yield playground.area, {
      'user': uid,
      'playground': playground.wkt,
    }

  def _locs_to_polys(self, locs):
    for lng, lat in locs:
      yield Point(lng, lat).buffer(BUFFER)


if __name__ == '__main__':
  UserPlaygrounds.run()
