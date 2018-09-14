import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):

        origin = self.get_http_origin()
        self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header("Access-Control-Allow-Credentials","true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    def get_http_origin(self):

        origin = self.request.headers.get("Origin", "game.ksyun.com")
        origin.replace("http://", "")
        origin.replace("https://", "")

        return origin

