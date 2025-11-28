

class httpresponse:
  

    def __init__(self, response_time_ms=None, response_time_calculated_ms=None, status_code=None, content=None, headers=None, http_error=None):
        self.response_time_ms = response_time_ms
        self.response_time_calculated_ms = response_time_calculated_ms
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self.http_error = http_error
       
    