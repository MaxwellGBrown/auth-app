from pyramid.view import view_config


@view_config(route_name="home", renderer="home.mako",
             permission="authenticated")
def home(request):
    return {}
