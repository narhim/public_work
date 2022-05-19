def calculate_prob(dic_freq,sum_counts):
	'''Function that given a dictionary of frequencies and a sum of counts, calculates the probabilty of each key applying Laplace smoothing. Returns the dictionary of probabilities.'''
	dic_prob = {}
	for word in dic_freq.keys():
		dic_prob[word] = (dic_freq[word] + 1)/ sum_counts
	return dic_prob


#def get_data(path):
#	'''Function that, given a path, extracts all the text in the text files tokeinzed in a list and also '''
#	files = []
#	for r, d, f in os.walk(path):
#		for file in f:
#			if '.txt' in file:
#				files.append(os.path.join(r, file))           
#	features = []
#	prior_p = len(files)
#	for f in files:
#		with open(f,"r",encoding = "utf-8") as file:
#			for line in file:
#				s_strip = line.strip()
#				p = re.compile('(\w)([?]|[!])')
#				texto = p.sub(r'\1 \2',s_strip)
#				p1 = re.compile('([?]|[!])(\w)')
#				texto1 = p.sub(r'\1 \2',texto)
#				s = re.split('["]|[(]|/|[-]{2, 3}|[..]| ',texto1)
#				review = []
#				for w in s:
#					review.append(w.lower())
#				features.append(review)		
#	return features,prior_p


#def tokenizer(list_lines):
#	#Initialize list where all words will be stored.			         
#	corpus = []
#	for line in list_lines:
#		#Separate characters by delimiters defined in regex.
#		s = re.split(' |[.] |[.]{2,}|[:]|[;]|[\']|["]|[„]|[‟]|[”]|[<]+|[>]+|[(]|[)]|[\[]|[\]]|[¿]|[?]|[¡]|[!]',line)
#		#Initialize list in which results from strip will be appended.
#		result = []
#		for element in s:
#			#Remove characters specified in regex from string.
#			s_r = element.strip('\n|[.]+|[:]|[,]|[;]|[«]|[»]|["]|[„]|[‟]|[”]|[<]+|[>]+|[\*]|[(]|[)]|[\[]|[\]]|[¿]|[?]|[¡]|[!]')
#			result.append(s_r)
#		 #Loop over results from strip for second clean up.
#		for w in result:
#			#Avoid empty strings and "===".
#			if (w=='') or (re.match('=+',w) != None):
#				continue
#			#Conditions for string with hyphens. And example for each condition is provided.
#			elif re.search('-',w) != None:
#				#5-5
#				if re.search('\d+-\d+',w):
#					numbers = re.split('-',w)
#					corpus.append(numbers[0].lower())
#					corpus.append(numbers[1].lower())
#				#cat-dog
#				elif re.search('[a-z]+-[a-z]+',w,flags=re.IGNORECASE):
#					corpus.append(w.lower())
#
#				#45-ben
#				elif re.search('\d+-\D+',w):
#					numbers = re.split('-',w)
#					corpus.append(numbers[0].lower())
#					corpus.append(numbers[1].lower())
#				#-32,9
#				elif re.match('-\d+',w):
#					corpus.append(w)
#				#alt- (from (alt-)griechisch)
#				elif re.search('[a-z]-',w,flags=re.IGNORECASE):
#					clean = w.strip('-')
#					corpus.append(clean.lower())
#				#-word
#				elif re.match('-\w+',w):
#					clean = w.strip('-')
#					corpus.append(clean.lower())
#				#45-
#				elif re.match('\d+-',w):
#					clean = w.strip('-')
#					corpus.append(clean.lower())
#				#-%45 and -«word
#				elif re.match('[-%\d+]|[-«\w+]',w):
#					clean = w.strip('[-%]|[-«]')
#					corpus.append(clean.lower())
#				#Avoid "-".
#				elif re.match('^-$',w):
#					continue
#			elif w == '/':
#				continue
#			elif re.search('[a-z]\/',w,flags=re.IGNORECASE):
#				splitted = w.split('/')
#				corpus.append(splitted[0].lower())
#				corpus.append(splitted[1].lower())
#			elif re.search('\d[.]\d',w):
#				corpus.append(w.lower())
#				#print(w)
#			#avoid the second type of hyphen found in raw text.
#			elif re.match('–',w):
#					continue
#			#If none of the conditions above apply, simply lower and apply.
#			else:
#				corpus.append(w.lower())
#	clean_corpus = [w for w in corpus if w not in stopwords.words('english')]
#	return clean_corpus
#
#def sent_tokenizer(text):
#	'''Function that given a raw texts returns a list of tokenized sentences.'''
#	#Split into raw tokens
#	corpus = []
#	sent_limit = '[.]|[!]|[?]|[:]'
#	split_text = text.split()
#	#Index for controlling sentences.
#	mark = 0
#	#Append in sentences to corpus_raw
#	for n,token in enumerate(split_text):
#		if (re.search(sent_limit,token) != None):
#			#Append initial sentence padding.
#			sent = []
#			#Remove all punctuation from each word.
#			for w in split_text[mark:(n+1)]:
#				word = ''
#				w = w.strip('\n|[”]|[“]')
#				for char in w:
#					if (char not in string.punctuation):
#						word += char
#				word = word.lower()
#				if word not in stopwords.words('english'):
#					sent.append(word)
#			corpus.append(sent)
#
#			#Update mark
#			mark = n+1
#		#We want to append sentence by sentence, so we continnue until we find an end mark.	
#		else:
#			continue
#
#	return corpus
#def calculate_freq(corpus):
#	'''Function that, given a list of words, returns a dictionary of frequencies of each word.'''
#	#Initialize dictionary
#	frequencies = {}
#	for word in corpus:
#		if word in frequencies:
#			#If word in dictionary add 1 to the frequency.
#			frequencies[word] += 1
#		else:
#			#Add word to dictionary if not in dictionary.
#			frequencies[word] = 1
#	return frequencies

	#vocab_train_neg_raw = set()
	#neg_text = []
	#for review in neg_text_training:
	#	for text in review:
	#		tokens_neg = pre_processer.tokenizer(text)
	#		neg_text.append(tokens_neg)
	#		vocab_train_neg_raw.update(tokens_neg)
		#print(pos_text_training)

	#pos_text = pre_processer.tokenizer(pos_text_training)
	#with open('tokens.txt',"w",encoding = "utf-8") as file:
	#	for token in pos_text:
	#		file.write(token + '\n')
	#neg_text = pre_processer.tokenizer(neg_text_training)
	#with open('tokens_neg.txt',"w",encoding = "utf-8") as file:
	#	for token in neg_text:
	#		file.write(token + '\n')
	#vocab_train_pos_raw = set()
	#pos_text = []
	#for review in pos_text_training:
	#	for text in review:
	#		tokens_pos = pre_processer.tokenizer(text)
	#		pos_text.append(tokens_pos)
	#		vocab_train_pos_raw.update(tokens_pos)
		#pos_text_training, pos_num_files = path.raw_text_n_files('train/pos')
	#neg_text_training, neg_num_files = path.raw_text_n_files('train/neg')

		#####sum(count(w,c)) for all words in vocabulary
	#sum_pos = count.sum_counts(vocabulary,pos_counts)
	#sum_neg = count.sum_counts(vocabulary,neg_counts)