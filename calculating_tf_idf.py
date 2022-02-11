import pandas as pd
import json
from collections import Counter
import math
import argparse
import sys

def clean_ponctuation(string):
    """
    (string) --> string
    This function is a helper function which takes as input a string and replace some 
    of its punctuation with whitespace
    """
    remove = '()[],-.?!:;#&'
    trans = str.maketrans(remove, ' '*len(remove))
    return string.translate(trans)


def word_count(df):
    """
    (pandas data frame) --> json dictionary
    This function takes as input a pandas df. It will return a json dictionary containing
    all the words and their number of occurences for each topics.
    """
    
    topics = ['lawsuit','vote count', 'pandemic related','pol opi', 'trump a', 'trump c']
    df['title'] =df['title'].apply(clean_ponctuation)
    
    word_by_topics = {}
    dict1  ={}
    for topic in topics:
        dict1[topic] = df[df[topic]=='y']
        words = []
        titles = dict1[topic]['title'].tolist()
        total = []
        for i in range(len(titles)):
            words = titles[i].split()
            for word in words:
                to_add = word.lower()
                total.append(to_add)
    
        is_word = []
        for word in total:
            if word.isalpha():
                is_word.append(word)
        
        topics_dict = dict(Counter(is_word))
        final = {}
        for key,value in topics_dict.items():
            if value >=2:
                final[key] = value
                
        word_by_topics[topic] = final
            
    json_out = json.dumps(word_by_topics,indent = 4)
    
    return json_out


def add_words(file1,file2,file3,file4,file5,file6):
    """
    (file) --> list
    Takes as input files and returns a list of lists which contains all the words alpha words 
    used in each file.
    """
    list_of_lists = []
    list_of_files = [file1,file2,file3,file4,file5,file6]
    
    for file_in in list_of_files:
        words_in_file = []
        file_to_read = open(file_in,'r')
        for line in file_to_read:
            words = line.split()
            for word in words:
                if word.isalpha():
                    words_in_file.append(word)
    list_of_lists.append(words_in_file)
    
    return list_of_lists


def ComputeTF_IDF(data,term,d,list_of_lists):
    """
    (this take a json dictionary, a word, a topic, and a list of lists)
    This will return the tf idf score of a single word.
    """
    # For the TF part we start a zero and then add 
    # all the words which occur
    sum_d = 0
    for w in data[d]:
        sum_d += data[d][w]
    TF = data[d][term]/sum_d

    sum_occurences = 0
    for lists in list_of_lists:
        if term in lists:
            sum_occurences += 1
    if sum_occurences == 0:
        sum_occurences = 1        
    IDF = (6/sum_occurences)
    return TF * math.log(IDF)
   
    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('in_file',help = 'the file that will be used as input')
    parser.add_argument('-p','--in_file2', nargs= "?" ,default ='hey') #how to fix the optinal argument  
    args = parser.parse_args()
    
    # We put our csv from task 2 into a dataframe. This csv has been annotated.
    df = pd.read_csv(args.in_file)
    
    #Now our code will depend on whether we want to see the two files merged or not!
    massive_list = add_words('hot_con_trump18.json','hot_con_trump19.json','hot_con_trump20.json',
                         'hot_pol_trump18.json','hot_pol_trump19.json','hot_pol_trump20.json')
    if len(sys.argv) == 3:
        df_optional = pd.read_csv(args.in_file2)
        frames = [df,df_optional]
        merged_df = pd.concat(frames)
        
        words_count_dict = json.loads(word_count(merged_df))
        words_dic = {}
       
        num_words = 10
        
        for topic in words_count_dict:
            
            tf_idf = {}
            for word in words_count_dict[topic]:
                tf_idf[word] = ComputeTF_IDF(words_count_dict,word, topic,massive_list)
            tf_idf_df = pd.DataFrame.from_dict(tf_idf, orient='index', columns=['TF-IDF'])
            tf_idf_df.sort_values(by=['TF-IDF'],ascending=False, inplace=True)
            tf_idf_list = []
            for i in range(num_words):
                tf_idf_list.append(tf_idf_df.iloc[i].name)
            
            words_dic[topic] = tf_idf_list
        out = json.dumps(words_dic)
        out = out.replace('{','{\n')
        out = out.replace('],','],\n')
        out = out.replace('}','\n}')
        
        print("merged")
        print(out)
            
    elif len(sys.argv) == 2:
        
    
        words_count_dict = json.loads(word_count(df))
        words_dic = {}
        
        num_words = 10
      
        
        for topic in words_count_dict:
            
            tf_idf = {}
            for word in words_count_dict[topic]:
                tf_idf[word] = ComputeTF_IDF(words_count_dict,word, topic,massive_list)
            tf_idf_df = pd.DataFrame.from_dict(tf_idf, orient='index', columns=['TF-IDF'])
            tf_idf_df.sort_values(by=['TF-IDF'],ascending=False, inplace=True)
            tf_idf_list = []
            for i in range(num_words):
                tf_idf_list.append(tf_idf_df.iloc[i].name)
            
            words_dic[topic] = tf_idf_list
        out = json.dumps(words_dic)
        out = out.replace('{','{\n')
        out = out.replace('],','],\n')
        out = out.replace('}','\n}')
        
        print("single")
        print(out)

if __name__ == '__main__':
    main()
