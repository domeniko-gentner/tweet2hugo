# Tweet2Hugo

This python script fetches the latest tweet of a public user from twitter and outputs a json file to Hugo's data
directory. This script expects two json files in `/etc/tw2hugo`, which should have `chmod 700` for a non-privileged 
user and no rights for the group. All files should have `chmod 400`.

## Setup

This package depends only on the pip package "requests", which I recommend to simply install globally with 
`pip3 install requests`. You can also use the provided pipfile and install all dependencies into a virtual environment 
with `pipenv lock`, however, you will need to activate that environment in your automation script.

Next, you will need to install the configuration files below:

## Needed configuration files

/etc/tw2hugo/mail_credentials.json
```
{
  "enable": true,
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
    "output-location": "/hugo/project/directory/data/latest_tweet.json",
    "is_blocklist": true,
    "hashtags": [
        "dontincludethishastag",
        "politics"
    ],
    "omit_replies": true
}
```

## Why does it need email credentials?

The script has the specialty that sends an email when something goes wrong, so I am notifed and can fix the issue.
If you don't want that, replace `enable: true` in the `mail_credentials.json` with `false`.

## How does it integrate into Hugo?

It puts the full json reply from twitter into the data directory, if correctly configured. From there you can do two
things:

* Automate the build (strongly recommended)
* Build a template that uses the json data to build a twitter card.

I build the template using a [partial template](https://gohugo.io/templates/partials/#readout). It sits in the directory
`layouts/partials` and is called `latest_tweet.html`. The content is not very interesting:

```
<div class="box has-text-white brdr-yayellow bg-darkslate">
    <div class="content p-4">
        {{ with .Site.Data.latest_tweet }}
        <div class="columns">
            <div class="column is-half is-offset-one-quarter">
                <figure class="image is-128x128 is-centered">
                     <img class="is-rounded" src="/images/twitter_profile.webp">
                </figure>
            </div>
        </div>
        <p class="has-text-centered">
            <a target="_blank" rel="nofollow noreferrer noopener" href="https://twitter.com/{{.user.name}}">
                @{{ .user.name }}
            </a>
        </p>
        <hr class="twitter-hr">
        <p class="mt-5 has-text-justified">
            {{ .full_text | safeHTML }}
        </p>
        <hr class="twitter-hr">

        <div class="level mb-0">
            <span class="level-left">
                <a target="_blank" 
                   rel="nofollow noreferrer noopener" 
                   href="https://twitter.com/{{.user.name}}/status/{{.id_str}}">{{ slicestr .created_at 0 20 }}
                </a>
            </span>
            <span class="level-right">
               via {{ .source | safeHTML }}
            </span>
        </div>
        <hr class="twitter-hr">
        <div class="level">
            <span class="level-item is-size-4 mr-5">
                <a href="https://twitter.com/intent/like?tweet_id={{.id_str}}">
                    <span class="icon"><i class="fas fa-heart"></i></span>
                </a>
            </span>
            <span class="level-item is-size-4 mr-5">
                <a href="https://twitter.com/intent/retweet?tweet_id={{.id_str}}">
                    <span class="icon"><i class="fas fa-retweet"></i></span>
                </a>
            </span>
            <span class="level-item is-size-4 mr-5">
                <a href="https://twitter.com/intent/tweet?in_reply_to={{.id_str}}">
                    <span class="icon"><i class="fas fa-reply"></i></span>
                </a>
            </span>
        </div>
        {{ end }}
    </div>
</div>
```

The important bit is this go template instruction:

```
{{ with .Site.Data.latest_tweet }}
{{ end }}
```

Between these you can call the keys from the json, so `name` in dict `user` becomes simply `{{ .user.name }}`.    
Neato, isn't it? If you want to know how it looks like, head over to my [website](https://tuxstash.de/) and scroll down
to the footer.

## Excluding hashtags

Sometimes you do not want a tweet to decorate the hard work you call your web home. 
You can edit the following in `twitter.json` to exclude certain hashtags:

```
"is_blocklist: true,
"exclude": [
    "politics"
]
```

**Note**: If `is_blocklist` is false, then it acts as a list of allowed hashtags and will only output new json
if the hashtag is found.

You find sample configuration files in the `/etc/` folder in the project root.

<!--suppress HtmlDeprecatedAttribute -->
<p align="center">
<a href='https://ko-fi.com/L3L31HXRQ' target='_blank'><img height='36' style='border:0;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi2.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
</p>
