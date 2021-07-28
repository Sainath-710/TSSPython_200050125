import os
import random
import re
import sys
import numpy as np
import pandas as pd

DAMPING = 0.85
SAMPLES = 10000


def crawl(directory):
        """
        Parse a directory of HTML pages and check for links to other pages.
        Return a dictionary where each key is a page, and values are
        a list of all other pages in the corpus that are linked to by the page.
        """
        pages = dict()

        # Extract all links from HTML files
        for filename in os.listdir(directory):
                if not filename.endswith(".html"):
                        continue
                with open(os.path.join(directory, filename)) as f:
                        contents = f.read()
                        links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
                        pages[filename] = set(links) - {filename}

        # Only include links to other pages in the corpus
        for filename in pages:
                pages[filename] = set(
            		link for link in pages[filename]
            		if link in pages
        	)

        return pages

def transition_model(corpus, page, damping_factor):
        probabilities = dict()		#Dictionary to store probabilities
        total = len(corpus)	#Total number of pages in the corpus
        linked = len(corpus[page])+1		#Number of pages linked to the current page
        non_linked = total - linked	#No. of pages not linked to the present page
        for link in corpus:
                if link in corpus[page] or link == page:
                        probabilities[link] = damping_factor/linked
                else:
                        probabilities[link] = (1-damping_factor)/non_linked

        return probabilities

def sample_pagerank(corpus, damping_factor, n):
        pagenumbers_list = []
        list_of_keys = []
        count_dict = dict()
        for i in corpus.keys():
                count_dict[i] = 0
                list_of_keys.append(i)
        for i in range(1, len(corpus)+1):
                pagenumbers_list.append(i)
        first = random.randint(1, len(corpus))
        present = list_of_keys[first-1]
        for l in range(1, n+1):
                probabilities_dict = transition_model(corpus, present, damping_factor)		#Get the probabilities
                probabilities_list = []
                for i in probabilities_dict:
                        probabilities_list.append(probabilities_dict[i])
                count_dict[present]+=1
                next_page = random.choices(pagenumbers_list, weights = probabilities_list, k = 1)[0]
                present = list_of_keys[next_page-1]
        prob_dict = dict()
        for i in list_of_keys:
                prob_dict[i] = count_dict[i]/n
        return prob_dict

def check(previous, present):
        for i in previous.keys():
                if not (abs(previous[i] -present[i])<=0.001):
                        return False
        return True

def iterate_pagerank(corpus, damping_factor):
        N = len(corpus)         #Total number of pages in the corpus
        pageRanks = dict()
        linkedPages = dict()
        for i in corpus.keys():
                pageRanks[i] = 1/N
                linkedPages[i] = []
        for i in corpus.keys():
                if len(corpus[i]) == 0:		#For pages not linked to any other page
                        for k in corpus.keys():
                                corpus[i].add(k)
        for i in corpus.keys():
                for j in corpus[i]:
                        linkedPages[j].append(i)
        pageRanks_duplicate = pageRanks.copy()
        for i in corpus.keys():
                pageRanks[i] = (1-damping_factor)/N
                frac_sum = 0
                for j in linkedPages[i]:
                        frac_sum += pageRanks_duplicate[j]/len(corpus[j])
                pageRanks[i] += damping_factor*frac_sum
        while (not(check(pageRanks, pageRanks_duplicate))):
                pageRanks_duplicate = pageRanks.copy()
                for i in corpus.keys():
                        pageRanks[i] = (1-damping_factor)/N
                        frac_sum = 0
                        for j in linkedPages[i]:
                                frac_sum += pageRanks_duplicate[j]/len(corpus[j])
                        pageRanks[i] += damping_factor*frac_sum
        return (pageRanks)

def main(dir):
    corpus = crawl(dir)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

main("corpus2")		#Use "corpus0" or "corpus1" or "corpus2" here

        
