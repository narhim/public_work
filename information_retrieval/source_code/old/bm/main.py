import xml.etree.cElementTree as ET
import re
import math
from rank_bm25 import BM25Okapi
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


def bm_25(doc_dic, tf_dic, bm_idf_dic, k):
    bm_25_dic = {}
    b = 0.6
    # dic with lengths of the docs
    dl_dic = {x:len(doc_dic[x]) for x in doc_dic}
    # average length of the docs
    adl = sum(dl_dic.values())/len(dl_dic.keys())

    for d, terms in tf_dic.items():
        doc_bm = {}
        dl = dl_dic[d]
        e = 1 - b + b * dl / adl
        for t, tf in terms.items():
            idf = bm_idf_dic[t]
            doc_bm[t] = (tf/(tf+k*e))*idf
        bm_25_dic[d] = doc_bm
    return bm_25_dic

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

	corpus = []
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

		corpus.append(value_tokenized)
		#Loop over the unique set of tokens.
		for word in set(value_tokenized):
			#Add one to the count if already on dictionary.
			if word in dic_count_doc:
				dic_count_doc[word] += 1
			#Add to dictionary
			else:
				dic_count_doc[word] = 1
	#Testing
	#List where all tokenized queries will be stored.
	queries = []
	with open('./data/test_questions.txt') as f:
		for l in f:
			if re.search('<desc>',l):
				query = tokenizer(re.split(' ',next(f)))
				queries.append(query)
	#print(queries)



	#Calculate the BM25 weights and store them in a dictionary doc:(term,weight)


		# Calculate the tf-idf weights for each term in each document and store them in a dictionary doc:(term,weight)



	bm_output_per_query = {}
	#queries_dic = {q: queries[q] for q in range(len(queries))}
	bm25 = BM25Okapi(dic_doc.values())
	for q in range(len(queries)):
		top_1000 = bm25.get_top_n(queries[q], corpus, n=1000)
		for doc in range(len(top_1000)):
			for n, doct in dic_doc.items():
				if doct == top_1000[doc]:
					name = n
			top_1000[doc] = name
		print(top_1000)
		
		bm_output_per_query[q] = top_1000
	#print(output_per_query)
	#Evaluation
	#Dictionary where all queries with the respectiv answers will be stored q:a
	bm_dic_answers = {}
	with open('./data/patterns.txt') as f:
		for line in f:
			line_strip = line.strip('\n')
			#Original file was modified, query id and answer are now separated by tabs for clearer processing.
			a =line_strip.split('\t')
			if a[0] in bm_dic_answers:
				#For the cases in which there is more than one answer.
				bm_dic_answers[a[0]] += '|' + '(' + a[1] + ')'
			else:
				bm_dic_answers[a[0]] = '(' + a[1] + ')'


	#Calculate precision (for each document and overall) and number of queries that have a relevant output.
	bm_q_relevant = []
	bm_average_precision = 0
	bm_precisions = {}
	bm_average_recall = 0
	bm_recalls = {}
	bm_f_scores = {}
	bm_average_f = 0

	for (q,a),(qu,s) in zip(bm_dic_answers.items(),bm_output_per_query.items()):
		bm_relevant = 0
		bm_total_recovered = len(s)
		bm_relevant_answers = re.findall('\)\|\(', a)

		for d in s:

			if re.search(a,dic_raw_doc[d], re.IGNORECASE):
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

	#Write all the results in a .txt file.
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
