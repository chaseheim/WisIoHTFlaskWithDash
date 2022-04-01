"""Application entry point."""
from distutils.log import debug
from application import init_app

app = init_app()

if __name__ == "__main__":
    app.run(host='localhost', debug=True)# TODO: Change debug to false when deployed