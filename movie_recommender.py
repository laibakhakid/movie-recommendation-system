import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle
credits=pd.read_csv("tmdb_5000_credits.csv")
movies=pd.read_csv("tmdb_5000_movies.csv")
movies=movies.merge(credits,on='title')
# genre,id,keywords,title,overview,cast,crew.......> worthy so we will use these columns
movies=movies[['genres','movie_id','keywords','title','overview','cast','crew']]
movies.dropna(inplace=True)
movies.isnull().sum()
movies.duplicated().sum()
print(movies.iloc[0].genres)
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)
def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
         L.append(i['name'])
         counter+=1
        else:
           break
    return L
movies['cast']=movies['cast'].apply(convert3)
def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
         L.append(i['name'])
         break
    return L
movies['crew']=movies['crew'].apply(fetch_director)
movies['overview']=movies['overview'].apply(lambda x:x.split())

movies['genres']=movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x: [i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x: [i.replace(" ","") for i in x])
movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']
new_df=movies[['movie_id','title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()
ps=PorterStemmer()
def stem(text):
   y=[]
   for i in text.split():
      y.append(ps.stem(i))
   return " ".join(y)
new_df['tags']=new_df['tags'].apply(stem)
similarity=cosine_similarity(vectors)
def recommend(movie):
   movie_index=new_df[new_df['title']==movie].index[0]
   distances=similarity[movie_index]
   movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
   for i in movie_list:
      print(new_df.iloc[i[0]].title)
recommend("Avatar")
import pickle

with open('movies.pkl', 'wb') as f:
    pickle.dump(new_df, f)
pickle.dump(similarity,open('similarity.pkl','wb'))
# import os
# print(os.getcwd())