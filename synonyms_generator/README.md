# GloVe Experiments
## Taken from: https://github.com/brannondorsey/GloVe-experiments

This repository contains a few brief experiments with [Stanford NLP's GloVe](https://nlp.stanford.edu/projects/glove/), an unsupervised learning algorithm for obtaining vector representations for words. Similar to Word2Vec, GloVe creates a continuous N-dimensional representation of a word that is learned from its surrounding context words in a training corpus. Trained on a large corpus of text, these co-occurance statistics (an N-dimensional vector embedding) cause semantically similar words to appear near each-other in their resulting N-dimensional embedding space (e.g. "dog" and "cat" may appear nearby a region of other pet related words in the embedding space because the context words that surround both "dog" and "cat" in the training corpus are similar).

I've created three small python programs for exploring GloVe embeddings:

- `word_arithmetic.py`: Create word analogy searches using basic arithmetic operations (e.g. `king - man + women = queen`).
- `word_game.py`: A small terminal-based multiplayer text game for creating word analogies.
- `word_clustering.py`: Create [K-Means clusters](https://en.wikipedia.org/wiki/K-means_clustering) using GloVe embeddings. Saves results to JSON.

All three scripts use the GloVe.6B pre-trained word embeddings created from the combined Wikipedia 2014 and Gigaword 5 datasets. They were trained using 6 billion tokens and contains 400,000 unique lowercase words. Trained embeddings are provided in 50, 100, 200, and 300 dimensions (822 MB download).

## Getting Started

These small experiments can be run in MacOS or Linux environments (sorry ~~not sorry~~ Windoze users).

```bash
# clone this repo
git clone https://github.com/brannondorsey/GloVe-experiments.git
cd GloVe-experiments

# install python dependencies
pip3 install -r requirements.txt

# dowload the pre-trained embeddings. This might take a while...
./download_data.sh
```

## Word Arithmetic (Synonyms_Generator)

`word_arithmetic.py` allows you to write simple +/- arithmetic operations using words to find the closest approximated resulting word from the given word expression. Math operations are applied in the embedding space and a K-nearest-neighbor search is used to display the `K` words closest to the result of the algebraic transformation.

```bash
python3 word_arithmetic.py
> king - man + woman

queen                0.22
```

`word - word + word` is the traditional word analogy format, however `word_arithmetic.py` supports any number of `+` or `-` operations provided all words are in the database. The meaning of less traditional expressions, `word + word + word...` is more ambiguous but can lead to interesting results nonetheless. Specifying an order of operations is not supported at this time (e.g. `(word - word) + word`).

By default, `word_arithmetic.py` loads the 10,000 most frequently used words from the dataset and uses a 100-dimensional embedding vector. It also prints only the single nearest word to the resulting vector point from the expression (the "nearest neighbor"). You can specify your own values for each of these parameters if you would like:

```bash
python3 word_arithmetic.py --num_words 100000 --vector_dim 300 --num_output 10
> king - man + woman

queen                0.31
monarch              0.44
throne               0.44
princess             0.45
mother               0.49
daughter             0.49
kingdom              0.50
prince               0.50
elizabeth            0.51
wife                 0.52
```

Increasing `--num_words` and `--vector_dim` increases the number of usable words in the dictionary and accuracy of the resulting word expressions respectively. Increasing either will increase the processing time for each expression as well as the memory requirements needed to run the program.

```
usage: word_arithmetic.py [-h] [--vector_dim {50,100,200,300}]
                          [--num_words NUM_WORDS] [--num_output NUM_OUTPUT]
                          [--glove_path GLOVE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --vector_dim {50,100,200,300}, -d {50,100,200,300}
                        What vector GloVe vector depth to use (default: 100).
  --num_words NUM_WORDS, -n NUM_WORDS
                        The number of lines to read from the GloVe vector file
                        (default: 10000).
  --num_output NUM_OUTPUT, -o NUM_OUTPUT
                        The number of result words to display (default: 1)
  --glove_path GLOVE_PATH, -i GLOVE_PATH
                        GloVe vector file path
```



## License and Attribution

All code is released under an [MIT license](LICENSE). You are free to copy, edit, share, or sell it under those terms.

### GloVe citation

Jeffrey Pennington, Richard Socher, and Christopher D. Manning. 2014. [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf).

```
@inproceedings{pennington2014glove,
  author = {Jeffrey Pennington and Richard Socher and Christopher D. Manning},
  booktitle = {Empirical Methods in Natural Language Processing (EMNLP)},
  title = {GloVe: Global Vectors for Word Representation},
  year = {2014},
  pages = {1532--1543},
  url = {http://www.aclweb.org/anthology/D14-1162},
}
```
