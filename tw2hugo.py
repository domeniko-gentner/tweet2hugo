#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /**********************************************************************************
#  * _author  : Domeniko Gentner
#  * _mail    : code@tuxstash.de
#  * _repo    : https://git.tuxstash.de/gothseidank/tweet2png
#  * _license : This project is under MIT License
#  *********************************************************************************/
from twitter import twitter
from sys import exit
from platform import system
import json

twitter = twitter()
tweet = twitter.get_latest_tweet()
handle = twitter.handle()

if system().lower() == "windows":
    with open('latest_tweet.json', 'w') as fp:
        json.dump(tweet, fp, indent=4, sort_keys=True)
if system().lower() == "linux":
    with open(twitter.output_location(), 'w') as fp:
        json.dump(tweet, fp, indent=4, sort_keys=True)

exit(0)
