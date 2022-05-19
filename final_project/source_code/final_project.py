# python 3.6.7
#!/usr/bin/python
# -*- coding: utf-8 -*-
#Modules needed
import pre_processer
import evaluation
import classifier
import count
import os


def main():
	#Get the training data
	path = pre_processer.get_data()
	pos_text_training, pos_num_files = path.list_raw_text_n_files("./aclImdb/train/pos")
	neg_text_training, neg_num_files = path.list_raw_text_n_files('./aclImdb/train/neg')

	pos_train_tokenizer = pre_processer.tokenize(pos_text_training)
	pos_text,vocab_train_pos_raw = pos_train_tokenizer.tok_2_list()
	pos_text_binary = pos_train_tokenizer.tok_2_set()
	neg_train_tokenizer = pre_processer.tokenize(neg_text_training)
	neg_text,vocab_train_neg_raw = neg_train_tokenizer.tok_2_list()
	neg_text_binary = neg_train_tokenizer.tok_2_set()

	######P(w|c) in training
	######Count the frequencies count(w|c)
	counting = count.count()
	pos_counts = counting.list_abs_freq(pos_text)
	neg_counts = counting.list_abs_freq(neg_text)
	pos_counts_binary = counting.list_abs_freq(pos_text_binary)
	neg_counts_binary = counting.list_abs_freq(neg_text_binary)
	#with open('pos_freq.txt',"w",encoding = "utf-8") as file:
#	#	for k,v in pos_counts.items():
#	#		file.write(str(k) + '\t' + str(v) + '\n')
#
	#######Get the vocabulary
	vocabulary = set(pos_counts.keys()).union(set(neg_counts.keys()))
	#vocabulary = set(path.list_from_file('imdb.vocab'))
	#vocabulary = vocab_train_pos_raw.union(vocab_train_neg_raw)

	####with open('vocabulary.txt',"w",encoding = "utf-8") as file:
	####	for k in vocabulary:
	####		file.write(str(k) + '\n')
	#####Extract the features for testing, the gold list is the number of files of each directory.
	pos_text_test, pos_num_files_test = path.list_raw_text_n_files('./aclImdb/test/pos')
	neg_text_test, neg_num_files_test = path.list_raw_text_n_files('./aclImdb/test/neg')
	pos_test_tokenizer = pre_processer.tokenize(pos_text_test)
	pos_features,vocab_test_pos_raw = pos_test_tokenizer.tok_2_list()
	pos_features_binary = pos_test_tokenizer.tok_2_set()
	neg_test_tokenizer = pre_processer.tokenize(neg_text_test)
	neg_features,vocab_test_neg_raw = neg_test_tokenizer.tok_2_list()
	neg_features_binary = neg_test_tokenizer.tok_2_set()

	#vocab_test_pos = set(word for word in vocab_test_pos_raw if word in vocabulary)
	#vocab_test_neg = set(word for word in vocab_test_neg_raw if word in vocabulary)
	sum_pos = sum(pos_counts.values())
	sum_neg = sum(neg_counts.values())
	sum_pos_binary = sum(pos_counts_binary.values())
	sum_neg_binary = sum(neg_counts_binary.values())

##	##	##p(c) = N_c/N_doc			
##	####Calculate the total number of documents
	sum_files = pos_num_files + neg_num_files
##	#####Calculate the prior probabilities for both classes	
	prior_prob_pos = pos_num_files/sum_files
	prior_prob_neg = neg_num_files/sum_files
	#############Classify the reviews.
	init_classifier = classifier.nb_classifier(prior_prob_pos,prior_prob_neg,'pos','neg',vocabulary)
	results_pos = init_classifier.classify(pos_features,pos_counts,neg_counts,sum_pos,sum_neg)
	results_neg = init_classifier.classify(neg_features,pos_counts,neg_counts,sum_pos,sum_neg)
	results_pos_binary = init_classifier.classify(pos_features_binary,pos_counts_binary,neg_counts_binary,sum_pos_binary,sum_neg_binary)
	results_neg_binary = init_classifier.classify(neg_features_binary,pos_counts_binary,neg_counts_binary,sum_pos_binary,sum_neg_binary)
#####
#####	###########Calculate and print the scores
	evaluation.calculate_scores(results_pos,results_neg)
	evaluation.calculate_scores(results_pos_binary,results_neg_binary)
#####
#####

if __name__=='__main__':
	main()
