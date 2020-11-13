#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import time


class GroupMe:

    def __init__(self):
        self.bot_ID = "****"
        self.access_token = "***"

    @staticmethod
    def _url(path) -> str:
        """
        Helps format url with correct prefix
        :param path:
        :return:
        """
        return 'https://api.groupme.com/v3{}'.format(path)

    def send_message(self, text_input: str) -> bool:
        """
        Sends  a message to the bot using access token

        ex;
         curl -d '{"text" : "Your message here", "bot_id" : "f1c04db2ff93983a456147dfff"}' https://api.groupme.com/v3/bots/post

        :param text_input:
        :return:
        """
        r = requests.post(self._url("/bots/post"), data={'text': text_input, "bot_id" : self.bot_ID})
        time.sleep(1)
        if r.status_code == requests.codes.ok:
            print("Message sent to bot with success")
            return True
        else:
            print("Message failed to send")
            return False
