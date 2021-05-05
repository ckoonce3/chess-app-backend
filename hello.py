import bottle # i added this, not sure if you need to
from bottle import Bottle, run, response, request
import json

app = Bottle()

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


# Start the backend
run(app, host='localhost', port=8080, debug=True)

@app.route('/test', method=['OPTIONS', 'GET'])
@enable_cors
def getTest():
    return {'test': "Hello World"}

