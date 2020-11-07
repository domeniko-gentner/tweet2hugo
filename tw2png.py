import requests
from pathlib import Path
from platform import system
from json import load as j_load
from mail import mail

get_last_id_url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=GothSeidank&count=1&trim_user=1"
# get_tweet_url = "https://api.twitter.com/2/tweets/1324994969590001666"


if system().lower() == "windows":
    path = Path("bearer.json")
else:
    path = Path("/etc/twpng/bearer.json")

    try:
        with path.open('r') as fp:
            credentials = j_load(fp)
    except FileNotFoundError:
        mail("Could not find bearer token file! Script was discontinued.")
        exit(1)

try:
    header = {
        "Authorization": f"Bearer {credentials['bearer']}"
    }

    r = requests.get(url=get_last_id_url, headers=header)
    r.raise_for_status()

except Exception as e:
    message = f"The api call to twitter failed and requests said:\n'{e}'. Script was discontinued."
    mail(message)
    exit(1)


