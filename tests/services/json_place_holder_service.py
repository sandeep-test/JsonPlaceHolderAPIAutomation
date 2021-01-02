import requests
import json
import logging


class JsonPlaceHolderService:

    logger = logging.getLogger('test_log')

    def __init__(self, url):
        self.url = url
        self.end_point_get_posts = '/'.join((str(url), 'posts'))
        self.end_point_invalid_posts = '/'.join((str(url), 'invalidposts'))
        self.end_point_post_a_post = self.end_point_get_posts

    def __send_request(self, method: str, url: str, **kwargs):
        self.logger.debug("sending " + method + " request: " + str(url))
        self.logger.debug("sending params: " + str(kwargs))

        res = requests.request(method, url, **kwargs)

        self.logger.debug("received response code: " + str(res.status_code))
        self.logger.debug("received response: " + json.dumps(res.json()))
        return res

    def get_posts(self) -> requests.Response:
        res = self.__send_request('GET', self.end_point_get_posts)
        return res

    def post_a_new_post(self, post_req_body_json) -> requests.Response:
        res = self.__send_request('POST', self.end_point_post_a_post, json=post_req_body_json)
        return res

    def put_a_post(self, put_req_body_json) -> requests.Response:
        post_id = put_req_body_json.get('id')
        res = self.__send_request('PUT', '/'.join((self.end_point_post_a_post, str(post_id))), json=put_req_body_json)
        return res

    def get_post_with_id(self, i: int = 1) -> requests.Response:
        res = self.__send_request('GET', '/'.join((self.end_point_get_posts, str(i))))
        return res

    def delete_post_with_id(self, i: int = 1) -> requests.Response:
        res = self.__send_request('DELETE', '/'.join((self.end_point_get_posts, str(i))))
        return res

    def get_invalid_posts(self) -> requests.Response:
        res = self.__send_request('GET', self.end_point_invalid_posts)
        return res


