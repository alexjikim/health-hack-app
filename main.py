import cgi
import datetime
import urllib
import urllib2
import wsgiref.handlers
import os
import logging
import time
import re
import base64

# local imports
import model
from persistence import get_tasks_for_patient


from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from google.appengine.dist import use_library
from google.appengine.api import images
from google.appengine.api import mail

from django.utils import simplejson as json

use_library('django', '1.2')

from gaesessions import get_current_session


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')



class JustAnotherHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')









def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/dummyHandler', JustAnotherHandler)
    
                                         ], debug=True)
    run_wsgi_app(application)




if __name__ == '__main__':
    main()




