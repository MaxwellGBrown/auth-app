from pyramid.view import view_config, view_defaults
import pyramid.httpexceptions as http
from pyramid.security import remember, forget

from auth_app.models import User


@view_config(route_name='index', renderer='index.mako')
def index(request):
    return {}


@view_config(route_name="home", renderer="home.mako",
             permission="authenticated")
def home(request):
    return {}


@view_defaults(route_name="login", renderer="login.mako")
class LoginViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name="logout")
    def logout(self):
        return http.HTTPFound(
            self.request.route_url('index'),
            headers=forget(self.request)
        )

    @view_config(request_method="GET")
    def get_login(self):
        return {}

    @view_config(request_method="POST")
    def post_login(self):
        try:
            user = User.one(email=self.request.POST.get('email'))
        except:
            return {}

        if user.validate(self.request.POST.get('password', '')) is True:
            headers = remember(self.request, user.user_id)
            return http.HTTPFound(
                self.request.route_url('home'),
                headers=headers
            )
        else:
            return {}
