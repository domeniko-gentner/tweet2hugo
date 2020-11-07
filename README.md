# Tweet2Hugo

This python script fetches the latest tweet of a public user from twitter and outputs a json file to Hugo's data
directory. This script expects two json files in `/etc/tw2hugo`, which should have `chmod 700` for a non-privileged 
user and no rights for the group. All files should have `chmod 400`.

## Needed configuration files

/etc/tw2hugo/mail_credentials.json
```
{
  "smtp-server": "mail server",
  "smtp-port": 465,
  "email-user": "username for smtp",
  "email-sendfrom": "sender mail",
  "email-password": "passw0rd",
  "email-sendto": "receiving mail"
}
```

/etc/tw2hugo/twitter.json
```
{
    "bearer": "bearer token of your twitter app",
    "twitter-handle": "twitter handle",
    "output-location": "hugo base dir/data/latest_tweet.json"
}
```

## Why does it need email credentials?

The script has the specialty that sends an email when something goes wrong, so I am notifed and can fix the issue.
If you don't want that, simply open `mail/mail.py` and replace everyting in the init function with a simple `pass`.
