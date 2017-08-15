# README #

runcible

### What is this repository for? ###

* Python API for interacting with image metadata
* Web services and command line utilities using the API

### How do I get set up? ###

* Check out the code
* Install dependencies
    * `virtualenv venv`
    * `source venv/bin/activate`
    * `pip install -r requirements.txt`
    * `export DATABASE_URL="..."`
* Test installation
    * `python manage.py migrate`
    * `python manage.py shell`
* Run the service
    * `python mange.py runserver`
* Build a container
    * `docker build -t runcible .`
