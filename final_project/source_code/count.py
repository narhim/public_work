class count:

	def list_abs_freq(self,list_words):
		'''Function that, given a list of words, returns a dictionary in which the keys are every type of word and the values are the freuency of each word in the input list.'''
		dic_frequencies = {}
		for review in list_words:
			for w in review:
				if (w in dic_frequencies):
					dic_frequencies[w] += 1
				else:
					dic_frequencies[w] = 1
		return dic_frequencies
	
	def sum_counts(self,list_words,dic_freq):
		'''Function that sums up all the frequencies of a given dictionary.'''
		sum_count = 0
		for word in list_words:
			if word in dic_freq:
				sum_count = sum_count + dic_freq[word]
		sum_count = sum_count
		return sum_count

