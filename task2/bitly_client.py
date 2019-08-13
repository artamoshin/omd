import asyncio
import urllib.parse

import aiohttp

API_URL = 'https://api-ssl.bitly.com/v3/'
ACCESS_TOKEN = '5cc78a9260ddcef05f3e17a9a219134802019d4e'


class APIException(Exception):
    pass


class Request:
    def __init__(self, api, method_name):
        self._api = api
        self._method_name = method_name

    def __getattr__(self, method_name):
        return Request(self._api, self._method_name + '/' + method_name)

    def __call__(self, **method_args):
        self._method_args = method_args
        return self._api.make_request(self)


class Response:
    def __init__(self, d):
        self.__dict__ = d


class BitlyAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self._session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    def __getattr__(self, method_name):
        return Request(self, method_name)

    async def make_request(self, request):
        url = urllib.parse.urljoin(API_URL, request._method_name)
        params = request._method_args
        params['access_token'] = self.access_token

        try:
            async with self._session.get(url, params=params) as response:
                json = await response.json()
                status_code = json.get('status_code')
                if status_code != 200:
                    status_txt = json.get('status_txt')
                    raise APIException(f'[{status_code}] {status_txt}')
                return Response(json['data'])
        except aiohttp.ClientError as err:
            raise APIException(err)


async def main():
    async with BitlyAPI(access_token=ACCESS_TOKEN) as api:
        responses = await asyncio.gather(
            api.link.clicks(link='https://bit.ly/2EAh3Vo'),
            api.link.clicks(link='https://bit.ly/2A7lTGn'),
        )
        for response in responses:
            print(response.link_clicks)  # output: <number of clicks>

        try:
            response = await api.link.clicks(link='bad_link_not_found')
        except APIException as err:
            print(err)  # output: [404] NOT FOUND

        responses = await asyncio.gather(
            api.info(shortUrl='https://bit.ly/2EAh3Vo'),
            api.info(shortUrl='https://bit.ly/2A7lTGn'),
        )
        for response in responses:
            print(response.info)


if __name__ == '__main__':
    asyncio.run(main())
