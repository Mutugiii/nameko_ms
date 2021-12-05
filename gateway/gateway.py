import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http

class GatewayService:
    name = 'gateway'

    mailer_rpc = RpcProxy('mailer_service')
    sms_rpc = RpcProxy('sms_service')
    tweetbot_rpc = RpcProxy('tweetbot_service')

    @http('POST', '/mailer')
    def send_email(self, request):
        data = json.loads(request.get_data(as_text=True))
        message = self.mailer_rpc.create(data['receiver_email'], data['receiver_name'], data['mail_message'])

        return message
    
    @http('POST', '/sms')
    def send_sms(self, request):
        data = json.loads(request.get_data(as_text=True))
        message = self.sms_rpc.create(data['receiver_number'], data['sms_message'])

        return message

    @http('POST', '/tweet')
    def post_tweet(self, request):
        data = json.loads(request.get_data(as_text=True))
        message = self.tweetbot_rpc.create(data['tweet_message'])

        return message

