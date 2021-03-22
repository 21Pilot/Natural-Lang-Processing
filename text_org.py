## Hyomin Seo
## Natural Language Processing 
## ECE 467_2021 Spring 
## Professor Sable
## Project 1_Text Categorizer 

# NLTK 
# INSTALLATION OF NLTK AND OTHER PACKAGES
# http://www.nltk.org/install.html 
# http://www.nltk.org/data.html

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
# from nltk.stem.lancaster import LancasterStemmer

from math import log 
import numpy as np
import string 

# PorterStemmer 
pstem = PorterStemmer() 

# Required User Inputs
# train_input = "corpus1_train.labels"
train_input = input("Type the name of the file that contains labeled list of training documents: ")

# test_input = "corpus1_test.list"
test_input = input("Type the name of the file that contains list of testing documents to be categorized: ")

# Construct text categorization system 
def txt_categorizer(train_input = 0, test_input = 0):
  
    # Processing Training documents 
    # Seperation 
    train_list = open(train_input, 'r')
    train_list_lines = train_list.read().splitlines()
    
    # Declaration of each seperate dictionary 
    # 1_Dictionary for token count per category 
    # cat = category 
    diction_token_cat = dict()
    
    # 2_Dictionary for specific words per category based on training
    diction_word_cat = dict()
    
    # 3_Dictionary for files count per category to get previous file info 
    diction_prev_file_cat = dict()

    # Additive smoothing constant k 
    k = 0.065

    # Looping through Training list 
    # 1_Loop through each seperated line of training list 
    for line in train_list_lines: 
        # Process lines into string info list of file name and category 
        train_file_cat = line.split()
        
        # Read and find the address and the category of the training file
        train_file = open(train_file_cat[0],'r')
        # Set category of the training file
        train_cat = train_file_cat[1]
        
        # Tokenization on the training file 
        train_token = word_tokenize(train_file.read())
        
        # Counting the viewed categories 
        if train_cat in diction_prev_file_cat:
          diction_prev_file_cat[train_cat] += 1.
        else:
          diction_prev_file_cat[train_cat] = 1.

        # Loop_2 through words of the training list 
        for tr_token in train_token : 

            # Stemmer
            # Apply stemmer to token cut out inflection 
            tr_token = pstem().stem(tr_token) 
            
            # Counting how many times the word shows up in the category 
            # Appearance of word bound token in the category 
            if (tr_token, train_cat) in diction_word_cat : 
                diction_word_cat[(tr_token, train_cat)] +=1.
            else:
                diction_word_cat[(tr_token, train_cat)] = 1.
            if train_cat in diction_token_cat:
                diction_token_cat[train_cat] +=1.
            else:
                diction_token_cat[train_cat] = 1.

        # Storing 
        # Store total number of training files
        total_train_file = sum(diction_prev_file_cat.values())
        # Assign category names into a list 
        name_cat  = diction_token_cat.keys()
        
        ## Testing
        
        # Prediction
        predictions = []
        
        # Testing documents processing 
        # Seperation 
        test_list = open(test_input, 'r')
        test_list_lines = test_list.read().splitlines()
        
        # Looping through the Testing list 
        # 1_Loop through each seperated line of testing list file 
        for line in test_list_lines: 
            
            # Process lines into string info file 
            test_flie = open(line, 'r')
        
            # Tokenization
            test_token = word_tokenize(test_file.read())
            
            # Declaration of each dictionary 
            # Total token per category 
            diction_token_test = dict()
    
            # Specific words per category 
            # prob = probability
            category_log_prob = dict()
            
            # Calcualte Vocabulary size of the test file
            for ts_token in test_token:
                
                # Stemmer
                # Apply stemmer to token to  cut out inflection 
                ts_token = pstem().stem(ts_token) 
            
                # Counting how many times the word shows up in the category 
                # Appearance of token in the category 
                if ts_token in list(string.punctuation):
                    pass  
                else:
                    if ts_token in diction_token_test:
                      diction_token_test[ts_token] += 1.
                    else:
                      diction_token_test[ts_token] = 1.
                    
            vocab_test_size = len(diction_token_test)
          
            
            for category in name_cat:

                # Conditional Probability
                # Total conditional probability of article in the specific Category 
                
                total_cat_log_prob = 0.
                
                # Based on training set, calcualte previous categorical probability
                cat_prev_prob = diction_prev_file_cat[category] / total_train_file
                
                # Normalization 
                # Smoothing coeffiecent additive agent 
                normalization = diction_token_cat[category] + k*(vocab_test_size)
                
                # Conditional Categorical Probability Calculation
                # k smoothing coeffiecent 
                for word, count in diction_token_test.iteritems():
                    if (word, category) in diction_word_cat:
                        count_word_cat = diction_word_cat[(word, category)] + k 
                    else:
                        count_word_cat = k 
                    
                    cat_log_prob = count*log(count_word_cat / normalization) 
                    total_cat_log_prob += cat_log_prob
                category_log_prob[category] = total_cat_log_prob + log(cat_prev_prob)
                
            # Make category decision by showing the highest probability 
            cat_decision = max(category_log_prob, key = category_log_prob.get)
            
            # Construct string to write for each line of output file
            # append the output to the list 
            str = line + '' + cat_decision + '\n' 
            predictions.append(str)
            
    # Input of Output file name by User
    user_input = input('Enter a name for the category prediction output file: ') 

    # Final Decision 
    output_final = open(user_input, 'w')
    for line in predictions: 
        output_final.write(line)
    output_final.close() 
    return 

#Call to text categorization function
txt_categorizer(train_input, test_input)
