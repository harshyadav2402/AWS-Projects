import time
from monkeylearn import MonkeyLearn
import boto3
import json

ml = MonkeyLearn('enter monkey learn key')
module_id = 'cl_qkjxv9Ly'
sqs = boto3.resource('sqs')
sns = boto3.client('sns')
queue = sqs.get_queue_by_name(QueueName='enter sqs domain name')
arn = 'arn:aws:sns:us-east-2:479960115625:twitter'
def worker(queue):
    while True:
        messages = queue.receive_messages(MessageAttributeNames=['Tweet', 'Latitude', 'Longitude'])
        if len(messages)>0:
            for message in messages:
            
                if message.message_attributes is not None:
                    tweet = [message.message_attributes.get('Tweet').get('StringValue')]
                    lat = message.message_attributes.get('Latitude').get('StringValue')
                    lng = message.message_attributes.get('Longitude').get('StringValue')
                    
                    try:
                        response = ml.classifiers.classify(module_id, tweet, sandbox=True)
                        
                    except Exception as e:
                        print "error"
                
                    sns_message = {"tweet":tweet, "lat":lat, "lng": lng, "sentiment":response.result[0][0]['label']}
                    print("SNS messsage: "+str(sns_message))
                    sns.publish(TargetArn=arn, Message=json.dumps({'default':json.dumps(sns_message)}))
                
                message.delete()
        
if __name__ == '__main__':
    worker(queue)
while True:
    pass


