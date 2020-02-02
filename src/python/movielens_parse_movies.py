import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
if __name__ == '__main__':

    #Init
    os.system('clear')
    genre_threshold = 1.00
    datadir = '/Volumes/3-1TB-LaCie/data/movielens/'

    #Load Movies
    movies = pd.read_csv(datadir + '/raw/movies.csv')
    
    #Extract Genres
    genres = {}
    genrelist = movies['genres'].values
    for item in genrelist:
        elements = item.split('|')
        for element in elements:
            element = element.lower()
            if (element in genres):
                count = genres[element]
                genres[element] = count + 1
            else:
                genres[element] = 1
    
    #Remove genres below a certain percentage
    total = 0
    for item in genres:
        total = total + genres[item]
    for item in genres:
        genres[item] = float(genres[item]) / float(total) * 100.0
    genres_lite = {}
    genres_index = {}
    index = 0
    for i,item in enumerate(genres):
        percentage = genres[item]
        if (percentage > genre_threshold):
            genres_lite[item] = index
            genres_index[index] = item
            index += 1

    #Compute Co-occurence Matrix
    genre_names = []
    for i in range(len(genres_lite)):
       genre_names.append(genres_index[i])
    cooccurences = np.zeros((len(genres_lite),len(genres_lite)))
    for item in genrelist:
        elements = item.split('|')
        for element1 in elements:
            element1 = element1.lower()
            for element2 in elements:
                element2 = element2.lower()
                if (element1 != element2):
                    if (element1 in genres_lite):
                        if (element2 in genres_lite):
                            index1 = genres_lite[element1]
                            index2 = genres_lite[element2]
                            cooccurences[index1,index2] += 1
    
    #Plot
    plt.figure(figsize=(8,8))
    plt.imshow(cooccurences)
    plt.xticks(range(len(genres_lite)),genre_names,rotation=-90,fontsize=12)
    plt.yticks(range(len(genres_lite)),genre_names,fontsize=12)
    plt.tight_layout()
    plt.savefig('src/python/movielens_cooccurences.png')

    
            

