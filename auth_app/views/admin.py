import pyramid.httpexceptions as http
from pyramid.view import view_config, view_defaults

import auth_app.forms as forms
from auth_app.auth import User


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
            "users": [],  # TODO Return a list of users
            "create_user_form": self.create_user_form,
        }

    @view_config(route_name="create_user", request_method="POST")
    def create_user(self):
        if not self.create_user_form.validate():
            return self.manage_users()

        # TODO create a new user
        return http.HTTPFound(self.request.route_url("manage_users"))

    @view_config(route_name="delete_user", context=User)
    def delete_user(self):
        # TODO delete a user
        return http.HTTPFound(self.request.route_url("manage_users"))

    @view_config(route_name="reset_user", context=User)
    def reset_user(self):
        # TODO "reset" a user (password, account, whatever)
        return http.HTTPFound(self.request.route_url("manage_users"))
