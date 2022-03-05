import requests

class Telegram:

    SEND_MESSAGE_URL = ''

    def __init__(self, token, channelname) -> None:
        self.token = token
        self.channelname = channelname

    def sendmessage(self, message):
        SEND_MESSAGE_URL = 'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=@{channel}&text={msg}'.format(bot_token=self.token,channel=self.channelname,msg=message)
        requests.get(SEND_MESSAGE_URL)