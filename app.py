import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster from the movie API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e399b7597a4bee0336ca12dc2db137df&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']  # Remove extra indentation here

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title) # appending the movie name to the recommended_movies list
        recommended_movies_posters.append(fetch_poster(movie_id)) # calling the fetch_poster function to get the movie poster
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb')) # loading the movie dictionary
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb')) # loading the similarity scores

st.title('Movie Rec System')

#creating a selectbox for user input
selected_movie_name = st.selectbox(
    'Which movie do you like to watch today?',
    movies['title'].values) 

#creating a button in the main app page that takes the user to our about page
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])   
