from pyramid.security import unauthenticated_userid

from auth_app.models import Session, User


def request_user(request):
    """ config.add_request_method(request_user, "user", reify=True) """
    user_id = unauthenticated_userid(request)
    if user_id is not None:
        user = Session.query(User).filter_by(user_id=user_id).first()
        return user
    else:
        return None
