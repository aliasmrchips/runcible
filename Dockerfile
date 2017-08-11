FROM python:2

MAINTAINER Mark Mathis <aliasmrchips@descarteslabs.com>

RUN apt-get update
RUN apt-get install libpq-dev libgeos-dev libgdal-dev python-pkg-resources -y

COPY . /opt/app
WORKDIR /opt/app

RUN pip install --upgrade pip
RUN pip install numpy scipy gevent gunicorn
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "spoons.wsgi:application", "-k", "gevent", "--bind", ":8000", "--timeout", "360", "--access-logfile", "-", "--graceful-timeout", "360"]