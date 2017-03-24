import pyramid.httpexceptions as http
from pyramid.view import view_config, view_defaults

import auth_app.forms as forms
from auth_app.models import User, Session


@view_defaults(permission="admin", renderer="manage_users.mako")
class UserManagementViews(object):

    def __init__(self, request):
        self.request = request

    @property
    def create_user_form(self):
        if not getattr(self, '_create_user_form', None):
            self._create_user_form = forms.CreateUserForm(self.request.POST)
        return self._create_user_form

    @view_config(route_name="manage_users")
    def manage_users(self):
        return {
            "users": User.all(),
            "create_user_form": self.create_user_form,
        }

    @view_config(route_name="create_user", request_method="POST")
    def create_user(self):
        if not self.create_user_form.validate():
            return self.manage_users()

        new_user = User(**self.create_user_form.data)
        new_user.reset()  # randomize password and create token
        Session.add(new_user)
        try:
            Session.commit()
        except:
            Session.rollback()
            raise http.HTTPInternalServerError()
        return http.HTTPFound(self.request.route_url("manage_users"))

    @view_config(route_name="delete_user", context=User)
    def delete_user(self):
        Session.delete(self.request.context)
        Session.commit()
        return http.HTTPFound(self.request.route_url("manage_users"))

    @view_config(route_name="reset_user", context=User)
    def reset_user(self):
        self.request.context.reset()
        Session.add(self.request.context)
        Session.commit()
        return http.HTTPFound(self.request.route_url("manage_users"))
