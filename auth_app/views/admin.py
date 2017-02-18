from pyramid.view import view_config, view_defaults
import pyramid.httpexceptions as http

from auth_app.models import User, Session


@view_defaults(permission="admin")
class UserManagementViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name="manage_users", renderer="manage_users.mako")
    def manage_users(self):
        return {"users": User.all()}
