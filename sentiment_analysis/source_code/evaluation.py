#Calculate and print the scores
def calculate_scores(results_pos,results_neg):
	def count_sign(results,label):
		true = 0
		false = 0
		for result in results:
			if result == label:
				true += 1
			else:
				false += 1
		return true,false
	true_pos,false_neg = count_sign(results_pos,'pos')
	true_neg,false_pos = count_sign(results_neg,'neg')
	accuracy = (true_neg + true_pos) / (true_pos + true_neg + false_pos + false_neg)
	precision = true_pos/(true_pos + false_pos)
	recall = true_pos/(true_pos + false_neg)
	fscore = 2*((precision*recall)/(precision+recall))
	print('The accuracy is: ' + str(accuracy))
	print('The precision is: ' + str(precision))	
	print('The recall is: ' + str(recall))
	print('The f-score is: ' + str(fscore))