# SaralGyaan Reddit Twitter Bot

This is a twitter bot by reddit user [Udit Vashisht](https://www.reddit.com/user/uditvashisht) will take hot posts from the following sub-reddits and post them on [twitter](https://twitter.com/saral_gyaan) :-
* ProgrammerHumor
* ProgrammingMemes
* XKCD

## Prerequisites

* A twitter account alongwith consumer keys and access tokens, used for OAuth. You can get them from [here](https://developer.twitter.com)
* A reddit account alongwith client id and secret. You can get them frome here (https://reddit.com/prefs/apps)

## Requirements

* Python 3.6 or above (As the code uses [f-strings](https://saralgyaan.com/posts/f-string-in-python-usage-guide/))
* tweepy
* PRAW
* python-decouple
* requests

You can use the following command to install all the requisite modules:-
`pip install -r requirements.txt`

## Installation

Either download the directory from github or clone it using:-

`git clone https://github.com/uditvashisht/SaralGyaanTwitterRedditBot.git`

```
cd SaralGyaanTwitterRedditBot
python3 -m venv . #You can use python or python3 or python3.6 depending on your system
source bin/activate
pip install -r requirements.txt
```

## Usage

Create a .env file and add your credentials

```
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USERNAME=
REDDIT_PASSWORD=
TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
```
You can run the bot by using

``` python social-update.py```

## License
© 2021 Udit Vashisht This repository is licensed under the MIT license. See LICENSE for details.
