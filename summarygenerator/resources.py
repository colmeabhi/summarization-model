import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# nltk 3.9 renamed some of the data packages (the *_tab / *_eng ones),
# so we download both old and new names to be safe
NLTK_PACKAGES = [
    'punkt',
    'punkt_tab',
    'averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng',
    'maxent_ne_chunker',
    'maxent_ne_chunker_tab',
    'words',
    'stopwords',
]


def download_nltk_data():
    for package in NLTK_PACKAGES:
        nltk.download(package, quiet=True)


download_nltk_data()

porter = PorterStemmer()
stop = set(stopwords.words('english'))

WORD = re.compile(r'\w+')

# regex pieces used when splitting text into sentences
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = r"(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
