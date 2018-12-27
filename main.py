# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import json

from flask import Flask, render_template, request

import furthest_point


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def show_furthest_point():
  """Calculate furthest point from every point user enters."""
  # Load user data
  if 'latlongs_json' in request.values:
    latlongs = json.loads(request.values['latlongs_json'])
  else:
    latlongs = []

  if 'lat' in request.values and 'lng' in request.values:
    latlongs.append([float(request.values['lat']),
                     float(request.values['lng'])])
  latlongs_json = json.dumps(latlongs)

  # Convert from lat-long to 3d point on unit sphere.
  visited_points = []
  for (lat, long) in latlongs:
    visited_points.append(furthest_point.latlong2point(lat, long))

  try:
    # Find furthest point
    extreme_point, unscaled_dist = furthest_point.extreme_point(visited_points)

    # Convert these back into Human readable values.
    extreme_lat, extreme_long = furthest_point.point2latlong(extreme_point)
    distance_km = unscaled_dist * 6371  # Radius of Earth in kilometers.
  except:
    extreme_lat  = 0.0
    extreme_long = 0.0
    distance_km = 0.0

  return render_template('furthest_point.html',
                         furthest_lat  = extreme_lat,
                         furthest_long = extreme_long,
                         distance_km = distance_km,
                         visited_points_json = latlongs_json)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
