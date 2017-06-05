import codecs

from sentoken import sentences


# Function to read the news data
def read_data(filename):
    # the filename containing news be the argument passed
    f = codecs.open(filename, "r", encoding='utf-8')
    sfile = f.read()
    text = sfile.encode('utf-8')
    return text

# Create Sentence Object
sentclass = sentences()

# sys.argv[1] is the 2nd argument to python execution.
news = read_data('news.txt')

# Split the news into sentences [pre-processing]
sentlist = sentclass.split_into_sentences(news.decode('utf-8'))
