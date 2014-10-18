import flaq import login_manager
from flaq.models.user import User

@login_manager.request_loader
def load_user_from_request(request):
    auth_key = request.headers.get('Authentication-Token')
    if auth_key:
        try:
            auth_key = base64.b64decode(auth_key)
        except TypeError:
            pass
        user = User.get_by_authkey(auth_key)
        if user:
            return user
    return None