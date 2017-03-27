from pyramid.view import view_config, view_defaults
import pyramid.httpexceptions as http
from pyramid.security import remember, forget
from sqlalchemy.orm.exc import NoResultFound

from auth_app.models import User, Session
import auth_app.forms as forms


@view_defaults(route_name="login", renderer="login.mako")
class AuthViews(object):

    def __init__(self, request):
        self.request = request

    @property
    def login_form(self):
        if not getattr(self, '_login_form', None):
            self._login_form = forms.LoginForm(self.request.POST)
        return self._login_form

    @view_config(route_name="logout")
    def logout(self):
        return http.HTTPFound(
            self.request.route_url('index'),
            headers=forget(self.request)
        )

    @view_config(route_name="forgot_password", request_method="POST")
    def forgot_password(self):
        try:
            user = User.one(email=self.request.POST.get('email'))
        except NoResultFound:
            return {}

        user.set_token()
        Session.add(user)
        Session.commit()
        return {}

    @view_config(request_method="GET")
    def get_login(self):
        return {"login_form": self.login_form}

    @view_config(request_method="POST")
    def post_login(self):
        if self.login_form.validate():
            user = self.login_form.user
            if user.token is not None:  # clear any outstanding tokens
                user.token = None
                Session.add(user)
                Session.commit()

            headers = remember(self.request, user.user_id)
            return http.HTTPFound(
                self.request.route_url('home'),
                headers=headers
            )
        else:
            return self.get_login()


@view_defaults(route_name="redeem", context=User,
               renderer="change_password.mako")
class RedeemTokenViews(object):

    def __init__(self, request):
        self.request = request
        self.user = request.context

    @view_config(request_method="GET")
    def get_redeem_token(self):
        """ Show the set password screen """
        return {}

    @view_config(request_method="POST")
    def post_redeem_token(self):
        """ Clear the token and set the posted password """

        if self.request.POST.get("password") is None:
            return {}

        self.user.token = None
        self.user.password = self.request.POST.get("password", "")
        Session.add(self.user)
        Session.commit()

        return http.HTTPFound(self.request.route_url("login"))
