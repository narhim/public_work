This folder contains all the scrpits necesssary to run the whole program and they were design to be run on the parent directory, so access to the data is not problematic.

They are all written in Python 3.6 and the names of the scripts try to be self-explanatory:

	-main.py: main script, by running it, the whole program is executed, in other words, the information retrieval engine is run. It should be run on the parent directory.
	
	-pre_processer.py: module that contains all the preprocessing functions (retrieving from the xml file, word tokenizer and sentence tokenizer) as well as one unclassified functions used at the different stages of the information retrieval system.
	
	-basic_tf_idf.py: module that contains the tf-idf implementation.
	
	-cos_similarity.py: module that contains the function for calculating the cosine similarity between the matrix of queries and the matrix of documents.
	
	-bm_implementation.py: module that contains bm25 implementation for reranking cosine similarities and rankig sentences.
	
	-evaluation_results.py: module that contains all the functions for calculating the evaluation scores and writing them in output files, which re placed on the sister directory "results" whose pre-existance is assumed.

Other modules and libraries used are the following:
	-re: for regex
	
	-nltk, from here nltk corpus: the stopwords from nltk corpus are used for tkenizations.
	
	-math: for math operations
	
	-xml.etree.cElementTree: for parsing the xml file.


