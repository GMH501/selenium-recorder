from flask import Flask

from tester.view import index, test, start, stop


def create_app(test_config=None):
    # create and configure the app
    app = Flask('tester', instance_relative_config=True)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.add_url_rule("/", "index", index, methods=["GET"])
    app.add_url_rule("/test", "test", test, methods=["GET"])
    app.add_url_rule("/start", "start", start, methods=["GET"])
    app.add_url_rule("/stop", "stop", stop, methods=["GET"])
    
    return app


def run():
    app=create_app()
    app.run(host="0.0.0.0", port="5000")