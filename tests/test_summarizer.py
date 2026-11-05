from summarygenerator import summarize
from summarygenerator.preprocessing import split_into_sentences


SAMPLE = (
    'Highways are lines of communication. They connect cities and towns. '
    'In 2020, over 5 million people used the National Highway every day. '
    'Roads also help trade grow. Experts say this will boost the economy.'
)


def test_split_into_sentences():
    sentences = split_into_sentences('Hello there. Mr. Smith went to Washington. Bye')
    assert sentences == ['Hello there.', 'Mr. Smith went to Washington.', 'Bye']


def test_summary_is_shorter():
    result = summarize(SAMPLE, 0.3)
    assert result['summary_count'] < result['original_count']
    assert result['summary'].startswith('Highways are lines of communication.')


def test_same_text_gives_same_summary():
    assert summarize(SAMPLE)['summary'] == summarize(SAMPLE)['summary']


def test_short_text_is_returned_as_is():
    assert summarize('Only one sentence here.')['summary'] == 'Only one sentence here.'


def test_stopwords_only_text_does_not_crash():
    result = summarize('The. A. An. Of. To.')
    assert result['summary_count'] >= 1
