import base64

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] =  "http://sarnencj-us-1:kd99722l2k7y@proxyserver.webshare.io:3128"
	


"""

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] =  "http://sarnencj-us-1:kd99722l2k7y@proxyserver.webshare.io:3128"

        # Use the following lines if your proxy requires authentication
        proxy_user_pass = "sarnencj:kd99722l2k7y"
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

"""
