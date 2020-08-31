import xml.etree.cElementTree as ET
import re
import math
#from BeautifulSoup import BeautifulStoneSoup
def tokenizer(list_lines):
	#Initialize list where all words will be stored.			         
	corpus = []
	for line in list_lines:
		#Separate characters by delimiters defined in regex.
		s = re.split(' |[.] |[.]{2,}|[:]|[;]|[\']|["]|[„]|[‟]|[”]|[<]+|[>]+|[(]|[)]|[\[]|[\]]|[¿]|[?]|[¡]|[!]',line)
		#Initialize list in which results from strip will be appended.
		result = []
		for element in s:
			#Remove characters specified in regex from string.
			s_r = element.strip('\n|[.]+|[:]|[,]|[;]|[«]|[»]|["]|[„]|[‟]|[”]|[<]+|[>]+|[\*]|[(]|[)]|[\[]|[\]]|[¿]|[?]|[¡]|[!]')
			result.append(s_r)
		 #Loop over results from strip for second clean up.
		for w in result:
			#Avoid empty strings and "===".
			if (w=='') or (re.match('=+',w) != None):
				continue
			#Conditions for string with hyphens. And example for each condition is provided.
			elif re.search('-',w) != None:
				#5-5
				if re.search('\d+-\d+',w):
					numbers = re.split('-',w)
					corpus.append(numbers[0])
					corpus.append(numbers[1])
				#cat-dog
				elif re.search('[a-z]+-[a-z]+',w,flags=re.IGNORECASE):
					corpus.append(w.lower())

				#45-ben
				elif re.search('\d+-\D+',w):
					numbers = re.split('-',w)
					corpus.append(numbers[0])
					corpus.append(numbers[1])
				#-32,9
				elif re.match('-\d+',w):
					corpus.append(w)
				#alt- (from (alt-)griechisch)
				elif re.search('[a-z]-',w,flags=re.IGNORECASE):
					clean = w.strip('-')
					corpus.append(clean.lower())
				#-word
				elif re.match('-\w+',w):
					clean = w.strip('-')
					corpus.append(clean.lower())
				#45-
				elif re.match('\d+-',w):
					clean = w.strip('-')
					corpus.append(clean)
				#-%45 and -«word
				elif re.match('[-%\d+]|[-«\w+]',w):
					clean = w.strip('[-%]|[-«]')
					corpus.append(clean.lower())
				#Avoid "-".
				elif re.match('^-$',w):
					continue
			elif w == '/':
				continue
			elif re.search('[a-z]\/',w,flags=re.IGNORECASE):
				splitted = w.split('/')
				corpus.append(splitted[0].lower())
				corpus.append(splitted[1].lower())
			elif re.search('\d[.]\d',w):
				corpus.append(w)
			#avoid the second type of hyphen found in raw text.
			elif re.match('–',w):
					continue
			#If none of the conditions above apply, simply lower and apply.
			else:
				corpus.append(w.lower())
	return corpus

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
			
	#print(dic_raw_doc)
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
		value_tokenized = tokenizer(value_splitted)
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
				query = tokenizer(re.split(' ',next(f)))
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

	#Calculate precision (for each document and overall) and number of querie that have a relevant output.
		#Calculate precision (for each document and overall) and number of queries that have a relevant output.
	q_relevant = []
	average_precision = 0
	precisions = {}
	average_recall = 0
	recalls = {}
	f_scores = {}
	average_f = 0
	for (q,a),(qu,s) in zip(dic_answers.items(),output_per_query.items()):
		
		relevant = 0
		total_recovered = len(s)
		relevant_answers = re.findall('\)\|\(', a)
		for d in s:
			if re.search(a,dic_raw_doc[d[0]],flags=re.IGNORECASE):
				relevant += 1
				q_relevant.append(q)
		precision = relevant / total_recovered
		precisions[q] = precision
		average_precision += precision
		overall_precision = average_precision/len(output_per_query.keys())
		recall = relevant/ (len(relevant_answers)+1)

		recalls[q] = recall
		average_recall += recall
		den = precision+recall
		if den == 0:
			f_score = 0
		else:
			f_score = 2*(precision*recall)/(precision+recall)
		f_scores[q] = f_score
		average_f += f_score
		overall_precision = average_precision/len(output_per_query.keys())
		overall_recall = average_recall/len(output_per_query.keys())
		overall_f = average_f/len(output_per_query.keys())

