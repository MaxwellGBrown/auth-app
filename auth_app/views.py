from pyramid.view import view_config, view_defaults


@view_config(route_name='index', renderer='index.mako')
def index(request):
    return {}


@view_defaults(route_name="login", renderer="login.mako")
class LoginViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get_login(self):
        return {}

    @view_config(request_method="POST")
    def post_login(self):
        return {}
