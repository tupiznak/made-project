import nltk
from config import NLTK_PATH

nltk.download('stopwords', download_dir=NLTK_PATH)
nltk.download('averaged_perceptron_tagger', download_dir=NLTK_PATH)
nltk.download('punkt', download_dir=NLTK_PATH)
nltk.download('wordnet', download_dir=NLTK_PATH)
nltk.download('omw-1.4', download_dir=NLTK_PATH)
