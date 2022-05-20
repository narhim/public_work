This directory contains a very simple Naive Bayes sentiment analysis classifier designed for the IMDB movie reviews dataset. To run it, the script main.py, contained in the directory source_code, is run normally through the command line and uses all the other scripts contained in the repository. Results are printed in the command line.

The other scripts contained in the directory are:
-pre_processer.py: to read in all reviews and tokenize them. Not all functions there are used. It requires the following modules: re, os.
-count.py: simple class to obtain the required frequencies.
-classifier.py: performs the actual classification. It requires the following module: math.
-evaluation.py: computes accuracy, precision and recall.