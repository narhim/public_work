import re

def select_output_query(list_outputs):
	##Select the the 50 most similar outputs for each query.
	output_per_query = {}
	for number,q in enumerate(list_outputs):
		cos_sorted = sorted(q.items(),key=lambda item: item[1],reverse = True)
		output_per_query[number] = cos_sorted[0:50]
	return output_per_query

def select_doc_query(list_outputs):
	##Select the the 50 most similar outputs for each query.
	output_per_query = {}
	for number,q in enumerate(list_outputs):
		cos_sorted = sorted(q.items(),key=lambda item: item[1],reverse = True)
		output_per_query[number] = cos_sorted[0:1000]
	return output_per_query

def get_answers(path):
	##Dictionary where all queries with the respectiv answers will be stored q:a
	dic_answers = {}
	with open(path) as f:
		for line in f:
			line_strip = line.strip('\n')
			#Original file was modified, query id and answer are now separated by tabs for clearer processing.
			a =line_strip.split('\t')
			if a[0] in dic_answers:
				#For the cases in which there is more than one answer.
				dic_answers[a[0]] += '|' + '(' + a[1] + ')'
			else:
				dic_answers[a[0]] = '(' + a[1] + ')'
	return dic_answers

def precision_f_score(dic_answers,output_per_query,dic_raw_doc):#Calculate precision (for each document and overall) and number of querie that have a relevant output.
		#Calculate precision (for each document and overall) and number of queries that have a relevant output.
	q_relevant = []
	average_precision = 0
	precisions = {}
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
	return precisions,overall_precision,q_relevant,average_precision


def calculate_mrr(dic_answers, sent_output_per_query):
	sum_ranks = 0
	for (q,a),(qu,s) in zip(dic_answers.items(),sent_output_per_query.items()):		
		for n,d in enumerate(s):
			if re.search(a,d[0],flags=re.IGNORECASE):
				relevant_rank = n +1
				sum_ranks += 1/relevant_rank
				break
	return sum_ranks/100


def write_results(dic_precisions,overall_precision,q_relevant,average_precision,name):
	#Write all the results in a .txt file.
	with open(name,"w",encoding = "utf-8") as file:
		for k,v in dic_precisions.items():
			file.write('The precision for query ' + str(k) + ' is ' + str(v) + '\n')
		file.write('The average precision is ' + str(overall_precision) + '\n')
		file.write('The number of queries that have at least one relevant output is ' + str(len(set(q_relevant))))
