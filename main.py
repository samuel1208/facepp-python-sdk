#!/usr/bin/env python2

from facepp import API , File

API_KEY = 'f6dc9651b27bce2d54ce01945c1f7b83'
API_SECRET = 'mPl3uedPiLohaMuxSF0DQgEdrZw-cBkz'

api = API(API_KEY, API_SECRET)
res=api.detection.detect(img = File(r'/home/samuel/1.jpeg'))
print res
