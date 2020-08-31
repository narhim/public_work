import xml.etree.cElementTree as ET
import re
from nltk.corpus import stopwords
def read_xml(path):
#Get document
	with open(path) as f:
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
	return dic_raw_doc
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
					corpus.append(numbers[0].lower())
					corpus.append(numbers[1].lower())
				#cat-dog
				elif re.search('[a-z]+-[a-z]+',w,flags=re.IGNORECASE):
					corpus.append(w.lower())

				#45-ben
				elif re.search('\d+-\D+',w):
					numbers = re.split('-',w)
					corpus.append(numbers[0].lower())
					corpus.append(numbers[1].lower())
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
					corpus.append(clean.lower())
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
				corpus.append(w.lower())
				#print(w)
			#avoid the second type of hyphen found in raw text.
			elif re.match('–',w):
					continue
			#If none of the conditions above apply, simply lower and apply.
			else:
				if w not in stopwords.words('english'):
						corpus.append(w.lower())
	return corpus



def sent_tokenizer(text):
	'''Function that given a raw texts returns a list of tokenized sentences.'''
	#Split into raw tokens
	corpus = []
	sent_limit = '[.]|[!]|[?]|[:]'
	split_text = text.split()
	#Index for controlling sentences.
	mark = 0
	#Append in sentences to corpus_raw
	for n,token in enumerate(split_text):
		if (re.search(sent_limit,token) != None):
			#Append initial sentence padding.
			sent = []
			#Remove all punctuation from each word.
			for w in split_text[mark:(n+1)]:
				word = ''
				w = w.strip('\n|[”]|[“]')
				for char in w:
					if (char not in string.punctuation):
						word += char
				sent.append(word.lower())
			corpus.append(sent)

			#Update mark
			mark = n+1
		#We want to append sentence by sentence, so we continnue until we find an end mark.	
		else:
			continue

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

