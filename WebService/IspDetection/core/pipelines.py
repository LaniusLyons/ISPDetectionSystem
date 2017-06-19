import datetime
from .models import Collaborator

# User details pipeline
def user_details(strategy, details, response, is_new=False, user=None, *args, **kwargs):
	if user and is_new:
		changed = False
		protected = strategy.setting('PROTECTED_USER_FIELDS',[])
		keep = ('username','pk','id','email') + tuple(protected)

		for name, value in details.items():
			if name not in keep and hasattr(user,name):
				if value and value != getattr(user,name,None):
					try:
						setattr(user, name, value)
						changed = True
					except AttributeError:
						pass

		if changed:
			strategy.storage.user.changed(user)