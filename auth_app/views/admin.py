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

    @view_config(route_name="create_user", request_method="POST")
    def create_user(self):
        new_user = User(**self.request.POST)
        Session.add(new_user)
        try:
            Session.commit()
        except:
            Session.rollback()
        return http.HTTPFound(self.request.route_url("manage_users"))
