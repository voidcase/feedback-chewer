import maxiv_data

data_set = maxiv_data.get_set()

superdupermegacomment = ""
for c in data_set['text']:
    superdupermegacomment += c

def gensimtest():
    from gensim.summarization import summarize, keywords

    print("summary:\n", summarize(superdupermegacomment, ratio=0.005))
    print("\nkeywords:\n",keywords(superdupermegacomment,lemmatize=True,ratio=0.005))

def sumytest():
    from sumy.summarizers.lsa import LsaSummarizer as Summarizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.utils import get_stop_words
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.parsers.plaintext import PlaintextParser
    lang = "english"
    parser = PlaintextParser.from_string(superdupermegacomment, Tokenizer(lang))
    stemmer = Stemmer(lang)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(lang)

    for sentence in summarizer(parser.document, 5):
        print(sentence,'\n')

gensimtest()