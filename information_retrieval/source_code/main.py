import pre_processer
import basic_tfidf
import cos_similarity
import evaluation_results
import bm_implementation

def main():
	dic_raw_doc = pre_processer.read_xml('./data/trec_documents.xml')
	#Total number of documents.
	N = len(dic_raw_doc.keys())
	#Dictionary where the tokenized documents will be stored.
	dic_doc = {}
	#Dictionary where the counts for for each term in all documents will be stored.
	dic_count_doc = {}
	#Tokenize and count number of documents in which each token is.
	for k,v in dic_raw_doc.items():
		#Tokenize document in 2 steps.
		value_splitted = v.split('\n')
		value_tokenized = pre_processer.tokenizer(value_splitted)
		#Store tokenized document in dictionary.
		dic_doc[k] = value_tokenized
		#Loop over the unique set of tokens.
		for word in set(value_tokenized):
			#Add one to the count if already on dictionary.
			if word in dic_count_doc:
				dic_count_doc[word] += 1
			#Add to dictionary
			else:
				dic_count_doc[word] = 1
	idf_dic = basic_tfidf.calculate_idf_dic(dic_count_doc,N)
	tf_dic = basic_tfidf.calculate_tf_dic(dic_doc)

	queries = basic_tfidf.obtain_queries('./data/test_questions.txt')
	
	query_weights = basic_tfidf.obtain_query_weights(queries,idf_dic)
	doc_query_weights = basic_tfidf.obtain_doc_query_weights(queries,tf_dic,idf_dic)
	tf_idf_cos_similarity = cos_similarity.calculate_cos_similarity(query_weights,doc_query_weights)
	output_per_query = evaluation_results.select_output_query(tf_idf_cos_similarity)
	answers = evaluation_results.get_answers('./data/patterns.txt')
	scores = evaluation_results.precision_f_score(answers,output_per_query,dic_raw_doc)
	evaluation_results.write_results(scores[0],scores[1],scores[2],scores[3],scores[4],'./results/results_basic_tf-idf.txt')

	output_per_query_1000 = evaluation_results.select_doc_query(tf_idf_cos_similarity)
	bm_idf_dic = bm_implementation.calculate_idf_dic(dic_count_doc,N)
	doc_len = bm_implementation.create_dic_lengths(dic_doc)
	average_length = sum(doc_len.values())/(len(doc_len.keys()))
	k_list = [1,2,3,4,5]
	k_results = []
	for k in k_list:
		bm_tf_dic = bm_implementation.calculate_tf_dic(dic_doc,doc_len,average_length,k,0.1)
		

		dic_len_queries = {n:len(q) for n,q in enumerate(queries)}
		query_average_length = sum(dic_len_queries.values())/(len(dic_len_queries.keys()))
		bm_query_weights = bm_implementation.calculate_query_weights(queries,dic_len_queries,query_average_length,bm_idf_dic,1,0.6)
		bm_doc_query_weights = bm_implementation.obtain_doc_query_weights(queries,bm_tf_dic,bm_idf_dic)
		bm_cos_similarity = cos_similarity.calculate_cos_similarity(bm_query_weights,bm_doc_query_weights)
		bm_output_per_query = evaluation_results.select_output_query(bm_cos_similarity)
		
		#This two are just for comparing normal use of bm 25 to tf-idf, not for final results.
		#bm_scores = evaluation_results.precision_f_score(answers,bm_output_per_query,dic_raw_doc)
		#evaluation_results.write_results(bm_scores[0],bm_scores[1],bm_scores[2],bm_scores[3],bm_scores[4],'./results/results_bm.txt')
					
		rerank_bm_doc_query_weights = bm_implementation.reweight_matrix(bm_cos_similarity,output_per_query_1000)
		rerank_bm_output_per_query = evaluation_results.select_output_query(rerank_bm_doc_query_weights)
		rerank_bm_scores = evaluation_results.precision_f_score(answers,rerank_bm_output_per_query,dic_raw_doc)
		path = './results/results_rerank_bm' + '_k_value_' + str(k) + '.txt'
		#print(rerank_bm_scores[0],rerank_bm_scores[1],rerank_bm_scores[2],rerank_bm_scores[3],rerank_bm_scores[4])	
		evaluation_results.write_results(rerank_bm_scores[0],rerank_bm_scores[1],rerank_bm_scores[2],rerank_bm_scores[3],rerank_bm_scores[4],path)
 												

	# Part 3: Sentence Ranker
	
	# Get the top 50 documents and split them into sentences
	
	top_50_docs, list_sent, list_words = bm_implementation.get_top_50_docs(bm_output_per_query, dic_raw_doc)
	#Total number of documents
	N_sent = len(list_sent)
	
	# Calculate idf and saved it in a dictionary doc:(term,tf)
	sent_idf_dic = bm_implementation.calculate_sent_idf_dic(list_sent, list_words, N_sent)
	
	# Calculate tf and saved it in a dictionary doc:(term,tf)
	tf_term_sent = {}
	for sent in list_sent:
			tf_term_sent[' '.join(sent)] =  pre_processer.calculate_freq(sent)


	sent_len = dl_dic = {' '.join(list_sent[x]):len(list_sent[x]) for x in range(len(list_sent))}
	sent_average_length = sum(sent_len.values())/(len(sent_len.keys()))
	tf_term_sent = bm_implementation.calculate_tf_dic_sent(list_sent,sent_len,sent_average_length,1,0.6)


	sent_query_weights = bm_implementation.calculate_query_weights(queries,dic_len_queries,query_average_length,sent_idf_dic,1,0.6)
	bm_sent_query_weights = bm_implementation.obtain_doc_query_weights(queries,tf_term_sent,sent_idf_dic)
	sent_cos_similarity = cos_similarity.calculate_cos_similarity(sent_query_weights,bm_sent_query_weights)
	sent_output_per_query = evaluation_results.select_output_query(sent_cos_similarity)
	print('The MRR is', evaluation_results.calculate_mrr(answers, sent_output_per_query))
if __name__=='__main__':
	main()
