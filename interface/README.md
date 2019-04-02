## User Run Interface

This is where the user needs to 'run' the whole system from.


## User Setting Interface

This is where the user needs to specify his or her inputs:
(The first 3 inputs below concern the attributes of the products to be compared)
- Review Links (in Bahasa Indonesia)
- Product Names
- Aspect Terms

- location path of certain files
- choice of deep learning sentiment model (I use AOA as it achieves the highest accuracy)

## Product Class

This class contains functions that combine the functionalities of the whole system, mainly:
- Web Scraping (using Beautiful Soup library)
- Translation (using Google Translate API)
- Chunking
- Aspect Based Sentiment Analysis (using deep learning ABSA models)
- Sentiment Scoring
