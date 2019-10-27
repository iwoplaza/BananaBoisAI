import random

def getRandomChoice(src):
    return src[random.choice(range(len(src)))]

def popRandomChoice(src):
    return src.pop(random.choice(range(len(src))))