FROM python:3.5

ADD . /auth-app
VOLUME /auth-app
WORKDIR /auth-app

RUN pip install -e /auth-app

SHELL ["/bin/bash"]
CMD ["gunicorn", "--paste", "development.ini", "--reload"]
