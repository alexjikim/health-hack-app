from gaesessions import SessionMiddleware

from google.appengine.dist import use_library
use_library('django', '1.2')

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="89o21od1902ud1oi2dho891y2hduo1huh120d9181oihjkohd12098")
    return app
