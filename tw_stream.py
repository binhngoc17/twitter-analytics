#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import elasticsearch
from utils import NestedDict
import json
import datetime

#Variables that contains the user credentials to access Twitter API 
access_token = "18347756-tP0MLB56MKtTUtKn3mMxj2rHEV5btRC36lscMj47w"
access_token_secret = "T43LSZPkxmxcyG8Ouzw3Nmq14m8blK2kpuFQyBQul8KJQ"
consumer_key = "ccSUlIjsJ4GqLGE6l16KkvchM"
consumer_secret = "g2lt8Xe5fPOhG8ffYASI3bUk5Wu2YZKucVXSdbZUXaqxLlbIoV"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        data = NestedDict(json.loads(data))
        with open('data/twitter/zopim.json', 'w') as f:
            json.dump({
                'created_at': datetime.datetime.strptime(
                    data['created_at'],
                    '%a %b %d %H:%M:%S +0000 %Y'
                    ).strftime('%s'),
                'username': data['user.name'],
                'screen_name': data['user.screen_name'],
                'msg': data['text']
                },f)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['zopim', 'livechat', 'customer engagement'])