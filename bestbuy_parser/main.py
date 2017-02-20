import requests
import json, urllib
import csv
import time
from random import randint

def dl_movies():
    f = open("movies.csv", 'w+')
    writer = csv.writer(f)
    writer.writerow( ('movieId', 'title', 'genres') )

    page = 1
    try:
        for i in range(1, 90):

            print "page: " + str(i)
            url = "https://api.bestbuy.com/v1/products(type=Movie)?format=json&pageSize=100&page=" + str(i) + "&apiKey=p59525shzt55n2d58ujzpszs"
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            for product in data['products']:
                if product['genre']:
                    writer.writerow((product['sku'], product['name'].encode('utf-8'), product['genre'].encode('utf-8')))
            time.sleep(5)


    finally:
        f.close()


def generate_ratings():
    f = open("movies.csv")
    r = open("ratings.csv", 'w+')
    writer = csv.writer(r)
    writer.writerow( ('userId','movieId','rating','timestamp') )
    lines = f.readlines()
    for i in range(1,500):
        for j in range(1,200):
            movie = randint(1, 7354)
            movieId = lines[movie].split(",")[0]
            rating = (randint(0,10) + randint(0,10))/4.0
            timestamp = "1343732032"
            writer.writerow((i,movieId,rating,timestamp))
    f.close()
    r.close()


def generate_tag():
    a = open("adj.txt")
    f = open("movies.csv")
    r = open("tags.csv", 'w+')

    writer = csv.writer(r)
    writer.writerow( ('userId','movieId','tag','timestamp') )
    movies = f.readlines()
    adjs = a.readlines()
    for i in range(1,1300):
        movie = randint(1, 7354)
        movieId = movies[movie].split(",")[0]
        adj = adjs[randint(0,49)].strip()
        user = randint(1,500)
        timestamp = "1343732032"
        writer.writerow((user,movieId,adj,timestamp))
    f.close()
    r.close()

generate_tag()