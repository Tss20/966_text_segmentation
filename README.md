This project involves using a bigram model in order to assess the likelihood of a given segmentation of a sentence without spaces. 
The function of each code file is the following:

generate_fake.py: When run, creates samples of a fake "language". This language is constructed based on a pcfg, with probabilities randomly generated. Vocabulary has already been defined in the file, and have been chosen to result in unsegmented text with ambiguous word boundaries. Will create a training_data.txt, which can be fed directly into training, and a testing_data.txt, which are more unique sentences generated by the pcfg, both unsegmented and segmented, for testing
purposes.

training.py: When run, uses text from training_data.txt to find bigram probabilities, marginial probabilities, and optimizes smoothing and interpolation hyperparameters. Creates Conditional.csv (bigram probabilities), Marginials.csv (marginial probabilities), and Paramcsv (two hyperparameters), that can be used to assess likelihood of segmentation. This ngram model uses both additive smoothing and interolation with marginial probability (i.e. likelihood is calculated through
expression l * bigram_probability + (1-l) * marginial_probability where l is a hyperparameter optimized using Maximum Log Likelihood)

util.py: Contains a number of function to aid with the above code, including code to save and unpack ngram model data.

assess.py: Plots the log likelihood of each possible segmentation given in the embedded list data that is present in code. This code is not currently generalizable, and was specifically meant for assessing results discussed in paper.
