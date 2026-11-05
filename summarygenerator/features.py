"""All the sentence scoring features used to build the feature matrix."""
import collections
import math

from collections import Counter

from .resources import WORD


def tfIsf(tokenized_sentences):
    scores = []
    for sentence in tokenized_sentences :
        counts = collections.Counter(sentence)
        score = 0
        for word in counts.keys() :
            count_word = 1
            for sen in tokenized_sentences :
                for w in sen :
                    if word == w :
                        count_word += 1
            score = score + counts[word]*math.log(count_word-1)
        scores.append(score/max(len(sentence), 1))
    return scores


def similar(tokens_a, tokens_b) :
    #Using Jaccard similarity to calculate if two sentences are similar
    union = set(tokens_a).union(tokens_b)
    if len(union) == 0:
        return 0.0
    return len(set(tokens_a).intersection(tokens_b)) / float(len(union))


def similarityScores(tokenized_sentences) :
    scores = []
    for sentence in tokenized_sentences :
        score = 0
        for sen in tokenized_sentences :
            if sen != sentence :
                score += similar(sentence,sen)
        scores.append(score)
    return scores


def properNounScores(tagged) :
    scores = []
    for i in range(len(tagged)) :
        score = 0
        for j in range(len(tagged[i])) :
            if(tagged[i][j][1]== 'NNP' or tagged[i][j][1]=='NNPS') :
                score += 1
        scores.append(score/float(max(len(tagged[i]), 1)))
    return scores


def text_to_vector(text):
    words = WORD.findall(text)
    return collections.Counter(words)


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def centroidSimilarity(sentences,tfIsfScore) :
    centroidIndex = tfIsfScore.index(max(tfIsfScore))
    scores = []
    for sentence in sentences :
        vec1 = text_to_vector(sentences[centroidIndex])
        vec2 = text_to_vector(sentence)

        score = get_cosine(vec1,vec2)
        scores.append(score)
    return scores


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def numericToken(tokenized_sentences):
    scores = []
    for sentence in tokenized_sentences :
        score = 0
        for word in sentence :
            if is_number(word) :
                score +=1
        scores.append(score/float(max(len(sentence), 1)))
    return scores




def sentencePos(sentences) :
    th = 0.2
    minv = th*len(sentences)
    maxv = th*2*len(sentences)
    pos = []
    for i in range(len(sentences)):
        if i==0 or i==len((sentences)):
            pos.append(0)
        else:
            t = math.cos((i-minv)*((1/maxv)-minv))
            pos.append(t)

    return pos


def sentenceLength(tokenized_sentences) :
    # sentences with less than 3 words get 0, others are divided by the
    # longest sentence (before it was divided by sys.maxsize so everything was 0)
    count = []
    for sentence in tokenized_sentences:
        num_words = len(sentence)
        if num_words < 3 :
            count.append(0)
        else :
            count.append(num_words)

    max_length = max(count) if count and max(count) > 0 else 1
    return [1.0*x/max_length for x in count]


def thematicFeature(tokenized_sentences) :
    word_list = []
    for sentence in tokenized_sentences :
        for word in sentence :
            word = ''.join(e for e in word if e.isalnum())
            word_list.append(word)
    counts = Counter(word_list)
    number_of_words = len(counts)
    most_common = counts.most_common(10)
    thematic_words = []
    for data in most_common :
        thematic_words.append(data[0])
    scores = []
    for sentence in tokenized_sentences :
        score = 0
        for word in sentence :
            word = ''.join(e for e in word if e.isalnum())
            if word in thematic_words :
                score = score + 1
        score = 1.0*score/max(number_of_words, 1)
        scores.append(score)
    return scores
