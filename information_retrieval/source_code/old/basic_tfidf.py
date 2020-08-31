import xml.etree.cElementTree as ET
import re
import math
import pre_processer
import evaluation_results

def calculate_freq(corpus):
	'''Function that, given a list of words, returns a dictionary of frequencies of each word.'''
	#Initialize dictionary
	frequencies = {}
	for word in corpus:
		if word in frequencies:
			#If word in dictionary add 1 to the frequency.
			frequencies[word] += 1
		else:
			#Add word to dictionary if not in dictionary.
			frequencies[word] = 1
	return frequencies

def main():
	#Get document
	with open('./data/trec_documents.xml') as f:
	    xml = f.read()
	#Parse document and get headlines and text.
	root = ET.fromstring(xml)
	#Dictionary where docs numbers and raw text will be stored.
	dic_raw_doc = {}
	for child in root:
		#Initialize variable where text will be stored.
		raw_text = ''
		for grandchild in child:
			if grandchild.tag == 'DOCNO':
				#Store doc numbers.
				key = grandchild.text
			#Store headlines.
			elif grandchild.tag == 'HEADLINE':
				#Try except for controlling LA documents which have a deeper level.
				try:
					grandchild[0]
					for greatgrandchild in grandchild:
						raw_text = raw_text + greatgrandchild.text
						
				except:
					raw_text = raw_text + grandchild.text
			#Store text.
			elif grandchild.tag == 'TEXT':
				#Try except for controlling LA documents which have a deeper level.
				try:
					grandchild[0]
					for greatgrandchild in grandchild:
						raw_text = raw_text + greatgrandchild.text
					#Text is completed, save in dictionary.
					dic_raw_doc[key] = raw_text
				except:
					raw_text = raw_text + grandchild.text
					#Text is completed, save in dictionary.
					dic_raw_doc[key] = raw_text
			
	#Dictionary where the tokenized documents will be stored.
	dic_doc = {}
	#Dictionary where the counts for for each term in all documents will be stored.
	dic_count_doc = {}
	#Total number of documents.
	N = len(dic_raw_doc.keys())
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
	#Calculate idf and saved it in a dictionary term:idf
	idf_dic = {}
	for k,v in dic_count_doc.items():
		idf_dic[k] = math.log((N/v),2)

	for k in idf_dic.keys():
		if re.search('[A-Z]',k):
			print(k)
	#Calculate tf and saved it in a dictionary doc:(term,tf)
	tf_term_doc = {}
	for k,v in dic_doc.items():
		counts_terms = calculate_freq(v)
		terms = {}
		maximum = max(counts_terms.values())
		for t,c in counts_terms.items():
			terms[t] = c/maximum
		tf_term_doc[k] = terms
	
	#Testing
	#List where all tokenized queries will be stored.
	queries = []
	with open('./data/test_questions.txt') as f:
		for l in f:
			if re.search('<desc>',l):
				query = pre_processer.tokenizer(re.split(' ',next(f)))
				queries.append(query)
	query_weights = []
	for query in queries:
		query_vector = []
		freq_query = calculate_freq(query)
		#terms_query = {}
		maximum = max(freq_query.values())
		for term,freq in freq_query.items():
			try:
				query_vector.append((c/maximum)*idf_dic[term])
			except:
				query_vector.append(0)
		query_weights.append(query_vector)
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
	cos_similarity = []
	for query,q in zip(query_weights,doc_query_weights):
		norm_q = math.sqrt(sum([pow(i,2) for i in query]))
		cos_similarity_query = {}
		for doc,vector in q.items():
			try:
				#Cosine similarity betweeen query and vector
				norm_d = math.sqrt(sum([pow(i,2) for i in vector]))
				dot_product = sum([i*j for i,j in zip(query,vector)])
				cos_similarity_query[doc] = dot_product/(norm_q*norm_d)
			except:
				continue
		cos_similarity.append(cos_similarity_query)

	##Select the the 50 most similar outputs for each query.
	output_per_query = {}
	for n,q in enumerate(cos_similarity):
		cos_sorted = sorted(q.items(),key=lambda item: item[1],reverse = True)
		output_per_query[n] = cos_sorted[0:50]
	#print(output_per_query)
	##Evaluation
	##Dictionary where all queries with the respectiv answers will be stored q:a
	dic_answers = {}
	with open('./data/patterns.txt') as f:
		for line in f:
			line_strip = line.strip('\n')
			#Original file was modified, query id and answer are now separated by tabs for clearer processing.
			a =line_strip.split('\t')
			if a[0] in dic_answers:
				#For the cases in which there is more than one answer.
				dic_answers[a[0]] += '|' + '(' + a[1] + ')'
			else:
				dic_answers[a[0]] = '(' + a[1] + ')'

	
	scores = evaluation_results.precision_f_score(dic_answers,output_per_query,dic_raw_doc)
	evaluation_results.write_results(scores[0],scores[1],scores[2],scores[3],scores[4],'./results/results_basic_tf-idf.txt')
	#Return top 1000 documents for each query.
	#output_per_query1 = {}
	#for q,docs in cos_similarity.items():
	#	cos_sorted1 = sorted(docs,key=lambda item: item[1],reverse = True)		output_per_query1[q] = cos_sorted1[0:1000]

if __name__=='__main__':
	main()