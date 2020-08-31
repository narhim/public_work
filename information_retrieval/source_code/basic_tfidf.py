
import re
import math
import pre_processer

	
def calculate_idf_dic(dic_count_doc,N):	#Calculate idf and saved it in a dictionary term:idf
	idf_dic = {}
	for k,v in dic_count_doc.items():
		idf_dic[k] = math.log((N/v),2)
	return idf_dic

def calculate_tf_dic(dic_doc):
	#Calculate tf and saved it in a dictionary doc:(term,tf)
	tf_term_doc = {}
	for k,v in dic_doc.items():
		counts_terms = pre_processer.calculate_freq(v)
		terms = {}
		maximum = max(counts_terms.values())
		for t,c in counts_terms.items():
			terms[t] = c/maximum
		tf_term_doc[k] = terms
	return tf_term_doc
	
def obtain_queries(path):
	##List where all tokenized queries will be stored.
	queries = []
	with open(path) as f:
		for l in f:
			if re.search('<desc>',l):
				query = pre_processer.tokenizer(re.split(' ',next(f)))
				queries.append(query)
	return queries
def obtain_query_weights(queries,idf_dic):
	query_weights = []
	for query in queries:
		query_vector = []
		freq_query = pre_processer.calculate_freq(query)
		#terms_query = {}
		maximum = max(freq_query.values())
		for term,freq in freq_query.items():
			try:
				query_vector.append((freq/maximum)*idf_dic[term])
			except:
				query_vector.append(0)
		query_weights.append(query_vector)
	return query_weights

def obtain_doc_query_weights(queries,tf_term_doc,idf_dic):
	doc_query_weights = []
	for query in queries:
		doc_dic = {}
		for doc,terms in tf_term_doc.items():
			doc_vector = []
			for token in query:
				if token in terms:
					doc_vector.append(terms[token]*idf_dic[token])
				else:
					doc_vector.append(0)
			doc_dic[doc] = doc_vector
		doc_query_weights.append(doc_dic)

	return doc_query_weights