#
	#Write all the results in a .txt file.
	with open('./results/results_basic_tf-idf.txt',"w",encoding = "utf-8") as file:
		for k,v in precisions.items():
			file.write('The precision for query ' + str(k) + ' is ' + str(v) + '\n')
		file.write('The average precision is ' + str(overall_precision) + '\n')
		file.write('The number of queries that have at least one relevant output is ' + str(len(set(q_relevant))))
		for i, g in f_scores.items():
			file.write('The F1 score for query ' + str(i) + ' is ' + str(g) + '\n')
		file.write('The average F1 score is ' + str(overall_f) + '\n')
		file.write('The number of queries that have at least one relevant output is ' + str(len(set(q_relevant))))

	#Return top 1000 documents for each query.
	#output_per_query1 = {}
	#for q,docs in cos_similarity.items():
	#	cos_sorted1 = sorted(docs,key=lambda item: item[1],reverse = True)		output_per_query1[q] = cos_sorted1[0:1000]
	#For 1000 documents
	output_per_query1 = {}
	for q,docs in enumerate(cos_similarity):
		cos_sorted1 = sorted(docs,key=lambda item: item[1],reverse = True)
		cos_sorted_1000 = cos_sorted1[0:1000]
		doc_list = []
		for par in cos_sorted_1000:
			doc_list.append(par)
		output_per_query1[q] = doc_list
	##Calculate the BM25 weights and store them in a dictionary doc:(term,weight)
	#Create a dic for bm25
	bm_idf_dic = {}
	for k, v in dic_count_doc.items():
		bm_idf_dic[k] = math.log((1+((N - v + .5) / (v+.5))), 2)

	doc_len = {}
	for docno,terms in dic_doc.items():
		doc_len[docno] =len(terms)
	average_length = sum(doc_len.values())/(len(doc_len.keys()))
	bm_tf_dic = {}
	for k, v in tf_term_doc.items():
		bm_tf_doc = {}
		for t,f in v.items():
			bm_tf_doc[t] = f/(f + 4*(1-0.6+(0.6*doc_len[k]/average_length)))
		bm_tf_dic[k] = bm_tf_doc



	bm_query_weights = []
	for query in queries:
		query_vector = []
		freq_query = calculate_freq(query)
		for term,freq in freq_query.items():
			try:
				query_vector.append(f/(f + 4*(1-0.6+(0.6*doc_len[k]/average_length)))*idf_dic[term])
			except:
				query_vector.append(0)
		bm_query_weights.append(query_vector)

	bm_doc_query_weights = []
	for n,query in enumerate(queries):
		doc_dic = {}
		for doc,terms in bm_tf_dic.items():
			#if doc in output_per_query1[n]:
			doc_vector = []
			for token in query:
				if token in terms:
					doc_vector.append(terms[token]*bm_idf_dic[token])
				else:
					doc_vector.append(0)
			doc_dic[doc] = doc_vector
			#else:
			#	continue
		bm_doc_query_weights.append(doc_dic)
	bm_cos_similarity = []
	for query,q in zip(bm_query_weights,bm_doc_query_weights):
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
		bm_cos_similarity.append(cos_similarity_query)

	##Select the the 50 most similar outputs for each query.
	bm_output_per_query = {}
	for n,q in enumerate(bm_cos_similarity):
		cos_sorted = sorted(q.items(),key=lambda item: item[1],reverse = True)
		bm_output_per_query[n] = cos_sorted[0:50]

	##Evaluation
	##Dictionary where all queries with the respectiv answers will be stored q:a
	bm_dic_answers = dic_answers
	##Calculate precision (for each document and overall) and number of queries that have a relevant output.
	bm_q_relevant = []
	bm_average_precision = 0
	bm_precisions = {}
	bm_average_recall = 0
	bm_recalls = {}
	bm_f_scores = {}
	bm_average_f = 0
#
	for (q,a),(qu,s) in zip(bm_dic_answers.items(),bm_output_per_query.items()):
		bm_relevant = 0
		bm_total_recovered = len(s)
		bm_relevant_answers = re.findall('\)\|\(', a)
		for d in s:
			if re.search(a,dic_raw_doc[d[0]], flags=re.IGNORECASE):
				bm_relevant += 1
				bm_q_relevant.append(q)
		bm_precision = bm_relevant / bm_total_recovered
		bm_recall = bm_relevant / (len(bm_relevant_answers)+1)
		bm_precisions[q] = bm_precision
		bm_recalls[q] = bm_recall
		bm_average_precision += bm_precision
		bm_average_recall += bm_recall
		den = bm_precision+bm_recall
		if den == 0:
			bm_f_score = 0
		else:
			bm_f_score = 2*(bm_precision*bm_recall)/(bm_precision+bm_recall)
		bm_f_scores[q] = bm_f_score
		bm_average_f += bm_f_score
	bm_overall_precision = bm_average_precision/len(bm_output_per_query.keys())
	bm_overall_recall = bm_average_recall/len(bm_output_per_query.keys())
	bm_overall_f = bm_average_f/len(bm_output_per_query.keys())
#
#Wri#te all the results in a .txt file.
	with open('./results/results_bm.txt',"w",encoding = "utf-8") as file:
		for k,v in bm_precisions.items():
			file.write('The precision for query ' + str(k) + ' is ' + str(v) + '\n')
		file.write('The average precision is ' + str(bm_overall_precision) + '\n')
		file.write('The number of queries that have at least one relevant output is ' + str(len(set(bm_q_relevant))))
		for i, g in bm_f_scores.items():
			file.write('The F1 score for query ' + str(i) + ' is ' + str(g) + '\n')
		file.write('The average F1 score is ' + str(bm_overall_f) + '\n')
		file.write('The number of queries that have at least one relevant output is ' + str(len(set(bm_q_relevant))))

	

if __name__=='__main__':
	main()
#