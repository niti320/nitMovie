import pickle
import requests
import streamlit as st

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        data = requests.get(url)
        data.raise_for_status()  
        poster_path = data.json().get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"

def fetch_rating(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        data = requests.get(url)
        data.raise_for_status()
        rating = data.json().get('vote_average')
        return rating
    except Exception as e:
        print(f"Error fetching rating: {e}")
        return None

movies = pickle.load(open("movieL.pkl", 'rb'))
simi = pickle.load(open("simi.pkl", 'rb'))
MovieL = movies['title'].values

st.set_page_config(page_title="Movie Recommendations Engine", layout="centered")
st.header("Select Your Favorite Movie!") 

selectvalue = st.selectbox("", MovieL)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(simi[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    recommend_ratings = []
    for i in distance[1:7]: 
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies.iloc[i[0]].id))  
        recommend_ratings.append(fetch_rating(movies.iloc[i[0]].id))  
    return recommend_movie, recommend_poster, recommend_ratings

# State to manage loading status
if 'loading' not in st.session_state:
    st.session_state.loading = False

if st.session_state.loading:
    st.markdown("Loading recommendations, please wait...")
else:
    if st.button("Show Recommendations"):
        st.session_state.loading = True  # Set loading to True
        with st.spinner("Loading recommendations..."):
            movie_name, movie_poster, movie_ratings = recommend(selectvalue)
        st.session_state.loading = False  # Reset loading after completion

        # Display recommended movies
        cols = st.columns(3)  
        for i in range(6): 
            with cols[i % 3]:  
                st.image(movie_poster[i], use_column_width=True, caption=f"Rating: {movie_ratings[i]}")
                st.write(movie_name[i])  
                st.write("")

# Custom CSS for loading overlay and styling
st.markdown(
    """
    <style>
        /* Loading Overlay */
        .streamlit-spinnerOverlay {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background-color: rgba(0, 0, 0, 0.6);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            pointer-events: all;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Your existing styles remain unchanged
st.markdown(
    """
    <style>
        /* Existing styles remain unchanged */
        * {
            border-color: #12e9b3 !important;
        }
        body {
            background-color: #121212;
            color: #ffffff;
            height: 100vh;
            gap: 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Arial', sans-serif;
        }
        .stImage > div > div > p {
            color: black;
            font-weight: bold;
        }
        .stSelectbox {
            margin: 0;
        }
        
        h1 {
            color: #181818;
            font-weight: bold;
        }
       
        h2 {
            font-size: 4em;
            font-family: Arial, Helvetica, sans-serif;
            color: #242424;
        }
        .stApp {
            display: flex;
            justify-content: center;
            align-items: center;
            color: #121212;
            background-color: #ffffff;
        }
        .stAppHeader {
            color: #ffffff;
            background-color: #14151a;
        }
        .stMainBlockContainer {
            min-height: 100vh;
            display: flex;
            justify-content: center;
        }
        .stMainBlockContainer div {
            justify-content: center;
        }
        .stHorizontalBlock {
            width: 100%;
            justify-content: center;
            align-items: center;
            display: flex;
        }
        select {
            background-color: #e6e6e6;
            color: #fff;
            padding: 10px;
            border: none;
        }
        .stImageCaption {
            font-size: 20px;
        }
        p {
            color: #121212;
            transition: 0.3s ease-in-out;
        }
        .stButton > button {
            margin-top: 20px;
            border: 1px solid rgb(43, 43, 43);
            background-color: #ffffff;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: 0.3s ease-in-out;
        }
        .stButton > button:hover {
            box-shadow: 0 0 20px #0df0f8; 
            border: 1px solid rgb(15, 250, 160);
            background-color: #0fe97c; 
        }
        .stButton > button:focus {
            box-shadow: 0 0 20px #0df0f8; 
            border: 1px solid rgb(15, 250, 160) !important;
            background-color: #0fe97c; 
            outline: none;
        }
        .stButton > button:hover p {
            color: white;
        }
        .stColumn {
            min-width: 200px;
            max-width: 250px;
        }
        .stImage {
            overflow: hidden;
            width: 200px;
            box-sizing: border-box;
            color: black !important;
            border-radius: 10px;
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.623);
            transition: transform 0.3s ease, box-shadow 0.3s ease; 
        }

        .stImage:hover .stImage div div {
            opacity: 0;
        }

        .stImage div div {
            border-radius: 10px;
            font-size: 15px;
            color: white;
            font-weight: bold;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: 0.3s ease-in-out;
            position: absolute;
            background-color: #101010d8;
            width: 100%;
            height: 100%;
            opacity: 0;
        }
        
        .stImage div div:hover {
            opacity: 1;
        }
    </style>
    """,
    unsafe_allow_html=True
)
