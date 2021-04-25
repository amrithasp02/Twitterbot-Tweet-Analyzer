import wikipedia
from wordcloud import WordCloud, STOPWORDS
import os
from PIL import Image
import numpy as np

currdir = os.path.dirname(__file__)


def create_wordcloud(text):

    mask = np.array(Image.open(os.path.join(currdir, "cloud.png")))

    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color='white', mask=mask, max_words=200, stopwords=stopwords)
    wc.generate(text)
    wc.to_file(os.path.join(currdir, "wc.png"))
