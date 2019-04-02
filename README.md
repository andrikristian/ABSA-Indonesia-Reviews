# ABSA-Indonesia-Reviews
I did this as part of my Final Year Project in NUS


## ABSA

This folder concerns the Aspect Based Sentiment Analysis. The following briefly explains the files listed:
- models (list all the models available for training)
- state_dict (list all the weights and parameters of the model that achieve the best performance)
- train (code for training the model; hyperparameter settings can be changed here)
- infer_example (sample code for testing the model; not in use for my sentiment analysis system)

## Interface

This folder concerns settings of the system and the product details to be analysed. 
User also needs to run the whole system through running the file 'user_run_interface.py'

## Synonyms_Generator

The purpose of this is to generate synonyms of the aspect terms that the user input into the system. The reason is because some reviews are relevant but do not contain the exact aspect terms input by the user. Hence, a need for the synonyms generator.
