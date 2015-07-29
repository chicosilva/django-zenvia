import os,sys 
import django.core.handlers.wsgi 
apache_configuration = os.path.dirname(__file__) 
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path.append('/home/chicosilva/public/betaniasms/public_html/keepsms/')
sys.path.append('/home/chicosilva/public/betaniasms/public_html/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'keepsms.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()