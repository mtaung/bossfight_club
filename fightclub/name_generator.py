from nltk.corpus import wordnet
import re
import random

prefix = ['savage', 'devastating', 'destructive', 'rapid', 'explosive', 'powerful', 'shining', 'furious', 'royal', 'infinite', 'shocking', 'infernal', 'fatal', 'lethal']
suffix = ['smash', 'slam', 'beam', 'crush', 'punch', 'blast', 'attack', 'burst', 'clash', 'weapon', 'blow', 'bolt', 'rush', 'shot', 'wave', 'dunk', 'massacre']

def related_words(tokens):
    related = set()
    for word in tokens:
        ss = wordnet.synsets(word)
        for s in ss:
            for l in s.lemmas():
                related.add(l.name().replace('_', ' '))
            for h in s.hyponyms():
                for l in h.lemmas():
                    related.add(l.name().replace('_', ' '))
            for h in s.hypernyms():
                for l in h.lemmas():
                    related.add(l.name().replace('_', ' '))
    return related

def tokenize(text):
    return re.findall(r'\b[^\s]+\b', text)

def clamp(i, limit):
    return i if i < limit else limit

def related_name(p, s, token):
    if random.choice([True, False]):
        return (random.choice(p) + ' ' + token).title()
    else:
        return (token + ' ' + random.choice(s)).title()

def generic_name(p, s):
    return (random.choice(p) + ' ' + random.choice(s)).title()

def generate_attack_names(text):
    tokens = set(tokenize(text))
    syns = related_words(tokens)
    sample = random.sample(syns, clamp(len(syns), 4))
    attack_names = []
    for w in sample:
        attack_names.append(related_name(prefix, suffix, w))
    for i in range(4 - len(sample)):
        attack_names.append(generic_name(prefix, suffix))
    return attack_names
