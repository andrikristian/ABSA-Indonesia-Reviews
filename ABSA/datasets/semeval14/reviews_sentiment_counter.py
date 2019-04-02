#open laptop training data

f = open("Laptops_Test", "r")

review = '.'
num_pos_rev = 0
num_neutral_rev = 0
num_neg_rev = 0

review = ' '
aspect_term = ''
sentiment_score = ''

while review != '':
    review = f.readline()
    aspect_term = f.readline()
    sentiment_score = int(f.readline())

    print(review)
    print(aspect_term)
    print(sentiment_score)

    if sentiment_score == 1:
        num_pos_rev += 1

    if sentiment_score == 0:
        num_neutral_rev += 1

    if sentiment_score == -1:
        num_neg_rev += 1

    print('num_pos_rev: ', num_pos_rev)
    print('num_neutral_rev: ', num_neutral_rev)
    print('num_neg_rev: ', num_neg_rev)