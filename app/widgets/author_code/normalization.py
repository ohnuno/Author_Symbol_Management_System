import string
import unicodedata


def normalization(word):
    word = word.lower()
    punctuation = string.punctuation
    punctuation += "ʿ"
    word = word.translate(str.maketrans('', '', punctuation))
    word = unicodedata.normalize('NFKD', word)
    return u"".join([c for c in word if not unicodedata.combining(c)])
