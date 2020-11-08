#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /**********************************************************************************
#  * _author  : Domeniko Gentner
#  * _mail    : code@tuxstash.de
#  * _repo    : https://git.tuxstash.de/gothseidank/tweet2png
#  * _license : This project is under MIT License
#  *********************************************************************************/
from email.mime.text import MIMEText
from json import load as j_load
from pathlib import Path
from platform import system
from smtplib import SMTP_SSL, SMTPHeloError, SMTPAuthenticationError, SMTPException
from ssl import create_default_context


class mail:

    def __init__(self, what: str):

        if system().lower() == "windows":
            path = Path("mail_credentials.json")
        else:
            path = Path("/etc/tw2hugo/mail_credentials.json")

        with path.open("r") as fp:
            credentials = j_load(fp)

        if not credentials['enable']:
            return

        message = MIMEText(what, _charset='utf8')
        message['Subject'] = "Tweet2Hugo alarm report"
        message['From'] = credentials['email-sendfrom']
        message['To'] = credentials['email-sendto']

        try:
            with SMTP_SSL(host=credentials['smtp-server'],
                          port=credentials['smtp-port'],
                          context=create_default_context()) as server:
                server.login(user=credentials['email-user'], password=credentials['email-password'])
                server.sendmail(to_addrs=credentials['email-sendto'],
                                msg=message.as_string(),
                                from_addr=credentials['email-sendfrom'])

        except SMTPHeloError as helo:
            print(f"SMTPHeloError: {helo}")
        except SMTPAuthenticationError as auth_error:
            print(f"Authentication Error: {auth_error}")
        except SMTPException as e:
            print(f"SMTPException: {e}")

