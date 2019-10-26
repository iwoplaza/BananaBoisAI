import random

global_adjectives = [
    'looks fancy', 'is pretty functional', 'is very useful', 
    'is nice', 'is passable', 'looks fine', 'seems nice', 
    'looking good', 'improves your status', 'is an inspiration for your friends', 
    'is making a difference', 'gives you a new perspective', 'lived more than you think', 
    'has cool color', 'gives a new look to the room', 'makes your area bigger',
    'never let you down', 'will change your life'
]

adjectives = {
    'bed':      [ 'is very comfortable' ],
    'bed' : [ "could make your mornings comfortable" ],
    'chair':    [ "feels like it's been taken straight out of your grandmas house" ],
    'chair':    [   "was approved by the president of the United States" ],
    'coffee table': [ "makes your coffee better" ],
    'fireplace' : [ "warms your heart" ],
    'floor' : [ "is making you stay on the ground" ],
    'real estate': [ "is free" ],
    'toilet' : [ "makes you shit with ease" ],
    'tree' : [ "is just hanging around" ],
    'couch' : [ "makes you relax in the afternoon" ],
    'window' : [ "gives you a new view" ],
    'window' : [ "...always better than apple" ],
    'shower': [ "helps you to get up everyday"],
    'mattress': [ "will make you fall asleep right away" ],
    'nightstand': [ "will help you survive a night" ]
}

labels = {
    'bed': 'bed',
    'chair': 'chair'
}

prefixes = [
    '. The',
]

connector_prefixes = [
    ', and the',
    ', the'
]

fancy_prefixes = [
    '. Furthermore, the',
    '. On top of that, the',
]

def getRandomChoice(src):
    return src[random.choice(range(len(src)))]

def popRandomChoice(src):
    return src.pop(random.choice(range(len(src))))

def getPrefix(statement_index = 0):
    if statement_index > 0 and random.random() < 0.1 and len(fancy_prefixes) != 0:
        return popRandomChoice(fancy_prefixes)
    elif statement_index > 0 and random.random() < 0.5:
        return getRandomChoice(connector_prefixes)
    else:
        return getRandomChoice(prefixes)

def getAdjective(noun):
    totalAdjs = len(global_adjectives + (adjectives[noun] if noun in adjectives else []))

    if totalAdjs == 0:
        return 'is good'
    else:
        weight = len(global_adjectives) / totalAdjs

        pool = global_adjectives if random.random() <= weight else adjectives[noun]
        return popRandomChoice(pool)

def generateDescription(topics):
    random.shuffle(topics)

    description = ''
    index = 0
    for topic in topics:
        prefix = getPrefix(index > 0)

        topic = topic.lower()
        sentence = f'{prefix} {labels[topic] if topic in labels else topic} {getAdjective(topic)}'

        description = description + sentence

        index = index + 1
    return description[2:]

if __name__ == '__main__':
    print(generateDescription([ 'bed', 'chair', 'table' ]))