import random
import re
import json
import torch

all_tweets = json.load(open('./data/tweets.txt'))

def make_dataset(dataset, epochs):
    total_text = '<|endoftext|>'
    tweets = [t for t in dataset]
    for _ in range(epochs):
        random.shuffle(tweets)
        total_text += '<|endoftext|>'.join(tweets) + '<|endoftext|>'
    return total_text


# shuffle data
random.shuffle(all_tweets)

# fraction of training data
split_train_valid = 0.9

# split dataset
train_size = int(split_train_valid * len(all_tweets))
valid_size = len(all_tweets) - train_size
train_dataset, valid_dataset = torch.utils.data.random_split(all_tweets, [train_size, valid_size])

EPOCHS = 4

with open('./data/train.txt', 'w') as f:
    data = make_dataset(train_dataset, EPOCHS)
    f.write(data)

with open('./data/valid.txt', 'w') as f:
    data = make_dataset(valid_dataset, 1)
    f.write(data)