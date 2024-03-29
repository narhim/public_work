import re
import os
class get_data:
	"""class with different methods of reading data from path"""

	def raw_text_n_files(self,path):
		files = []
		for r, d, f in os.walk(path):
			for file in f:
				if '.txt' in file:
					files.append(os.path.join(r, file))           
		text = ''
		prior_p = len(files)
		for f in files:
			with open(f,"r",encoding = "utf-8") as file:
				text += file.read()	
		return text,prior_p

	def list_raw_text_n_files(self,path):
		list_files = []
		for root, directories, files in os.walk(path):
			for file in files:
				if '.txt' in file:
					list_files.append(os.path.join(root, file))           
		text = []
		prior_p = len(list_files)
		for f in list_files:
			with open(f,"r",encoding = "utf-8") as file:
				text.append([file.read()])
		return text,prior_p

	def list_from_file(self,path):
		'''Function that given a file, saves in a list each line stripped. Returns that list.'''
		list_items = []
		with open(path,"r",encoding = "utf-8") as file:
			for line in file:
				w = line.strip()	
				list_items.append(w)
			return list_items

class tokenize:
	def __init__(self,list_list_raw_text):
		self.list_list_raw_text = list_list_raw_text

	def tokenizer_1(self,raw_text):
		features = []
		#Break by line
		lines = raw_text.split('<br /><br />')
		marca = re.compile('\.|,|-|_|\*|\+|\"|„|‟|”|[<]+|[>]+|\[|\]|[-]+|[\']|\^|´')
		signs = re.compile('[!]+|(:\))|(:\()|(;\))|(;\()|(:P)|(:D)|(;D)|/')
		emo_items = re.compile('[;]|[:]|[\(]|[\)]')
		for line  in lines:
			words = line.split()
			for word in words:
				elements = marca.split(word)
				for element in elements:
					if signs.search(element):
						matched = signs.search(element)
						if matched.start() != 0 and matched.end() != len(element): 
							features.append(element[0:matched.start()].lower())
							features.append(element[matched.start():matched.end()])
							features.append(element[matched.end():len(element)].lower())
						elif matched.start() == 0 and matched.end() != len(element): 
							features.append(element[matched.start():matched.end()])
							features.append(element[matched.end():len(element)].lower())
						elif matched.start() == 0 and matched.end() == len(element): 
							features.append(element[matched.start():matched.end()])
					elif emo_items.search(element):
						elementos = emo_items.split(element)
						for elemento in elementos:
							if elemento != '':
								#Maybe it's repeating appending of elements?
								features.append(elemento.lower())
					elif re.search('[!]+$',element):
						word = element.strip('[!]+')
						features.append(word.lower())
					elif element != '':	
						features.append(element.lower())
		return features

	def tok_2_list(self):
		list_list_tokens = []
		vocabulary = set()
		for review in self.list_list_raw_text:
			for text in review:
				tokens = self.tokenizer_1(text)
				list_list_tokens.append(tokens)
				vocabulary.update(tokens)
		return list_list_tokens,vocabulary

	def tok_2_set(self):
		list_list_tokens = []
		vocabulary = set()
		for review in self.list_list_raw_text:
			for text in review:
				tokens = self.tokenizer_1(text)
				list_list_tokens.append(set(tokens))
				vocabulary.update(tokens)
		return list_list_tokens