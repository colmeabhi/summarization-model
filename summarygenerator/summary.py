import numpy

from .entity import namedEntityRecog
from .feature_enhancer import enhance_features
from .features import (
    centroidSimilarity,
    numericToken,
    properNounScores,
    sentenceLength,
    sentencePos,
    similarityScores,
    tfIsf,
    thematicFeature,
)
from .preprocessing import posTagger, remove_stop_words, split_into_sentences


# how much of the text to keep for each option on the website
SUMMARY_LENGTHS = {
    'short': 0.3,
    'medium': 0.5,
    'long': 0.7,
}

# texts shorter than this are just returned as they are
MIN_SENTENCES = 3


def build_feature_matrix(sentences):
    """Makes a (number of sentences x 8) matrix, one column per feature."""
    tokenized_sentences = remove_stop_words(sentences)
    tagged = posTagger(tokenized_sentences)

    tfIsfScore = tfIsf(tokenized_sentences)

    features = [
        thematicFeature(tokenized_sentences),
        sentencePos(sentences),
        sentenceLength(tokenized_sentences),
        properNounScores(tagged),
        numericToken(tokenized_sentences),
        namedEntityRecog(sentences),
        tfIsfScore,
        centroidSimilarity(sentences, tfIsfScore),
    ]

    # each feature is a row right now, transpose so each sentence is a row
    return numpy.array(features, dtype=float).T


def score_sentences(feature_matrix):
    """Runs the features through the enhancer and adds them up per sentence."""
    enhanced = enhance_features(feature_matrix)
    return numpy.sum(enhanced, axis=1)


def pick_sentences(sentences, scores, ratio):
    """
    Returns the indexes of the sentences to keep, in the original order.
    The first sentence is always kept. The rest are picked from the
    lowest enhanced scores (same as the original project).
    """
    ranked = sorted(range(len(sentences)), key=lambda i: scores[i])
    how_many = max(1, int(len(sentences) * ratio))

    picked = [0]
    for index in ranked[:how_many]:
        if index != 0:
            picked.append(index)

    return sorted(picked)


def summarize(text, ratio=0.5):
    """
    Main function. Takes the text and returns a dict with the summary
    and a few numbers to show on the result page.
    """
    sentences = split_into_sentences(text)

    if len(sentences) < MIN_SENTENCES:
        picked = list(range(len(sentences)))
    else:
        feature_matrix = build_feature_matrix(sentences)
        scores = score_sentences(feature_matrix)
        picked = pick_sentences(sentences, scores, ratio)

    summary_sentences = [sentences[i] for i in picked]

    return {
        'summary': ' '.join(summary_sentences),
        'sentences': summary_sentences,
        'original_count': len(sentences),
        'summary_count': len(summary_sentences),
        'original_words': len(text.split()),
        'summary_words': sum(len(s.split()) for s in summary_sentences),
    }
