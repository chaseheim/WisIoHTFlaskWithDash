"""Application entry point."""
from application import create_app

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)# TODO: Change debug to false when deployed