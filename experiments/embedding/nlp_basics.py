import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words("english"))
nltk.download('punkt_tab')
nltk.download('words')
nltk.download('wordnet')
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
from nltk import ne_chunk
nltk.download('averaged_perceptron_tagger_eng')
import re
nltk.download('maxent_ne_chunker_tab')

# 1. Tokenization and Text Cleaning
text = "NLP is amazing! Let's explore its wonders."
tokens = nltk.word_tokenize(text)
cleaned_tokens = [word.lower() for word in tokens if word.isalpha()]
print(cleaned_tokens)

# 2. 2. Stop Words Removing:
filtered_sentence = [word for word in cleaned_tokens if word not in stop_words]
print(filtered_sentence)


 # 3. Stemming and Lemmatizing
#  Stemming: Reducing to Root Forms 
# Lemmatization: Transforming to Dictionary Form

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

stemmed_words = [stemmer.stem(word) for word in filtered_sentence]
lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_sentence]

print(stemmed_words)
print(lemmatized_words)

# 4. Part-of-Speech Tagging:

pos_tags = nltk.pos_tag(filtered_sentence)
print(pos_tags)

# 5. Named Entity Recognition (NER):

ner_tags = ne_chunk(pos_tags)
print(ner_tags)

# 6. 
def clean_tweet(tweet):
    tweet = re.sub(r'@\w+', '', tweet)  # Remove mentions
    tweet = re.sub(r'#\w+', '', tweet)  # Remove hashtags
    tweet = re.sub(r'http\S+', '', tweet)  # Remove URLs
    return tweet

tweet = "Loving the new #iPhone! Best phone ever! @Apple"
clean_tweet(tweet)