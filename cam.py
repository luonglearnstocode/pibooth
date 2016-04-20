# -*- coding: utf-8 -*-
import time
import picamera
from PIL import Image, ImageDraw, ImageFont
import itertools
import datetime as dt
from time import localtime, strftime
import sys
from twython import Twython
CONSUMER_KEY = 'XPMRRREmy4jv6HU1U0N2d6HYv'
CONSUMER_SECRET = 'MHSkXmP28PW6IEVZ3iCitOlegWLhsZwLN9IBCd16dkOwBacUwU'
ACCESS_KEY = '722345011652796416-HtuggTLRcgv7DE5rUXrcJftNKLE04tz'
ACCESS_SECRET = 'LTH7mcHZs7H1gTY6M5s70RASEdcbZie2JTRLKR6BVAbVY'

def shoot(temp, lux):
	with picamera.PiCamera() as camera:
			camera.resolution = (1024, 768)
			camera.start_preview()
			time.sleep(3)

			#fix camera values
			camera.shutter_speed = camera.exposure_speed
			camera.exposure_mode = 'off'
			g = camera.awb_gains
			camera.awb_mode = 'off'
			camera.awb_gains = g
			
			#camera.iso = 100-200 daytime, 400-800 low light
			if float(lux) >= 250:
				iso = 100 + (float(lux) - 250)/(1000 - 250)*(200-100)
			else:
				iso = 400 - (float(lux) - 250)/(250)*(800-400)
			camera.iso = int(iso) #set iso value	
		
			#add date time to the image
			camera.annotate_text = strftime('%d-%m-%Y %H:%M:%S', localtime())
			#camera.annotate_text = temp
			camera.capture('/var/www/html/image.jpg')
			camera.stop_preview()

def editImage(temp):
	base_path = '/var/www/html/image.jpg'
	icon_path = 'icon.png'
	base = Image.open(base_path)
	icon = Image.open(icon_path)
	icon = icon.resize((200,200))
	offset = (0,550)
	base.paste(icon, offset, mask=icon)
	draw = ImageDraw.Draw(base)
	font_path = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
	font = ImageFont.truetype(font_path,80)
	text = str(int(float(temp))) + u"\N{DEGREE SIGN}" + 'C' 
	draw.text((180,620),text,(0,0,0), font=font)
	base.save(base_path)

def tweet(temp, lux):
	twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 
	toTweet = 'Current condition: ' + str(int(float(temp))) + u'\N{DEGREE SIGN}' + 'C ' \
		+ str(int(float(lux))) + ' lux'
	photo = open('/var/www/html/image.jpg','rb')
	#twitter.update_status_with_media(media=photo, status=toTweet)
	response = twitter.upload_media(media=photo)
	twitter.update_status(status=toTweet, media_ids=[response['media_id']]) 

