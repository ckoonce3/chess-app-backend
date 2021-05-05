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

'''
    If you essentially copied the structure of A4 in COMP 521, you have
    to modify your ORM layer's Bottle routes.

    For example, originially I had this:
    
        @app.post('/login') 
            def login():
                < the code you made for login > 
                return json.dumps(some login thing)
            
    But I had to change it to this:
    
        @app.route('/login', method=['OPTIONS', 'POST']) 
            def login():
                < the code you made for login >   
                return json.dumps(some login thing)

'''
