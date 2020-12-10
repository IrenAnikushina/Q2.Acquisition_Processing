import scrapy
from scrapy.http import HtmlResponse
import re
from instaparser.items import InstaparserItem
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'iriska_msk'
    inst_pwd = "#PWD_INSTAGRAM_BROWSER:10:1607526051:AaBQALGpRRXfEt9nOzzRppsHo+LlYcYcgc29iClgegiDE4o0bPUO8qumJZ9eLNXdeg2Cwh7R7emKk5hsVSHgtJYEyDCcIjzszzDtooCjc+izNjhggIZxvpF/WqLEmfE9nTeL9hVITpe4nl8bU7np"
    parse_user = ['clean.inside', 'luxury.undwear']
    graphql_link = 'https://www.instagram.com/graphql/query/?'
    query_hash_foll = 'c76146de99bb02f6415203be841dd25a'
    query_hash_sub = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_link,
            method='POST',
            callback=self.user_parse,
            formdata={
                'username': self.inst_login,
                'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_user:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 12}
        follower_links = f'{self.graphql_link}query_hash={self.query_hash_foll}&{urlencode(variables)}'
        yield response.follow(
            follower_links,
            callback=self.user_foll_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )
        subscription_links = f'{self.graphql_link}query_hash={self.query_hash_sub}&{urlencode(variables)}'
        yield response.follow(
            subscription_links,
            callback=self.user_sub_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def user_foll_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            follower_links = f'{self.graphql_link}query_hash={self.query_hash_foll}&{urlencode(variables)}'
            yield response.follow(
                follower_links,
                callback=self.user_foll_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for follower in followers:
            item = InstaparserItem(
                source_user=username,
                user_id=follower['node']['id'],
                username=follower['node']['username'],
                full_name=follower['node']['full_name'],
                profile_pic_url=follower['node']['profile_pic_url'],
                follower_data=follower['node'],
                status='follower'
            )
            yield item

    def user_sub_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            subscription_links = f'{self.graphql_link}query_hash={self.query_hash_sub}&{urlencode(variables)}'
            yield response.follow(
                subscription_links,
                callback=self.user_sub_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        subscriptions = j_data.get('data').get('user').get('edge_follow').get('edges')
        for subscription in subscriptions:
            item = InstaparserItem(
                source_user=username,
                user_id=subscription['node']['id'],
                username=subscription['node']['username'],
                full_name=subscription['node']['full_name'],
                profile_pic_url=subscription['node']['profile_pic_url'],
                follower_data=subscription['node'],
                status='subscription'
            )
            yield item

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
