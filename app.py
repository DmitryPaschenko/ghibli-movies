from flask import Flask, render_template
from movies.db import get_movies
from movies.updater import update_movie_list


app = Flask(__name__)


@app.route('/movies')
def movies():
    films = get_movies()
    if films is None:
        update_movie_list()
        films = get_movies()

    return render_template("movies.html", movies=films)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
