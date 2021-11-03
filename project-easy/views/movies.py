from flask import request
from flask_restx import Resource, Namespace

from models import Movie, MovieSchema
from setup_db import db

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        t = db.session.query(Movie)
        if director is not None:
            t = t.filter(Movie.director_id == director)
        if genre is not None:
            t = t.filter(Movie.genre_id == genre)
        if year is not None:
            t = t.filter(Movie.year == year)
        all_movies = t.all()
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    def post(self):
        req_json = request.json
        ent = Movie(**req_json)

        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"/movies/{ent.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid):
        b = db.session.query(Movie).get(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        movie = db.session.query(Movie).get(bid)
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, bid):
        movie = db.session.query(Movie).get(bid)

        db.session.delete(movie)
        db.session.commit()
        return "", 204
