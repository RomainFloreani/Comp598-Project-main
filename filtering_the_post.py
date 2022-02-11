import json
import pandas as pd
import re
import random
import argparse


def get_post_titles(inp):
    """
    (file) --> (list)
    this function takes as input a file with Reddit post collected with the reddit API
    returns a list of all the titles of each of the posts.
    """
    list_of_titles = []
    file_in = open(inp,'r')
    for line in file_in:
        
        data = json.loads(line)
        list_of_titles.append(data['data']['title'])
    return list_of_titles
    


def get_titles_by_candidate(list_of_titles, candidate):
    """
    (list, string (biden or trump in lower case)) --> list
    
    This takes as input a list of post titles and returns a list of post titles containing 
    the name of the candidate.
    """
    if candidate != 'trump' and candidate != 'biden':
        raise ValueError ('candidate must be equal to "trump" or "biden" ') 
    
    titles_containing_the_candidate = []
    for title in list_of_titles:
        lower_title = title.lower()
        if re.search(f"[^0-9a-zA-Z]{candidate}[^0-9a-zA-Z]", lower_title) or re.search(f"{candidate}[^0-9a-zA-Z]", lower_title):
            titles_containing_the_candidate.append(title)
    
    return titles_containing_the_candidate

    
def choose_random_line(list_of_post, num_post):
    """
    (list, int) --> list
    This function takes as input a list of titles posts and a number. 
    It returns a list of list of length of that number containing radomly selected posts
    from list_of_posts.
    """
    
    random_post = []
    
    while(len(random_post) < num_post):
        mytitle = list_of_post.pop(random.randint(0,len(list_of_post)-1))
        random_post.append(mytitle)
    return random_post


   
    
        
def main():
    parser =  argparse.ArgumentParser()
    parser.add_argument('input_file_d1', help = 'this is the file for one of your reddit post collection')
    parser.add_argument('input_file_d2')
    parser.add_argument('input_file_d3')
    parser.add_argument('-c','--candidate')
    parser.add_argument('-o','--output_file')
    args = parser.parse_args()
    
    ## We now get the list of titles for the 3 days we collected the reddit data from
    titles_day1 = get_post_titles(args.input_file_d1)
    titles_day2 = get_post_titles(args.input_file_d2)
    titles_day3 = get_post_titles(args.input_file_d3)
    
    # Now from the lists of titles from the 3 days we get the ones containing the name of 
    # of the candidate of our choice
    candidate_titles_day1 = get_titles_by_candidate(titles_day1, args.candidate)
    candidate_titles_day2 = get_titles_by_candidate(titles_day2, args.candidate)
    candidate_titles_day3 = get_titles_by_candidate(titles_day3, args.candidate)
    
    
    # We now chose randomly for the three list of titles containign 
    shortlist_day1 = choose_random_line(candidate_titles_day1,66)
    shortlist_day2 = choose_random_line(candidate_titles_day2,66)
    shortlist_day3 = choose_random_line(candidate_titles_day3,66)
        
        
    
    sample_titles = []
    larger_list = [shortlist_day1,shortlist_day2]#,shortlist_day3]
    for sublist in larger_list:
        for title in sublist:
            sample_titles.append(title)
    
    
    
    posts = {'titles': sample_titles}
    
    df = pd.DataFrame(posts,columns = ['titles'])
    
    df.to_csv(f'{args.output_file}.csv', index = False, encoding = 'utf-8')
    
if __name__ == '__main__':
    main()
