from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

# Function to fetch movie poster from OMDB API
def fetch_poster(movie_title):
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey=b5b4bd76"
    try:
        data = requests.get(url)
        data.raise_for_status()  # Raise an error for bad responses
        data = data.json()
        if data['Response'] == 'True':
            return data['Poster']
        else:
            return "Poster not found"  # You can return a default poster URL here
    except requests.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "Poster not found"  # You can return a default poster URL here

# Load movie data and similarity data
movies = pickle.load(open("movieL.pkl", 'rb'))
simi = pickle.load(open("simi.pkl", 'rb'))
MovieL = movies['title'].values

# Function to recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []  # Return empty lists if the movie is not found

    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(simi[index])), reverse=True, key=lambda vector: vector[1])
    
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:9]:  
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies.iloc[i[0]].title))
    return recommend_movie, recommend_poster

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        movie_name = request.form.get("movie_name")
        movie_recommendations, movie_posters = recommend(movie_name)
        return render_template("index.html", movies=MovieL, recommendations=zip(movie_recommendations, movie_posters))
    
    # Render the template with an empty recommendations list on GET request
    return render_template("index.html", movies=MovieL, recommendations=[])

if __name__ == "__main__":
    app.run(debug=True)
