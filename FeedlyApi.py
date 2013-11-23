#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import ProjectConfig
import traceback
import urllib2
import urllib
import json


class FeedlyAPI:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def __request(self, url, data=None, token=None):
        headers = {}
        url = ProjectConfig.api_prefix+url
        if token:
            headers['Authorization'] = 'OAuth %s' % token
        if data:
            data = urllib.urlencode(data)
        request = urllib2.Request(url, data,  headers)
        result = urllib2.urlopen(request).read()
        return result

    def getToken(self, code, redirect_uri, state=None):
        data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
            }
        if state:
            data['state'] = state
        url = '/v3/auth/token'
        try:
            result = self.__request(url, data)
            jsp_result = json.loads(result)
            if 'access_token' in jsp_result:
                self.token = jsp_result['access_token']
            return jsp_result
        except urllib2.HTTPError, e:
            return json.loads(e.read())
        except:
            print traceback.format_exc()


    def getSubscription(self, token=None):
        if not token:
            token = self.token
        url = '/v3/subscriptions'
        result = self.__request(url, None, token)
        jsp_result = json.loads(result)
        return jsp_result

    def getProfile(self, token):
        if not token:
            token = self.token
        url = '/v3/profile'
        result = self.__request(url, None, token)
        jsp_result = json.loads(result)
        return jsp_result

    def getPreferences(self, token):
        if not token:
            token = self.token
        url = '/v3/preferences'
        result = self.__request(url, None, token)
        jsp_result = json.loads(result)
        return jsp_result

    def getCategories(self, token):
        if not token:
            token = self.token
        url = '/v3/categories'
        result = self.__request(url, None, token)
        jsp_result = json.loads(result)
        return jsp_result

    

if __name__ == '__main__':
    fa = FeedlyAPI('sandbox', 'Z5ZSFRASVWCV3EFATRUY')
    #print fa.getToken('AQAAqeZ7InUiOiIxMTA1MjE3ODMwNDgxNjc1NTI3MjAiLCJpIjoiMmU2MWZhMDUtYTA5Zi00MmU0LWFmNzctYzFjNjkyMDk4N2I5IiwicCI6NiwiYSI6IkZlZWRseSBzYW5kYm94IGNsaWVudCIsInQiOjEzODUxOTU4NDIwOTd9', 'http://localhost')
    print fa.getCategories('AQAAk5J7ImkiOiIyZTYxZmEwNS1hMDlmLTQyZTQtYWY3Ny1jMWM2OTIwOTg3YjkiLCJwIjo2LCJhIjoiRmVlZGx5IHNhbmRib3ggY2xpZW50IiwidCI6MSwidiI6InNhbmRib3giLCJ4Ijoic3RhbmRhcmQiLCJlIjoxMzg1ODAwODQ1OTAwfQ:sandbox')
