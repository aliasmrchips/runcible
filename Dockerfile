FROM python:2

MAINTAINER Mark Mathis <aliasmrchips@descarteslabs.com>

RUN apt-get update
RUN apt-get install libpq-dev libgeos-dev libgdal-dev python-pkg-resources -y

RUN pip install --upgrade pip
RUN pip install numpy==1.10.4 
RUN pip install scipy==0.17.0
RUN pip install gevent==1.2.2
RUN pip install gunicorn==19.7.1
RUN pip install -r requirements.txt

COPY . /opt/app
WORKDIR /opt/app

EXPOSE 8000

CMD ["gunicorn", "spoons.wsgi:application", "-k", "gevent", "--bind", ":8000", "--timeout", "360", "--access-logfile", "-", "--graceful-timeout", "360"]