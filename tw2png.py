#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /**********************************************************************************
#  * _author  : Domeniko Gentner
#  * _mail    : code@tuxstash.de
#  * _repo    : https://git.tuxstash.de/gothseidank/tweet2png
#  * _license : This project is under MIT License
#  *********************************************************************************/
from mail import mail
from painter import painter
from twitter import twitter
from sys import exit

twitter = twitter()
painter(twitter.get_latest_tweet(), twitter.handle())
exit(0)
