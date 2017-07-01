import datetime
from .models import Collaborator

# User details pipeline
def custom_extras(backend,strategy, details, response, is_new=False, user=None, *args, **kwargs):
	print strategy.session_get('coords')