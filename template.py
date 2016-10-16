from eca import *
from eca.generators import start_offline_tweets
import eca.http

import random
from datetime import datetime

## You might have to update the root path to point to the correct path
## (by default, it points to <rules>_static)
# root_content_path = 'template_static'

def add_request_handlers(httpd):
  httpd.add_route('/buffer', eca.http.GenerateEvent('buffer'), methods=["POST"])

# binds the 'setup' function as the action for the 'init' event
# the action will be called with the context and the event
@event('init')
def setup(ctx, e):
    # set empty buffer
    ctx.buffer = {'tweets': [], 'potd': []}
    ctx.photoCount = 0
    ctx.totalTweets = 0
    ctx.currentDay = 0
    ctx.dayTweets = 0
    start_offline_tweets('weer.txt', 'chirp', time_factor=10000)

# define a normal Python function
def clip(lower, value, upper):
    return max(lower, min(value, upper))

@event('chirp')
def tweet(ctx, e):
    # filter #Buren tweets
    if e.data['text'].find('#Buren') == -1:
      ctx.totalTweets += 1
      date = datetime.strptime(e.data['created_at'], '%a %b %d %H:%M:%S %z %Y')
      now = "{}{}{}".format(date.year, date.month, date.day)
      if now != ctx.currentDay:
        ctx.currentDay = now
        ctx.dayTweets = 0
        ctx.buffer['tweets'] = []
      ctx.dayTweets += 1
      
      # check for url to replace it with an working picture
      
      if 'media' in e.data['entities']:
        changeMedia(ctx, e)
        ctx.photoCount += 1
        print(e.data['text'])
        
      if len(e.data['entities']['urls']) > 0:
        changeUrls(ctx, e)
        ctx.photoCount += 1
        print(e.data['text'])
        
      if ctx.photoCount > 14:
        ctx.photoCount = 0
        
      ctx.buffer['tweets'].append(e.data)  
      emit('tweet', {
        'date': now,
        'mood': {
          'Noord-Holland': random.uniform(0, 10),
          'Utrecht': random.uniform(0, 10),
          'Friesland': random.uniform(0, 10),
          'Flevoland': random.uniform(0, 10),
          'Gelderland': random.uniform(0, 10),
          'Drenthe': random.uniform(0, 10),
          'Groningen': random.uniform(0, 10),
          'Overijssel': random.uniform(0, 10),
          'Zeeland': random.uniform(0, 10),
          'Zuid-Holland': random.uniform(0, 10),
          'Noord-Brabant': random.uniform(0, 10),
          'Limburg': random.uniform(0, 10)
        },
        'count': {
          'day': ctx.dayTweets,
          'total': ctx.totalTweets
        },
        'moodGeneral': {
          'moodLevel': random.uniform(6,10)
        },
        'tweet': e.data
      })  

def changeMedia(ctx, e): 
  e.data['text'] = e.data['text'].replace(e.data['entities']['media'][0]['url'], ' photo')
  e.data['entities']['media'][0]['url'] = urls[ctx.photoCount]
  e.data['entities']['media'][0]['display_url'] = ' photo'
  emitPhoto(ctx, e)
     
def changeUrls(ctx, e):       
  e.data['text'] = e.data['text'].replace(e.data['entities']['urls'][0]['url'], ' photo')
  e.data['entities']['urls'][0]['url'] = urls[ctx.photoCount]
  e.data['entities']['urls'][0]['display_url'] = ' photo'
  emitPhoto(ctx, e)
  
def emitPhoto(ctx, e):
  emit('photo', {
    'photo': photos[ctx.photoCount]
    })
  ctx.buffer['potd'].append(photos[ctx.photoCount])
  if len(ctx.buffer['potd']) > 5:
    ctx.buffer['potd'].pop(0)
  
@event('buffer')
def loadBuffer(ctx, e):
  emit('buffer', {
      'date': ctx.currentDay,
      'mood': {
        'Noord-Holland': random.uniform(0, 10),
        'Utrecht': random.uniform(0, 10),
        'Friesland': random.uniform(0, 10),
        'Flevoland': random.uniform(0, 10),
        'Gelderland': random.uniform(0, 10),
        'Drenthe': random.uniform(0, 10),
        'Groningen': random.uniform(0, 10),
        'Overijssel': random.uniform(0, 10),
        'Zeeland': random.uniform(0, 10),
        'Zuid-Holland': random.uniform(0, 10),
        'Noord-Brabant': random.uniform(0, 10),
        'Limburg': random.uniform(0, 10)
      },
      'buffer': ctx.buffer,
      'count': {
        'day': ctx.dayTweets,
        'total': ctx.totalTweets
      }
    })
    
urls = [
  'http://imgur.com/MqWFFPb',
  'http://imgur.com/oqXEEgh',
  'http://imgur.com/rV8W4O7',
  'http://imgur.com/vECgD96',
  'http://imgur.com/hkwXN7S',
  'http://imgur.com/K8k00tx',
  'http://imgur.com/1IJJcaj',
  'http://imgur.com/WtI90Eg',
  'http://imgur.com/nL3056N',
  'http://imgur.com/6Ns9xZx',
  'http://imgur.com/AxcwWYD',
  'http://imgur.com/CvwzIoE',
  'http://imgur.com/knDy7Cu',
  'http://imgur.com/EIUkR49',
  'http://imgur.com/lSbAiSb',
  'http://imgur.com/jENAMfB'
]

photos = [
  'http://imgur.com/MqWFFPb.jpg',
  'http://imgur.com/oqXEEgh.jpg',
  'http://imgur.com/rV8W4O7.jpg',
  'http://imgur.com/vECgD96.jpg',
  'http://imgur.com/hkwXN7S.jpg',
  'http://imgur.com/K8k00tx.jpg',
  'http://imgur.com/1IJJcaj.jpg',
  'http://imgur.com/WtI90Eg.jpg',
  'http://imgur.com/nL3056N.jpg',
  'http://imgur.com/6Ns9xZx.jpg',
  'http://imgur.com/AxcwWYD.jpg',
  'http://imgur.com/CvwzIoE.jpg',
  'http://imgur.com/knDy7Cu.jpg',
  'http://imgur.com/EIUkR49.jpg',
  'http://imgur.com/lSbAiSb.jpg',
  'http://imgur.com/jENAMfB.jpg'
]