#import and run sentiment analysis system
from sentiment_analysis_class import Product
from User_Setting_Interface import *
import pandas as pd

product_1 = Product(reviews_link_product_1, list_aspect_1, list_aspect_2, list_aspect_3, None, None, None)
product_2 = Product(reviews_link_product_2, list_aspect_1, list_aspect_2, list_aspect_3, product_1.ls_aspect_terms_1, product_1.ls_aspect_terms_2, product_1.ls_aspect_terms_3)
product_3 = Product(reviews_link_product_3, list_aspect_1, list_aspect_2, list_aspect_3, product_1.ls_aspect_terms_1, product_1.ls_aspect_terms_2, product_1.ls_aspect_terms_3)

print('Product 1: \n')
print(product_1.translated_review_texts)
print(product_1.chunked_review_texts)
print(product_1.ls_aspect_terms_1)
print(product_1.ls_aspect_terms_2)
print(product_1.ls_aspect_terms_3)
print(product_1.ls_ls_relevant_review_chunks_aspect_1)
print(product_1.ls_ls_prob_positive_sentiment_aspect_1)
print(product_1.ls_ls_relevant_review_chunks_aspect_2)
print(product_1.ls_ls_prob_positive_sentiment_aspect_2)
print(product_1.ls_ls_relevant_review_chunks_aspect_3)
print(product_1.ls_ls_prob_positive_sentiment_aspect_3)
print(product_1.sentiment_score_aspect_1)
print(product_1.sentiment_score_aspect_2)
print(product_1.sentiment_score_aspect_3)


print('Product 2: \n')
print(product_2.chunked_review_texts)
print(product_2.ls_aspect_terms_1)
print(product_2.ls_aspect_terms_2)
print(product_2.ls_aspect_terms_3)
print(product_2.ls_ls_relevant_review_chunks_aspect_1)
print(product_2.ls_ls_prob_positive_sentiment_aspect_1)
print(product_2.ls_ls_relevant_review_chunks_aspect_2)
print(product_2.ls_ls_prob_positive_sentiment_aspect_2)
print(product_2.ls_ls_relevant_review_chunks_aspect_3)
print(product_2.ls_ls_prob_positive_sentiment_aspect_3)
print(product_2.sentiment_score_aspect_1)
print(product_2.sentiment_score_aspect_2)
print(product_2.sentiment_score_aspect_3)
print('\n')

print('Product 3: \n')
print(product_3.chunked_review_texts)
print(product_3.ls_aspect_terms_1)
print(product_3.ls_aspect_terms_2)
print(product_3.ls_aspect_terms_3)
print(product_3.ls_ls_relevant_review_chunks_aspect_1)
print(product_3.ls_ls_prob_positive_sentiment_aspect_1)
print(product_3.ls_ls_relevant_review_chunks_aspect_2)
print(product_3.ls_ls_prob_positive_sentiment_aspect_2)
print(product_3.ls_ls_relevant_review_chunks_aspect_3)
print(product_3.ls_ls_prob_positive_sentiment_aspect_3)
print(product_3.sentiment_score_aspect_1)
print(product_3.sentiment_score_aspect_2)
print(product_3.sentiment_score_aspect_3)

#compare results using dataframe
comparison_matrix = pd.DataFrame(data = [[product_1.sentiment_score_aspect_1, product_2.sentiment_score_aspect_1, product_3.sentiment_score_aspect_1],\
                                         [product_1.sentiment_score_aspect_2, product_2.sentiment_score_aspect_2, product_3.sentiment_score_aspect_2],\
                                         [product_1.sentiment_score_aspect_3, product_2.sentiment_score_aspect_3, product_3.sentiment_score_aspect_3]],\
                                 index = [list_aspect_1[0], list_aspect_2[0], list_aspect_3[0]],\
                                 columns = [product_1_name, product_2_name, product_3_name])

print(comparison_matrix)
