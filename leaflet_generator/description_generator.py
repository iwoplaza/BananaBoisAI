import random

from array_utils import popRandomChoice, getRandomChoice

class DescriptionGenerator:

    def __init__(self):
        self.global_adjectives_positive = [
            'looks fancy', 'is pretty functional', 'is very useful', 
            'is nice', 'seems nice', 
            'looks good', 'improves your social status', 'is an inspiration for your friends', 
            'really makes a difference', 'gives you a <strong>new perspective</strong>', 'has been around for longer than you think', 
            'has a cool color', 'gives a new look to the room', 'is <strong>spacious</strong>',
            'never lets you down', 'will <strong>change your life</strong>', "is unique in it's design", 'is <strong>free</strong>',
            'wil make you <strong>happier</strong>',  'will make you want to comeback with pleasure', 'is perfectly designed'
        ]

        self.global_adjectives_neutral = [
            'is passable', 'looks fine', 'has neutral design', 'just standing here, I think..',
            'is still functional', 'is nothing spectacular', 'is nothing groundbreaking',
            'could look better', 'has good placement'
        ]

        self.global_adjectives_negative = [
            'is underwhelming', 'has seen better days', 'is barely holding form',
            '.. we really do not know what it is doing here', 'is very neglected',
            'belongs to a museum'
        ]

        self.adjectives_positive = {
            'bed':          [ 'is very comfortable', 'could make your mornings more comfortable' ],
            'chair':        [ "was approved by the president of the United States" ],
            'coffee table': [ "makes your coffee better" ],
            'fireplace' :   [ "warms your heart" ],
            'floor' :       [ ],
            'real estate':  [ "is free" ],
            'toilet' :      [ ],
            'tree' :        [ ],
            'couch' :       [ "makes you relax in the afternoon" ],
            'window' :      [ "gives you a new view", "...always better than apple" ],
            'shower':       [ "helps you to get up everyday"],
            'mattress':     [ "will make you fall asleep right away" ],
            'nightstand':   [ ]
        }

        self.adjectives_neutral = {
            'bed':          [ ],
            'chair':        [ "feels like it's been taken straight out of your grandmas house" ],
            'coffee table': [ ],
            'fireplace' :   [ ],
            'floor' :       [ "is making you stay on the ground" ],
            'real estate':  [ ],
            'toilet' :      [ ],
            'tree' :        [ "is just hanging around" ],
            'couch' :       [ ],
            'window' :      [ ],
            'shower':       [ ],
            'mattress':     [ ],
            'nightstand':   [ "will help you survive a night" ]
        }

        self.adjectives_negative = {
            'bed':          [ 'feels soggy and hard at the same time' ],
            'coffee table': [ ],
            'fireplace' :   [ 'is a fire hazard waiting to happen' ],
            'floor' :       [ "doesn't look like something that should be able to support anyone's weight" ],
            'real estate':  [ ],
            'toilet' :      [ ],
            'tree' :        [ ],
            'couch' :       [ ],
            'window' :      [ ],
            'shower':       [ ],
            'mattress':     [ ],
            'nightstand':   [ ]
        }

        self.labels = {
            'bed': 'bed',
            'chair': 'chair'
        }

        self.prefixes = [
            '. The',
            '. The',
            '. The',
            '. The',
            '! The',
        ]

        self.connector_prefixes = [
            ', and the',
            ', the'
        ]

        self.fancy_prefixes = [
            '. Furthermore, the',
            '. On top of that, the',
            '. Oh, and the'
        ]

    def getPrefix(self, statement_index = 0):
        if statement_index > 0 and random.random() < 0.1 and len(self.fancy_prefixes) != 0:
            return popRandomChoice(self.fancy_prefixes)
        elif statement_index > 0 and random.random() < 0.5:
            return getRandomChoice(self.connector_prefixes)
        else:
            return getRandomChoice(self.prefixes)

    def getGlobalAdjectivePool(self, score):
        return self.global_adjectives_positive if score > 0.7 else self.global_adjectives_neutral if score > 0.3 else self.global_adjectives_negative

    def getAdjectivePool(self, score):
        return self.adjectives_positive if score > 0.7 else self.adjectives_neutral if score > 0.3 else self.adjectives_negative

    def getAdjective(self, noun, score = 0.5):
        global_adjectives = self.getGlobalAdjectivePool(score)
        adjectives = self.getAdjectivePool(score)
        totalAdjs = len(global_adjectives + (adjectives[noun] if noun in adjectives else []))

        if totalAdjs == 0:
            return 'is good'
        else:
            weight = len(global_adjectives) / totalAdjs

            pool = global_adjectives if random.random() <= weight else adjectives[noun]
            return popRandomChoice(pool)

    def generate(self, topics, excludedTags):
        random.shuffle(topics)

        description = ''
        index = 0
        for (topic, score) in topics:
            topic = topic.lower()
            if topic in excludedTags:
                continue

            prefix = self.getPrefix(index > 0)

            sentence = f'{prefix} {self.labels[topic] if topic in self.labels else topic} {self.getAdjective(topic, score)}'

            description = description + sentence

            index = index + 1
        return description[2:] + '.'

if __name__ == '__main__':
    generator = DescriptionGenerator()
    print(generator.generate([ 'bed', 'chair', 'table' ], []))