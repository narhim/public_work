This directory contains an information retrieval system that both Iuliia Zaitova (https://github.com/IuliiaZaitova) and I developed for the final project of the lecture "Statistical Natural Language Processing" in our masters "Language Science and Technology".

The system consists on three distinguished parts:

	1.- Basic tf-idf implementation: 
		- Document retrieval implementation that retrieves the top 50 documents for the 100 queries. The retrieval is based in tf-idf weights and cosine similarity, queries are treated as documents.
		- Outputs are then evaluated based on the regex patterns contained in the gold file, both precision and F1-Score are calculated for each query and for the whole of the queries and outputted into the directory "results".
		- Queries (test_questions.txt), documents (trec_documents.xml) and gold file (patterns.text) are contained in the directory "data". 

	2.- Advance Document Retriever (BM25) Re-Ranking: 
		- Takes 1000 documents per query from the implementation on the first step.
		- Redefines the tf-idf weights with the BM25 implementation (http://www.kmwllc.com/index.php/2020/03/20/understanding-tf-idf-and-bm25/) for k in [1,2,3,4,5] and re-ranks the 1000 documents above.
		- Outputs 50 documents per query and evaluates the results as in the first section.

	3.- Sentence Ranking:
		-Ranks the sentences from the documents outputted in section 2 with BM25 weights.
		-Returns the top 50 sentences for each query.
		-Evaluation is done by calculating the mean reciprocal rank (MRR) and printted on the terminal.


Technical charecteristics and explanations on how to run the program are on the README in the source_code directory.
