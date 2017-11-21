SCORE_TYPES = [
    'Overall',
    'Scientific support',
    'Technical support',
    'Beamline hardware',
    'Beamline software',
    'Machine operation',
    'DUO'
    ]
NAME_HEADERS = ['Beamline', 'Department', 'User Affiliation']
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
VILDE_PICKLE_FILE = 'pickles/vilde.pickle'
WORDVEC_PICKLE_FILE = 'pickles/wordvec.pickle'
DROPTEST = ['Proposal'] + SCORE_TYPES + EXTERNAL_FACTOR_HEADERS + DATE_HEADERS
TARGET = 'Overall'
VARIANCE_THRESHOLD = 0.01
MIN_DF=1
DEFAULT_CONFIG = {
    'target': 'Overall',
    'variance_threshold': 0.001,
    'droplist': ['Proposal'] + SCORE_TYPES + EXTERNAL_FACTOR_HEADERS + DATE_HEADERS
}
NUMBER_DIMENSIONS = 256