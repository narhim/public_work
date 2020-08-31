import math

def calculate_cos_similarity(query_weights,doc_query_weights):
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
	return cos_similarity
