from flask import Flask
from flask import render_template
from flask import request
import pickle
import numpy as np

app = Flask(__name__)

# Load the models and data
model = pickle.load(open('models/model.pkl', 'rb'))
book_names = pickle.load(open('models/books_name.pkl', 'rb'))
final_rating = pickle.load(open('models/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('models/book_pivot.pkl', 'rb'))

# Fallback image URL if a valid one isn't found
fallback_image_url = 'https://via.placeholder.com/150'

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        if 'img_url' in final_rating.columns:
            url = final_rating.iloc[idx].get('img_url', fallback_image_url)  # Get image URL or use fallback
        else:
            url = fallback_image_url  # Fallback URL if 'image_url' column doesn't exist
        poster_url.append(url)

    return poster_url

def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=8)

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)
    
    return books_list, poster_url

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    posters = []
    selected_book = None  # Initialize selected_book

    if request.method == 'POST':
        selected_book = request.form.get('book_name')
        recommendations, posters = recommend_book(selected_book)

    # Pass the zip function to the template
    return render_template('index.html', book_names=book_names, recommendations=recommendations, posters=posters, zip=zip, selected_book=selected_book)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
