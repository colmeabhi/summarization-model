import os
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# nltk 3.9 renamed some of the data packages (the *_tab / *_eng ones),
# so we download both old and new names to be safe.
# the value is where nltk keeps it, so we can check if its already there
NLTK_PACKAGES = {
    'punkt': 'tokenizers/punkt',
    'punkt_tab': 'tokenizers/punkt_tab',
    'averaged_perceptron_tagger': 'taggers/averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng': 'taggers/averaged_perceptron_tagger_eng',
    'maxent_ne_chunker': 'chunkers/maxent_ne_chunker',
    'maxent_ne_chunker_tab': 'chunkers/maxent_ne_chunker_tab',
    'words': 'corpora/words',
    'stopwords': 'corpora/stopwords',
}


def download_nltk_data():
    # NLTK_DATA lets us keep the data inside the project folder on the server
    download_dir = os.environ.get('NLTK_DATA')

    for package, path in NLTK_PACKAGES.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, download_dir=download_dir, quiet=True)


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
