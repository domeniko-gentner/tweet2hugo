#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /**********************************************************************************
#  * _author  : Domeniko Gentner
#  * _mail    : code@tuxstash.de
#  * _repo    : https://git.tuxstash.de/gothseidank/tweet2png
#  * _license : This project is under MIT License
#  *********************************************************************************/
import requests
from pathlib import Path
from platform import system
from json import load as j_load
from mail import mail
from typing import Union
from sys import exit


class twitter:

    def __init__(self):
        self.path = str()
        self.credentials = str()

        if system().lower() == "windows":
            self.path = Path("twitter.json")
        else:
            self.path = Path("/etc/tw2hugo/twitter.json")

        try:
            with self.path.open('r') as fp:
                self.credentials = j_load(fp)

        except FileNotFoundError:
            mail("Could not find bearer token file! Script was discontinued.")
            exit(1)

    def handle(self):
        return self.credentials['twitter-handle']

    def output_location(self):
        return self.credentials['output-location']

    def get_latest_tweet(self) -> Union[str, None]:
        try:
            get_url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" \
                      f"{self.credentials['twitter-handle']}&count=1&tweet_mode=extended"

            header = {
                "Authorization": f"Bearer {self.credentials['bearer']}"
            }

            r = requests.get(url=get_url, headers=header)
            r.raise_for_status()
            try:
                # Get hashtag list
                hashtag = r.json()[0]['entities']['hashtags'][0]['text']

                # It's  a blocklist and the hashtag is found
                if self.credentials['is_blocklist'] and hashtag in self.credentials['hashtags']:
                    exit(0)

                # It is a list of allowed hashtags and the hashtag was not found
                if not self.credentials['is_blocklist'] and hashtag not in self.credentials['hashtags']:
                    exit(0)

                if self.credentials['omit_replies'] and r.json()[0]['in_reply_to_status_id']:
                    # Tweet is a reply
                    exit(0)

            except IndexError:
                # No hashtags, that's fine
                pass

            return r.json()[0]

        except Exception as e:
            message = f"The api call to twitter failed, the server responded:\n'{e}'.\nScript was discontinued."
            mail(message)
            exit(1)
