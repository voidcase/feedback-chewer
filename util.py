SCORE_TYPES = [
    'Overall',
    'Scientific support',
    'Technical support',
    'Beamline hardware',
    'Beamline software',
    'Machine operation',
    'DUO'
    ]

DATE_HEADERS = ['Experiment start', 'Experiment end', 'Report submitted']
EXTERNAL_FACTOR_HEADERS = ['Department', 'User Affiliation'] + DATE_HEADERS

TEXT_HEADERS_AND_SUFFIXES = [
    ('Experiment comments', '_ec'),
    ('Infrastructure comment', '_ic'),
    ('Overall comments', '_oc'),
    ('Remarks', '_r')
]
TEXT_HEADERS = [h[0] for h in TEXT_HEADERS_AND_SUFFIXES]
DATASET_PATH = 'datasets/'
FEEDBACK_DATA = DATASET_PATH + 'feedback.csv'
POSITIVE_DATA = DATASET_PATH + 'positive_words_utf8.txt'
NEGATIVE_DATA = DATASET_PATH + 'negative_words_utf8.txt'
WORDVEC_DATA = DATASET_PATH + 'word_vectors.txt'
AMAZON_DATA = DATASET_PATH + 'reviews_Electronics_5.json'
VILDE_PICKLE_FILE = 'pickles/vilde.pickle'
WORDVEC_PICKLE_FILE = 'pickles/wordvec.pickle'
OWN_WORDVEC_PICKLE_FILE = 'pickles/ownwordvec.pickle'
AUTOCORRECT_PICKLE_FILE = 'pickles/autocorrect.pickle'
COEFF_PICKLE = 'pickles/coeff.pickle'
STMTS_PICKLE = 'pickles/stmts.pickle'
MIN_DF= 0.01
DEFAULT_CONFIG = {
    'target': 'Overall',
    'variance_threshold': 0.001,
    'droplist': ['Proposal'] + SCORE_TYPES + EXTERNAL_FACTOR_HEADERS + DATE_HEADERS
}
NUMBER_DIMENSIONS = 256
SCOREPAIRS =[(['Overall comments',  'Remarks'], ['Overall']),
             (['Infrastructure comment'],['DUO']),
             (['Experiment comments'],
              ['Scientific support', 'Technical support',
                                     'Beamline hardware',
                                     'Beamline software',
                                     'Machine operation'])
             ]