'''
Natural Language Processing (NLP)
Python Package :NLTK

Source: https://realpython.com/nltk-nlp-python/

Tokenizing:
By tokenizing, you can conveniently split up text by word or by sentence. 
This will allow you to work with smaller pieces of text that are still relatively coherent and meaningful even outside of the context of the rest of the text.
It’s your first step in turning unstructured data into structured data, which is easier to analyze.

'''
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

example_string = """Muad'Dib learned rapidly because his first training was in how to learn. And the first lesson of all was the basic trust that he could learn.It's shocking to find how many people do not believe they can learn, and how many more believe learning to be difficult."""

print(sent_tokenize(example_string))

print(word_tokenize(example_string))

'''
Stop words are words that you want to ignore, so you filter them out of your text when you’re processing it.
'''

# nltk.download('stopwords')

worf_quote = "Sir, I protest. I am not a merry man!"

words_in_quote = word_tokenize(worf_quote)
print(words_in_quote)

stop_words = set(stopwords.words('english'))

filtered_list = []

for word in words_in_quote:
    if word.casefold() not in stop_words: ## .casefold() return strings in lowercase 
        filtered_list.append(word)

'''
Stemming is a text processing task in which you reduce words to their root, which is the core part of a word. For example, the words “helping” and “helper” share the root “help.” Stemming allows you to zero in on the basic meaning of a word rather than all the details of how it’s being used. 
'''

from nltk.stem import PorterStemmer


stemmer = PorterStemmer()

string_for_stemming = '''The crew of the USS Discovery discovered many discoveries. Discovering is what explorers do.'''
words = word_tokenize((string_for_stemming))

print(words)

stemmed_words = [stemmer.stem(word) for word in words]

print(stemmed_words)

'''
Understemming happens when two related words should be reduced to the same stem but aren’t. This is a false negative.
Overstemming happens when two unrelated words are reduced to the same stem even though they shouldn’t be. This is a false positive.
'''


'''
Part of speech is a grammatical term that deals with the roles words play when you use them together in sentences. Tagging parts of speech, or POS tagging, is the task of labeling the words in your text according to their part of speech.

'''

segan_quote = "If you wish to make an apple pie from scratch,you must first invent the universe"

words_in_segan_quote = word_tokenize(segan_quote)

# nltk.download('averaged_perceptron_tagger')
print(nltk.pos_tag(words_in_segan_quote))

'''JJ = adj, NN = noun, RB = adv, PRP = pronuns, VB = verbs'''


'''
Like stemming, lemmatizing reduces words to their core meaning, but it will give you a complete English word that makes sense on its own instead of just a fragment of a word like 'discoveri'.
'''

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


# nltk.download('wordnet')
print(lemmatizer.lemmatize("scarves"))

string_for_lemmatizing = "The friends of DeSoto love scarves."

words = word_tokenize(string_for_lemmatizing)

lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

print(lemmatized_words)

print(lemmatizer.lemmatize("worst", pos ="a"))

'''
pos (str) – The Part Of Speech tag. Valid options are “n” for nouns, “v” for verbs, “a” for adjectives, “r” for adverbs and “s” for satellite adjectives.
'''

'''
'While tokenizing allows you to identify words and sentences, chunking allows you to identify phrases.
'''

lotr_quote = "It's a dangerous business, Frodo, going out your door."

words_in_quote = word_tokenize((lotr_quote))

# nltk.download("average_perceptron_tagger")
lotr_pos_tags = nltk.pos_tag(words_in_quote)

print(lotr_pos_tags)
''' need to review regular expression'''

grammar = "NP: {<DT>?<JJ>*<NN>}" ## Create chunk grammar with one regular expression rule:

chunk_parser = nltk.RegexpParser(grammar)

tree= chunk_parser.parse(lotr_pos_tags)

tree.draw()