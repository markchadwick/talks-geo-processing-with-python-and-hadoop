import json
import sys

from shapely.geometry import mapping
from shapely import wkt


def _records():
  for line in open('./playgrounds'):
    area, rec = line.split('\t')
    rec =  json.loads(rec)
    rec['playground'] = wkt.loads(rec['playground'])

    yield float(area), rec

def _features():
  for area, rec in _records():
    yield {
      'type':       'Feature',
      'geometry':   mapping(rec['playground']),
      'properties': {
        'user':   'User %s' % (rec['user']),
        'area':   area,
      },
    }

def main(n):
  i = 0

  collection = {
    'type':     'FeatureCollection',
    'features': [],
  }
  for feature in _features():
    collection['features'].append(feature)

    i += 1
    if i == n:
      break

  json.dump(collection, sys.stdout)

if __name__ == '__main__':
  main(int(sys.argv[1]))
