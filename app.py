from flask import Flask, request, render_template
import requests


app = Flask(__name__)
SWAPI_URL = 'https://swapi.py4e.com/api/'

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/swapi', methods=['GET', 'POST'])
def character_search(): 
    character = None
    error = None

    if request.method == 'POST':
        char_id = request.form.get('char_id')
        if not char_id:
            error = "Character ID is required. Please provide a valid ID."
            return render_template('swapi.html', character=None, error=error)

        try:
            response = requests.get(f"{SWAPI_URL}people/{char_id}/")
            response.raise_for_status()

            character = response.json()

            # Fetch homeworld name if available
            homeworld_url = character.get('homeworld')
            if homeworld_url:
                homeworld_response = requests.get(homeworld_url)
                character['homeworld_name'] = homeworld_response.json().get('name', 'Unknown')

            # Fetch film titles if available
            films = character.get('films', [])
            character['film_titles'] = []
            for film_url in films:
                film_response = requests.get(film_url)
                character['film_titles'].append(film_response.json().get('title', 'Unknown'))

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP Error: {http_err}")
            error = "Could not retrieve character. Please check the ID and try again."
        except Exception as e:
            print(f"Unexpected Error: {e}")
            error = "An unexpected error occurred. Please try again."

    return render_template('swapi.html', character=character, error=error)







if __name__ == '__main__':
    app.run(port=8000, debug=True)