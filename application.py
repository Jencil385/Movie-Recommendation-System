import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ccf883124ebbe95b879defdd565a8d0f&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def fetch_reviews(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}/reviews?api_key=ccf883124ebbe95b879defdd565a8d0f&language=en-US&page=1'.format(movie_id))
    data=response.json()
    reviews = [review['content'] for review in data['results'][:2]]
    return reviews

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[0:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    recommended_movies_reviews=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        #fetch reviews from api
        recommended_movies_reviews.append(fetch_reviews(movie_id))
    return recommended_movies,recommended_movies_posters,recommended_movies_reviews

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.set_page_config(page_title="Movie Recommender System", page_icon=":film_strip:", layout="wide")

st.title("Movie Recommender System")

selected_movie_name=st.selectbox(
    'Choose a movie:',
    movies['title'].values, format_func=lambda x: x.title(), index=0
)

if st.button('Recommend'):
    recommended_movies, recommended_movies_posters, recommended_movies_reviews = recommend(selected_movie_name)

    st.write("Based on your selection of `%s`, we recommend the following movies:" % selected_movie_name)
    st.write("---")

    for i, movie in enumerate(recommended_movies):
        st.write("%d. %s" % (i + 1,movie))
        st.image(recommended_movies_posters[i], width=200)
        st.write("---")
        st.write("Top Reviews:")
        for review in recommended_movies_reviews[i]:
            st.write("- %s" % review)
            st.write("---")
