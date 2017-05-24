
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
#from requests_aws4auth import AWS4Auth
import requests

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''



sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='enter sqs name')
class StdOutListener(StreamListener):




    def on_data(self, data):
        global queue
        data_json = json.loads(data)
        try:
            coordinates = data_json['place']['bounding_box']['coordinates']
            tweet = data_json['text']
            # print tweet
            place = data_json['place']
            language = data_json[u'user'][u'lang']
            #print language
            if place is not None and language== u'en':
                if coordinates[0] is not None and len(coordinates[0]) > 0:
                    avg_x = 0
                    avg_y = 0
                    for c in coordinates[0]:
                        avg_x = (avg_x + c[0])
                        avg_y = (avg_y + c[1])
                    avg_x /= len(coordinates[0])
                    avg_y /= len(coordinates[0])
                    coordinates = [avg_x, avg_y]
                
                e_data = {
                    'Tweet': {'DataType': 'String', 'StringValue': (tweet).encode("utf-8")},
                    'Latitude': {'DataType': 'Number', 'StringValue':str(avg_x)},
                    'Longitude': {'DataType': 'Number', 'StringValue': str(avg_y)}
                }
                #
                print e_data


                queue.send_message(MessageBody="tweet",MessageAttributes=e_data)

                
        except (KeyError, TypeError):
            pass
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    # for queue in sqs.queues.all():
    #     print(queue.url)


    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    streamin=Stream(auth,0)
    stream = Stream(auth, StdOutListener())
    stream.filter(languages=['en'], track=['trump','messi','ronaldo','bush','thursday','josh brown',
                         'location','amazon','dollar','lenovo','hugh','pizza','snapchat','money',
                         'election','lol','instagram','twitter','fb','facebook','nba','birthday',
                         'technology', 'hillary', 'food', 'travel','vote','nintendo', 'fashion', 'soccer',
                         'sports','modi','debate','america','india','obama','song','punjab','new york','bernie',
                         'news','logan','usa','london','health','Dangal'])
