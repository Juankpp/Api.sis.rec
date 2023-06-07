import re
import csv
import json
import pandas as pd
import os
import sys
from datetime import datetime
import time

# include application directory in import path
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))

sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, '../src/main/python')))

# application imports
from app import create_app
from app import db
from config import Config
from modules.users.model import User
from modules.movies.model import Movie
from modules.genres.model import Genre
from modules.tags.model import Tag
from modules.ratings.model import Rating
from modules.artists.model import Artist
from modules.songs.model import Song
from modules.authors.model import Author
from modules.books.model import Book
from modules.book_ratings.model import BookRating
from modules.song_ratings.model import SongRating

import random
import string

def generate_password(length=10):
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    return password

# Generate a username and password

# init att and prep fixtures
app = create_app(Config)


def read_rating_dat(file_path):
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            split_line = line.strip().split("::")
            if len(split_line) == 4:
                
                # get existing user
                user = User.query.filter(
                    User.id == split_line[0]).first()

                # create new rating
                if user is None:
                    user = User(
                        id=split_line[0], 
                        username=f'user${split_line[0]}',
                        password = f'${generate_password()}')
                    db.session.add(user)

                movie = Movie.query.filter(
                    Movie.id == split_line[1]).first()

                if movie != None and user != None:
                    print("Rating", movie.id, split_line[2])
                    rating = Rating(
                        movie = movie,
                        user = user,
                        rating = split_line[2],
                        timestamp = datetime.fromtimestamp(int(split_line[3]))
                    )
                    db.session.add(rating)
    db.session.commit()

def read_tag_dat(file_path):
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            split_line = line.strip().split("::")
            if len(split_line) == 4:
                
                # get existing user
                user = User.query.filter(
                    User.id == split_line[0]).first()

                # create new tag
                if user is None:
                    user = User(
                        id=split_line[0], 
                        username=f'user${split_line[0]}',
                        password = f'${generate_password()}')
                    db.session.add(user)

                movie = Movie.query.filter(
                    Movie.id == split_line[1]).first()

                if movie != None and user != None:
                    print("Tag", split_line[2])

                    tag = Tag(
                        movie = movie,
                        user = user,
                        tag = split_line[2],
                        timestamp = datetime.fromtimestamp(int(split_line[3]))
                    )
                    db.session.add(tag)
    db.session.commit()

def read_movies_dat(file_path):
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            split_line = line.strip().split("::")
            if len(split_line) == 3:
                re_year = r"\((\d{4})\)"
                re_title = r"\s*\(\d{4}\)"
                result = re.search(re_year, split_line[1])
                year = ""
                title = ""
            if result:
                year = result.group(1)
            title = re.sub(re_title, "", split_line[1])
            
            genres = []
            for genre_data in split_line[2].split("|"):
                
                # get existing genre
                genre = Genre.query.filter(
                    Genre.genre == genre_data).first()

                # create new tag
                if genre is None:
                    genre = Genre(
                        genre=genre_data)
                    db.session.add(genre)
                genres.append(genre)
            print("Movie", split_line[0])
            movie = Movie(
                id=split_line[0],
                title=title.strip(),
                year=year,
                genres=genres)
            db.session.add(movie)
    db.session.commit()

def read_song_cvs(file_path):
    
    df_songs = pd.read_csv(file_path, encoding="utf-8")
    df_songs.dropna(inplace=True)
        
    for index, row in df_songs.iterrows():
        
        artist = Artist.query.filter(
                    Artist.name == row['artist']).first()
        
        if artist == None:
            artist = Artist(
                name=row['artist'])
            db.session.add(artist)        
        print("Song", row['song'])
        song = Song(
            song=row['song'],
            link=row['link'],
            text=row['text'],
            artist=artist)
        db.session.add(song)

    db.session.commit()


def read_book_json(file_path):

    with open(file_path, "r",  encoding="utf-8") as file:
        data = json.load(file)
        df_books = pd.DataFrame(data)
        df_books.dropna(inplace=True)

    for index, row in df_books.iterrows():
            
            for author_data in row['authors'].split('/'):
            
                author = Author.query.filter(
                            Author.name == author_data).first()
                
                if author == None:
                    author = Author(
                        name=author_data)
                    db.session.add(author)        
            
            book = Book.query.filter(
                            Book.id == row['bookID']).first()

            try:
                float_valor = float(row['average_rating'])
                if book == None:
                    
                    print("Book", row['bookID'])

                    book = Book(
                        id=row['bookID'],
                        title=row['title'],
                        average_rating=float_valor,
                        ratings_count=row['ratings_count'],
                        publisher=row['publisher'],
                        text_reviews_count=row['text_reviews_count'],
                        author=author)
                    db.session.add(book)
                
            except ValueError:
                pass                                    
            
                
    db.session.commit()







# wipe database and load new fixtures
with app.app_context():

    # Inicio del temporizador
    start_time = time.time()
    print("Starting")
    # clear and rebuild database tables
    db.drop_all()
    db.create_all()
    read_movies_dat("./files/movies.dat")
    read_tag_dat("./files/tags.dat")
    read_rating_dat("./files/ratings.dat")
    read_song_cvs("./files/songdata.csv")
    read_book_json("./files/books-json.json")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Tiempo transcurrido:", elapsed_time, "segundos")
    

