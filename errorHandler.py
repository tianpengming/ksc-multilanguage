from tornado.web import HTTPError
import tornado.web


class ErrorHandler(tornado.web.RequestHandler):
    """
    当请求错误的url时，进入该handle并抛出异常
    """
    def get(self):
        raise HTTPError(404, reason="Not Found", log_message="not found")
    def write_error(self, status_code, **kwargs):
        exc_info = kwargs.get("exc_info", None)
        exc = exc_info[1]
        if isinstance(exc, HTTPError):
            rsp = {
                "RequestId": 'a',
                "Error":{
                    "Code": exc.reason,
                    "Message": exc.log_message,
                    "Type": "Response"
                }
            }
            self.write(rsp)
            self.finish()
