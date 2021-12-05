import os
from twilio.rest import Client
from nameko.rpc import rpc

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
    
class SmsSend:
    name = "sms_service"

    @rpc
    def create(self, receiver_number, sms_message):
        client = Client(account_sid, auth_token)

        message = client.messages.create(body=sms_message, from_=phone_number, to=receiver_number)

        return 'Sent to {}'.format(receiver_number)
