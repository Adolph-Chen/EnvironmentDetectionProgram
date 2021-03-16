from django.utils.deprecation import MiddlewareMixin
class MyTest(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['access-control-expose-headers'] = "Authorization"
        response['access-control-allow-methods'] = ['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE']
        response['access-control-allow-headers'] = ["Authorization","Content-Type","Depth","User-Agent","X-File-Size","X-Requested-With","X-Requested-By",'If-Modified-Since','X-File-Name','X-File-Type','Cache-Control','Origin']
        '''
        access-control-allow-headers: Authorization, Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, X-File-Type, Cache-Control, Origin

        access-control-allow-methods: GET, POST, OPTIONS, PUT, DELETE

        access-control-allow-origin: *

        access-control-expose-headers: Authorization

        '''
        return response