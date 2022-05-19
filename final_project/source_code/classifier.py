import math

class nb_classifier:

	def __init__(self,prior_1,prior_2,class1,class2,vocabulary):
		self.prior_1 = prior_1
		self.prior_2 = prior_2
		self.class1 = class1
		self.class2 = class2
		self.vocabulary = vocabulary
	def classify(self,features,counts_1,counts_2,sum_1,sum_2):
		'''Function that classifies a list of reviews (features), given the posterior and prior probabilities.'''
		results = []
		vocab_size = len(self.vocabulary)
		for review in features:
			posterior_1 = math.log(self.prior_1)
			posterior_2 = math.log(self.prior_2)
			for w in review:
				#If the word was seen in training, add the log of the probability, if not, continue.
				if w in self.vocabulary:
					try:				
						posterior_1 +=math.log((counts_1[w] + 1)/(sum_1 + vocab_size))
						posterior_2 +=math.log((counts_2[w] + 1)/(sum_2 + vocab_size))
					except:
						posterior_1 +=math.log(1/(sum_1 + vocab_size))
						posterior_2 +=math.log(1/(sum_2 + vocab_size))
			#If the probability of the class1 is greater than that of the second class, append name class1 to results, else, the opposite.		
			if posterior_1 > posterior_2:
				results.append(self.class1)
			else:
				results.append(self.class2)
		#Return a list with the tag for each review.
		return results