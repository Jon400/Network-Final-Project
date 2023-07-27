from datetime import datetime
import json
import os
from whatsapp_api_client_python import API
from os import environ
#!/usr/bin/env python3

import sys
from dateutil import tz
import asyncio
#import socks


# host = '127.0.0.1'
# port = 9011
# username = '1234'
# password = '1234'
# proxy = (socks.SOCKS5, host, port, True, username, password)

channel_id1 = "972528706580-1610534090@g.us"
#channel_id2 = sys.argv[2]
# channel_id3 = sys.argv[3]

COVERT_RATE = 10

directory1 = 'channels-'+str(COVERT_RATE)+'/channel-'+str(COVERT_RATE)+'-'+channel_id1+'.txt' 
os.makedirs(os.path.dirname(directory1), exist_ok=True)
#directory2 = 'channels-'+str(COVERT_RATE)+'/channel-'+str(COVERT_RATE)+'-'+channel_id2+'.txt'

ID_INSTANCE = "7103843108"
API_TOKEN_INSTANCE = "0951241446c743fb897b5a227a1b698ae15e4d24205a4b398b"

greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)

update_count1 = 0
update_count2 = 0
update_count3 = 0
TestChannelID1 = 1141095048
TestChannelID2 = 1347586411
TestChannelID3 = 1367067490
counter = 0

now = datetime.now()

f= open(directory1, 'w')
f.write(str(now) + "\n")
f.close()

# f= open(directory2, 'w')
# f.write(str(now) + "\n")
# f.close()

def main():
   greenAPI.webhooks.startReceivingNotifications(onEvent)

def onEvent(typeWebhook, body):
   if typeWebhook == 'incomingMessageReceived':
      onIncomingMessageReceived(body)      
   elif typeWebhook == 'deviceInfo':   
      onDeviceInfo(body)              
   elif typeWebhook == 'incomingCall':
      onIncomingCall(body)
   elif typeWebhook == 'outgoingAPIMessageReceived':
      onOutgoingAPIMessageReceived(body)
   elif typeWebhook == 'outgoingMessageReceived':
      onOutgoingMessageReceived(body)
   elif typeWebhook == 'outgoingMessageStatus':
      onOutgoingMessageStatus(body)
   elif typeWebhook == 'stateInstanceChanged':
      onStateInstanceChanged(body)
   elif typeWebhook == 'statusInstanceChanged':
      onStatusInstanceChanged(body)

def onIncomingMessageReceived(body):
        idMessage = body['idMessage']
        eventDate = datetime.fromtimestamp(body['timestamp'])
        senderData = body['senderData']
        messageData = body['messageData']
        print(idMessage + ': ' 
            + 'At ' + str(eventDate) + ' Incoming from ' \
            + json.dumps(senderData, ensure_ascii=False) \
            + ' message = ' + json.dumps(messageData, ensure_ascii=False))

def onIncomingCall(body):
   idMessage = body['idMessage']
   eventDate = datetime.fromtimestamp(body['timestamp'])
   fromWho = body['from']
   print(idMessage + ': ' 
      + 'Call from ' + fromWho 
      + ' at ' + str(eventDate))

def onDeviceInfo(body):
   eventDate = datetime.fromtimestamp(body['timestamp'])
   deviceData = body['deviceData']
   print('At ' + str(eventDate) + ': ' \
      + json.dumps(deviceData, ensure_ascii=False))

def onOutgoingMessageReceived(body):
   global TestChannelID1
   global TestChannelID2
   global TestChannelID3
   global update_count1
   global update_count2
   global update_count3
   senderData = body['senderData']
   channel_id = senderData['chatId']
   if channel_id == channel_id1:
      update_count1 += 1
      curr_directory = directory1
      # elif channel_id == channel_id2:
      #    update_count2 += 1
      #    curr_directory = directory2
   else:
      return
   update_time = body['timestamp']
   idMessage = body['idMessage']
   eventDate = datetime.fromtimestamp(body['timestamp'])
   messageData = body['messageData']
   message_size = len(json.dumps(body, ensure_ascii=False).encode('utf-8'))
   # calculate the message size
   if 'text' in messageData:
      update_type = 'text'
   elif 'image' in messageData:
      update_type = 'image'
   elif 'video' in messageData:
      update_type = 'video'
   elif 'audio' in messageData:
      update_type = 'audio'
   elif 'document' in messageData:
      update_type = 'document'
   else :
      update_type = 'other'

   file = open(curr_directory, 'a')
   file.write(str(channel_id)+' '+str(update_time)+' '+update_type+' '+str(message_size)+"\n")
   file.close()

   print(idMessage + ': ' 
   + 'At ' + str(eventDate) + ' Outgoing from ' \
   + json.dumps(senderData, ensure_ascii=False) \
   + ' message = ' + json.dumps(messageData, ensure_ascii=False)
   + ' message size = ' + str(message_size))

def onOutgoingAPIMessageReceived(body):
   idMessage = body['idMessage']
   eventDate = datetime.fromtimestamp(body['timestamp'])
   senderData = body['senderData']
   messageData = body['messageData']
   print(idMessage + ': ' 
      + 'At ' + str(eventDate) + ' API outgoing from ' \
      + json.dumps(senderData, ensure_ascii=False) + \
      ' message = ' + json.dumps(messageData, ensure_ascii=False))

def onOutgoingMessageStatus(body):
   idMessage = body['idMessage']
   status = body['status']
   eventDate = datetime.fromtimestamp(body['timestamp'])
   print(idMessage + ': ' 
      + 'At ' + str(eventDate) + ' status = ' + status)

def onStateInstanceChanged(body):
   eventDate = datetime.fromtimestamp(body['timestamp'])
   stateInstance = body['stateInstance']
   print('At ' + str(eventDate) + ' state instance = ' \
      + json.dumps(stateInstance, ensure_ascii=False))

def onStatusInstanceChanged(body):
   eventDate = datetime.fromtimestamp(body['timestamp'])
   statusInstance = body['statusInstance']
   print('At ' + str(eventDate) + ' status instance = ' \
      + json.dumps(statusInstance, ensure_ascii=False))


if __name__ == "__main__":
    main()


