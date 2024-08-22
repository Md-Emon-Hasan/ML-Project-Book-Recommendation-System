'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date: 2021-Dec-18
'''

import pickle
import streamlit as st
import numpy as np

st.header('Book Recommender System Using Machine Learning')

# Load the models and data
model = pickle.load(open('C:/Users/emon1/OneDrive/Desktop/Book Recommendation System/models/model.pkl', 'rb'))
book_names = pickle.load(open('C:/Users/emon1/OneDrive/Desktop/Book Recommendation System/models/books_name.pkl', 'rb'))
final_rating = pickle.load(open('C:/Users/emon1/OneDrive/Desktop/Book Recommendation System/models/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('C:/Users/emon1/OneDrive/Desktop/Book Recommendation System/models/book_pivot.pkl', 'rb'))

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
        print(f"Book: {final_rating.iloc[idx]['title']}, URL: {url}")  # Print the URL for debugging

    return poster_url

def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)
    
    return books_list, poster_url

# Streamlit interface
selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    book_names
)

if st.button('Show Recommendation'):
    recommended_books, poster_url = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])
    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])
