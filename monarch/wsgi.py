from werkzeug.contrib.fixers import ProxyFix

from monarch.app import create_app

application = create_app("monarch")
application.wsgi_app = ProxyFix(application.wsgi_app)
