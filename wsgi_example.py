#!/usr/bin/env python3


class Application:
    def __init__(self):
        self.routes = {}
        self.middlewares = set()

    def add_middleware(self, mware):
        self.middlewares.add(mware)

    def add_route(self, url):
        def inner_func(func):
            self.routes.update({url: func})

        return inner_func

    def __call__(self, env, start_response):
        path = env.get("PATH_INFO", None)
        route = self.routes.get(path, None)

        # undefined route
        if route is None:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Not Found"]

        # middle ware calls before route selection
        data = {}
        for mware in self.middlewares:
            mware(data, env)

        result = route(data)
        status = result["status"]
        text = result["text"]
        start_response(status, [("Content-Type", "text/plain")])
        return [text.encode("utf-8")]


app = Application()


@app.add_route("/")
def home_route(request_data):
    method = request_data["method"]
    return {"text": f"Home {method}", "status": "200 OK"}


@app.add_route("/contacts")
def contacts_route(request_data):
    hello = request_data["other"]
    return {"text": f"Contacts {hello}", "status": "200 OK"}


@app.add_middleware
def method_ware(request_data, environ):
    request_data["method"] = environ["REQUEST_METHOD"]


@app.add_middleware
def hello_ware(request_data, environ):
    request_data["other"] = "Hello from Front controller"

