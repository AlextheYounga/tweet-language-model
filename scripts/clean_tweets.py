import re
import json
import sys

TWEETS_FILE="./storage/old_deleted_tweets.txt"
OUTPUT_FILE="./data/tweets.txt"


def boring_tweet(tweet):
    "Check if this is a boring tweet"
    boring_stuff = ['http', '@', '#']
    not_boring_words = len([None for w in tweet.split() if all(bs not in w.lower() for bs in boring_stuff)])
    return not_boring_words < 3

def retweet(tweet):
    return 'RT @' in tweet

def fix_text(text):
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    return text


def clean_tweet(tweet, allow_new_lines = False):
    bad_start = ['http:', 'https:']
    for w in bad_start:
        tweet = re.sub(f" {w}\\S+", "", tweet)      # removes white space before url
        tweet = re.sub(f"{w}\\S+ ", "", tweet)      # in case a tweet starts with a url
        tweet = re.sub(f"\n{w}\\S+ ", "", tweet)    # in case the url is on a new line
        tweet = re.sub(f"\n{w}\\S+", "", tweet)     # in case the url is alone on a new line
        tweet = re.sub(f"{w}\\S+", "", tweet)       # any other case?
    tweet = re.sub(' +', ' ', tweet)                # replace multiple spaces with one space (makes the previous work worthless?)
    if not allow_new_lines:                         # Predictions seem better without new lines
        tweet = ' '.join(tweet.split())
    return tweet.strip()
    

def collect_tweets(): 
    tweets = []
    with open(TWEETS_FILE) as file:
        for line in file:
            if ("Tweet: " in line):
                tweet = line.replace('Tweet: ', '')
                fixed_tweet = fix_text(tweet)
                cleaned_tweet = clean_tweet(fixed_tweet)
                
                if (retweet(tweet)): continue
                if (boring_tweet(cleaned_tweet)): continue

                tweets.append(cleaned_tweet)
    print(f"{len(tweets)} tweets collected.")
    with open(OUTPUT_FILE, 'w') as filehandle:
        json.dump(tweets, filehandle)

collect_tweets()