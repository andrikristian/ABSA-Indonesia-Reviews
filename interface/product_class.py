#import module User_Interface
from User_Setting_Interface import *

#Libraries for web scraping
#**
from bs4 import BeautifulSoup
import requests
import sys
#**

#Libraries for generating synonyms
#**
sys.path.insert(0,synonyms_generator_path)
from synonyms_generator import process, args
#**

#Libraries for translation
#**
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS_path
from google.cloud import translate
#**

#Libraries for sentiment analysis
#**
sys.path.insert(0,ABSA_path)
from infer_example import Inferer, opt
#**

#other Libraries
#**
import re
#**

class Product:
    def __init__(self, reviews_web_link, ls_input_aspects_1, ls_input_aspects_2, ls_input_aspects_3, ls_aspect_terms_1, ls_aspect_terms_2, ls_aspect_terms_3):
        self.reviews_web_link = reviews_web_link
        self.original_review_texts = self.scrape_review_texts()
        self.translated_review_texts = [self.translate_text(original_review_text,target='en') for original_review_text in self.original_review_texts]
        
        #split/chunk reviews based on the punctuation marks below
        self.chunked_review_texts = [re.split(',|\.|-|\[|',review_text) for review_text in self.translated_review_texts]

        if ls_aspect_terms_1 == None:
            self.ls_aspect_terms_1 = self.synonyms_generator(ls_input_aspects_1)
        else:
            self.ls_aspect_terms_1 = ls_aspect_terms_1

        if ls_aspect_terms_2 == None:
            self.ls_aspect_terms_2 = self.synonyms_generator(ls_input_aspects_2)
        else:
            self.ls_aspect_terms_2 = ls_aspect_terms_2

        if ls_aspect_terms_3 == None:
            self.ls_aspect_terms_3 = self.synonyms_generator(ls_input_aspects_3)
        else:
            self.ls_aspect_terms_3 = ls_aspect_terms_3


        self.ls_ls_relevant_review_chunks_aspect_1 = self.search_relevant_chunks(self.ls_aspect_terms_1, self.chunked_review_texts)
        self.ls_ls_relevant_review_chunks_aspect_2 = self.search_relevant_chunks(self.ls_aspect_terms_2, self.chunked_review_texts)
        self.ls_ls_relevant_review_chunks_aspect_3 = self.search_relevant_chunks(self.ls_aspect_terms_3, self.chunked_review_texts)

        self.ls_ls_prob_positive_sentiment_aspect_1 = self.prob_positive_sentiment(self.ls_ls_relevant_review_chunks_aspect_1, self.ls_aspect_terms_1)
        self.ls_ls_prob_positive_sentiment_aspect_2 = self.prob_positive_sentiment(self.ls_ls_relevant_review_chunks_aspect_2, self.ls_aspect_terms_2)
        self.ls_ls_prob_positive_sentiment_aspect_3 = self.prob_positive_sentiment(self.ls_ls_relevant_review_chunks_aspect_3, self.ls_aspect_terms_3)

        self.sentiment_score_aspect_1 = self.sentiment_scoring(self.ls_ls_prob_positive_sentiment_aspect_1)
        self.sentiment_score_aspect_2 = self.sentiment_scoring(self.ls_ls_prob_positive_sentiment_aspect_2)
        self.sentiment_score_aspect_3 = self.sentiment_scoring(self.ls_ls_prob_positive_sentiment_aspect_3)


    #function to average the sentiment scores and output sentiment polarity and its extent 
    def sentiment_scoring(self, ls_ls_prob_positive_sentiment_by_aspect):
        print("enter sentiment_scoring!")

        ls_prob = []

        for ls in ls_ls_prob_positive_sentiment_by_aspect:
            for element in ls:
                ls_prob.append(element)

        if len(ls_prob) == 0:
            return "NA"

        ls_prob_negative_sentiment = []
        for ls in ls_prob:
            ls_prob_negative_sentiment.append(ls[0])


        ls_prob_neutral_sentiment = []
        for ls in ls_prob:
            ls_prob_neutral_sentiment.append(ls[1])


        ls_prob_positive_sentiment = []
        for ls in ls_prob:
            ls_prob_positive_sentiment.append(ls[2])

        if len(ls_prob_positive_sentiment) == 0:
            return "NA"

        ls_average_prob_negative_sentiment = sum(ls_prob_negative_sentiment) / len(ls_prob_negative_sentiment)
        ls_average_prob_neutral_sentiment = sum(ls_prob_neutral_sentiment) / len(ls_prob_neutral_sentiment)
        ls_average_prob_positive_sentiment = sum(ls_prob_positive_sentiment) / len(ls_prob_positive_sentiment)


        if ls_average_prob_negative_sentiment > ls_average_prob_neutral_sentiment and ls_average_prob_negative_sentiment > ls_average_prob_positive_sentiment:
            difference = ls_average_prob_negative_sentiment - max([ls_average_prob_neutral_sentiment, ls_average_prob_positive_sentiment])
            extent = difference * 5

            if extent <= 2:
                return "weak negative"

            if extent > 2 and extent < 4:
                return "moderate negative"

            if extent >= 4:
                return "strong negative"

        if ls_average_prob_neutral_sentiment > ls_average_prob_negative_sentiment and ls_average_prob_neutral_sentiment > ls_average_prob_positive_sentiment:
            difference = ls_average_prob_neutral_sentiment - max([ls_average_prob_negative_sentiment, ls_average_prob_positive_sentiment])
            extent = difference * 5

            if extent <= 2:
                return "weak neutral"

            if extent > 2 and extent < 4:
                return "moderate neutral"

            if extent >= 4:
                return "strong neutral"

        if ls_average_prob_positive_sentiment > ls_average_prob_negative_sentiment and ls_average_prob_positive_sentiment > ls_average_prob_neutral_sentiment:
            difference = ls_average_prob_positive_sentiment - max([ls_average_prob_negative_sentiment, ls_average_prob_neutral_sentiment])
            extent = difference * 5

            if extent <= 2:
                return "weak positive"

            if extent > 2 and extent < 4:
                return "moderate positive"

            if extent >= 4:
                return "strong positive"

    #input the relevant chunk and its aspect term to the deep learning ABSA model
    def prob_positive_sentiment(self, review_chunks, aspect_terms):
        ls_ls_prob_positive_sentiment_by_aspect = []
        sentiment_inferer = Inferer(opt)
        for idx,aspect_term in enumerate(aspect_terms):
            ls_prob_positive_sentiment = []
            for chunk in review_chunks[idx]:
                dummy_ls_sentiment = []
                dummy_ls_sentiment.append(sentiment_inferer.evaluate([chunk], aspect_term)[0][0])
                dummy_ls_sentiment.append(sentiment_inferer.evaluate([chunk], aspect_term)[0][1])
                dummy_ls_sentiment.append(sentiment_inferer.evaluate([chunk], aspect_term)[0][2])
                ls_prob_positive_sentiment.append(dummy_ls_sentiment)
            ls_ls_prob_positive_sentiment_by_aspect.append(ls_prob_positive_sentiment)
        return ls_ls_prob_positive_sentiment_by_aspect

    #search for chunks that contain the aspect terms input by the user and its synonyms
    def search_relevant_chunks(self, ls_aspect_terms, chunked_review_texts):
        ls_ls_relevant_chunks_by_aspect = []
        dummy_chunked_review_texts = []
        dummy_chunked_review_texts += chunked_review_texts

        for aspect_term in ls_aspect_terms:
            ls_relevant_chunks = []
            for review_text in dummy_chunked_review_texts:
                for idx,chunk in enumerate(review_text):
                    if 'Good]' in chunk:
                        chunk = chunk.replace('Good]', '')
                    if 'Bad]' in chunk:
                        chunk = chunk.replace('Bad]', '')
                    if aspect_term in chunk:
                        ls_relevant_chunks.append(chunk)
                        review_text[idx] = ''
            ls_ls_relevant_chunks_by_aspect.append(ls_relevant_chunks)

        return ls_ls_relevant_chunks_by_aspect

    def scrape_review_texts(self):

        page = requests.get(self.reviews_web_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        review_list = soup.find(class_="reviewList")
        review_texts_raw = [review_text.get_text() \
                            for review_text in review_list.select(".itemReviewBox .reviewIn .reviewText")]
        review_texts_clean = []
        for review_text_raw in review_texts_raw:
            review_texts_clean.append(review_text_raw[
                                      self.substr_find_nth(review_text_raw, '\n', 2) + 1: self.substr_find_second_last(
                                          review_text_raw, '\n')])

        return review_texts_clean

    def synonyms_generator(self, ls_input_aspects):
        aspect_terms = []
        aspect_terms += ls_input_aspects
        for aspect in ls_input_aspects:
            synonyms_generated = process(aspect,args.num_output)
            aspect_terms += synonyms_generated
            
        aspect_terms_with_space = []
        #add space in front and behind the aspect term
        for aspect_term in aspect_terms:
            aspect_term_with_space = ' ' + aspect_term + ' '
            aspect_terms_with_space.append(aspect_term_with_space)

        return aspect_terms_with_space

    #translation function
    def translate_text(self, text, target='en'):
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=target)
        return result['translatedText']

    #string manipulation
    def substr_find_nth(self, haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start + len(needle))
            n -= 1
        return start

    #string manipulation
    def substr_find_second_last(self, text, pattern):
        return text.rfind(pattern, 0, text.rfind(pattern))
