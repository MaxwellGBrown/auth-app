from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import auth_app.models as app_model


def main(global_config, **settings):
    config = Configurator(settings=settings)

    engine = engine_from_config(configuration=settings, prefix="sqlalchemy.")
    app_model.bind_engine(engine, create_all=True)

    config.add_route('index', '/')
    config.scan()

    return config.make_wsgi_app()
