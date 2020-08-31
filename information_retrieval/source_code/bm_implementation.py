import math
import pre_processer
def calculate_idf_dic(dic_count_doc,N):
	bm_idf_dic = {}
	for k, v in dic_count_doc.items():
		bm_idf_dic[k] = math.log((1+((N - v + .5) / (v+.5))), 2)
	return bm_idf_dic

def create_dic_lengths(dic_doc):
	doc_len = {}
	for docno,terms in dic_doc.items():
		doc_len[docno] =len(terms)
	return doc_len

def calculate_tf_dic(dic_doc,dic_len,average_length,k,b):
	bm_tf_dic = {}
	for key, v in dic_doc.items():
		counts_terms = pre_processer.calculate_freq(v)
		bm_tf_doc = {}
		for t,f in counts_terms.items():
			bm_tf_doc[t] = f/(f + k*(1-b+(b*dic_len[key]/average_length)))
		bm_tf_dic[key] = bm_tf_doc
	return bm_tf_dic

def calculate_query_weights(queries,doc_len,average_length_query,bm_idf_dic,k,b):
	bm_query_weights = []
	for n,query in enumerate(queries):
		query_vector = []
		freq_query = pre_processer.calculate_freq(query)
		for term,f in freq_query.items():
			try:
				query_vector.append(f/(f + k*(1-b+(b*doc_len[n]/average_length_query)))*bm_idf_dic[term])
			except:
				query_vector.append(0)
		bm_query_weights.append(query_vector)
	return bm_query_weights

def obtain_doc_query_weights(queries,bm_tf_dic,bm_idf_dic):
	bm_doc_query_weights = []
	for n,query in enumerate(queries):
		doc_dic = {}
		for doc,terms in bm_tf_dic.items():
			doc_vector = []
			for token in query:
				if token in terms:
					doc_vector.append(terms[token]*bm_idf_dic[token])
				else:
					doc_vector.append(0)
			doc_dic[doc] = doc_vector
		bm_doc_query_weights.append(doc_dic)
	return bm_doc_query_weights

def reweight_matrix(cosine_similarities,outputs):
	reweighted_cos_similarities = []
	for query,list_tuples in zip(cosine_similarities,outputs.values()):
		new_query_cos = {}
		for pair in list_tuples:
			new_query_cos[pair[0]] = query[pair[0]]
		reweighted_cos_similarities.append(new_query_cos)
	return reweighted_cos_similarities

def get_top_50_docs(bm_output_per_query, dic_raw_doc):

	top_50_docs = {}
	list_sent = []
	list_words = []
	for q, docs in bm_output_per_query.items():
		qu_sent = []
		for doc in docs:
			doc_token = pre_processer.sent_tokenizer(dic_raw_doc[doc[0]])
			qu_sent.extend(doc_token)
			for sent in doc_token:
				if sent not in list_sent:
					list_sent.append(sent)
				for word in sent:
					if word not in list_words:
						list_words.append(word)
		top_50_docs[q] = qu_sent
	return top_50_docs, list_sent, list_words


def calculate_sent_idf_dic(list_sent, list_words, N_sent):

	word_count_sent = {}
	
	for w in list_words:
		count = 0
		for v in list_sent:
			if w in v:
				count +=1
		word_count_sent[w] = count
	sent_idf_dic = {w: math.log((1 + (N_sent - k + .5) / (k+.5)), 2) for w, k in word_count_sent.items()}
	return sent_idf_dic

def calculate_idf_dic(dic_count_doc,N):
	bm_idf_dic = {}
	for k, v in dic_count_doc.items():
		bm_idf_dic[k] = math.log((1+((N - v + .5) / (v+.5))), 2)
	return bm_idf_dic

def calculate_tf_dic_sent(list_sent,sent_len,sent_average_length,k,b):
	bm_tf_dic = {}
	for sent in list_sent:
		str_sent = ' '.join(sent)	
		counts_terms = pre_processer.calculate_freq(sent)
		bm_tf_doc = {}
		for t,f in counts_terms.items():
			bm_tf_doc[t] = f/(f + k*(1-b+(b*sent_len[str_sent]/sent_average_length)))
		bm_tf_dic[str_sent] = bm_tf_doc
	return bm_tf_dic
	
	


