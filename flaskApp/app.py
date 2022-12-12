from flask import Flask, render_template, request, redirect, url_for
from neo4j import GraphDatabase
from urllib.request import urlopen
import json

app = Flask(__name__, static_url_path='', static_folder='static')

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "CS6400"))

api_key = 'b996cb6bd7c36029c4e2ee24a467d91b'

resposne = [{'n2': {'overview': "Teenagers in a small town are dropping like flies, apparently in the grip of mass hysteria causing their suicides. A cop's daughter, Nancy Thompson, traces the cause to child molester Fred Krueger, who was burned alive by angry parents many years before. Krueger has now come back in the dreams of his killers' children, claiming their lives as his revenge. Nancy and her boyfriend, Glen, must devise a plan to lure the monster out of the realm of nightmares and into the real world...", 'movieId': '377', 'title': 'A Nightmare on Elm Street'}, 'count': 1}, {'n2': {'overview': "Two Los Angeles homicide detectives are dispatched to a northern town where the sun doesn't set to investigate the methodical murder of a local teen.", 'movieId': '320', 'title': 'Insomnia'}, 'count': 1}, {'n2': {'overview': "Selfish yuppie Charlie Babbitt's father left a fortune to his savant brother Raymond and a pittance to Charlie; they travel cross-country.", 'movieId': '380', 'title': 'Rain Man'}, 'count': 1}, {'n2': {'overview': 'In 25 AD,Judah Ben-Hur, a Jew in ancient Judea, opposes the occupying Roman empire.  Falsely accused by a Roman childhood friend-turned-overlord of trying to kill the Roman governor, he is put into slavery and his mother and sister are taken away as prisoners.  Three years later and freed by a grateful Roman galley commander whom he has rescued from drowning, he becomes an expert charioteer for Rome, all the while plotting to return to Judea, find and rescue his family, and avenge himself on his former friend.  All the while, the form and work of Jesus move in the background of his life...', 'movieId': '665', 'title': 'Ben-Hur'}, 'count': 1}, {'n2': {'overview': 'After a defecting Russian general reveals a plot to assassinate foreign spies, James Bond is assigned a secret mission to dispatch the new head of the KGB to prevent an escalation of tensions between the Soviet Union and the West.', 'movieId': '708', 'title': 'The Living Daylights'}, 'count': 1}, {'n2': {'overview': 'Cars fly, trees fight back, and a mysterious house-elf comes to warn Harry Potter at the start of his second year at Hogwarts. Adventure and danger await when bloody writing on a wall announces: The Chamber Of Secrets Has Been Opened. To save Hogwarts will require all of Harry, Ron and Hermione’s magical abilities and courage.', 'movieId': '672', 'title': 'Harry Potter and the Chamber of Secrets'}, 'count': 1}, {'n2': {'overview': 'A shy woman, endowed with the speed, reflexes, and senses of a cat, walks a thin line between criminal and hero, even as a detective doggedly pursues her, fascinated by both of her personas', 'movieId': '314', 'title': 'Catwoman'}, 'count': 1}, {'n2': {'overview': "The lifelong friendship between Rafe McCawley and Danny Walker is put to the ultimate test when the two ace fighter pilots become entangled in a love triangle with beautiful Naval nurse Evelyn Johnson. But the rivalry between the friends-turned-foes is immediately put on hold when they find themselves at the center of Japan's devastating attack on Pearl Harbor on Dec. 7, 1941.", 'movieId': '676', 'title': 'Pearl Harbor'}, 'count': 1}, {'n2': {'overview': "Andy moves to New York to work in the fashion industry. Her boss is extremely demanding, cruel and won't let her succeed if she doesn't fit into the high class elegant look of their magazine.", 'movieId': '350', 'title': 'The Devil Wears Prada'}, 'count': 1}, {'n2': {'overview': "Harry Potter has lived under the stairs at his aunt and uncle's house his whole life. But on his 11th birthday, he learns he's a powerful wizard—with a place waiting for him at the Hogwarts School of Witchcraft and Wizardry. As he learns to harness his newfound powers with the help of the school's kindly headmaster, Harry uncovers the truth about his parents' deaths—and about the villain who's to blame.", 'movieId': '671', 'title': "Harry Potter and the Philosopher's Stone"}, 'count': 1}]

cdn_prefix = "https://image.tmdb.org/t/p/original"

# for res in resposne:
#     print(res.get('n2').get('overview'))
#     print(res.get('n2').get('title'))
# movie = "oops"
@app.route('/', methods=['POST', 'GET'])
def index():
    # if request.method == 'POST':
    #     movie = request.form.get('Name')
    #     print(movie)
    #     return redirect(url_for('recomendation', movie=movie))
    return render_template('index.html', messages=messages)

@app.route('/recomendation', methods = ['POST', 'GET'])
def recomendation():
    name = request.form.get('Name')
    print(name)
    
    movie_ids = []
    poster_urls = []
    
    # movies = []
    
    with driver.session() as session:
            
            recommendations = session.run("MATCH (n)-[r]->(n2) WHERE n.title = $title RETURN n2, COUNT(r) AS count ORDER BY COUNT(r) DESC LIMIT 10", title=name)
            
            movies = recommendations.data()
            
            
            for movie in movies:
                
                movie_ids.append(movie.get('n2').get('movieId'))
                
            
    for movie_id in movie_ids:
                
        # target_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, api_key)
        target_url = "https://api.themoviedb.org/3/movie/{}/images?api_key={}".format(movie_id, api_key)
        
        # response = requests.get(target_url)
        with urlopen(target_url) as response:
            
            response_dict = json.loads(response.read())
            
            poster = response_dict['posters']
            
            if len(poster) > 0:
                
                poster_path = poster[0]['file_path']
                
                poster_path = cdn_prefix + poster_path
                
                poster_urls.append(poster_path)
                
    
    # add the poster urls to the movies list
    
    for i in range(len(movies)):
        
        movies[i]['poster_url'] = poster_urls[i]
            
            # movies.append(data)
    
    print(movies)      
                    

            
    # movies = [{'n2': {'overview': "Teenagers in a small town are dropping like flies, apparently in the grip of mass hysteria causing their suicides. A cop's daughter, Nancy Thompson, traces the cause to child molester Fred Krueger, who was burned alive by angry parents many years before. Krueger has now come back in the dreams of his killers' children, claiming their lives as his revenge. Nancy and her boyfriend, Glen, must devise a plan to lure the monster out of the realm of nightmares and into the real world...", 'movieId': '377', 'title': 'A Nightmare on Elm Street'}, 'count': 1}, {'n2': {'overview': "Two Los Angeles homicide detectives are dispatched to a northern town where the sun doesn't set to investigate the methodical murder of a local teen.", 'movieId': '320', 'title': 'Insomnia'}, 'count': 1}, {'n2': {'overview': "Selfish yuppie Charlie Babbitt's father left a fortune to his savant brother Raymond and a pittance to Charlie; they travel cross-country.", 'movieId': '380', 'title': 'Rain Man'}, 'count': 1}, {'n2': {'overview': 'In 25 AD,Judah Ben-Hur, a Jew in ancient Judea, opposes the occupying Roman empire.  Falsely accused by a Roman childhood friend-turned-overlord of trying to kill the Roman governor, he is put into slavery and his mother and sister are taken away as prisoners.  Three years later and freed by a grateful Roman galley commander whom he has rescued from drowning, he becomes an expert charioteer for Rome, all the while plotting to return to Judea, find and rescue his family, and avenge himself on his former friend.  All the while, the form and work of Jesus move in the background of his life...', 'movieId': '665', 'title': 'Ben-Hur'}, 'count': 1}, {'n2': {'overview': 'After a defecting Russian general reveals a plot to assassinate foreign spies, James Bond is assigned a secret mission to dispatch the new head of the KGB to prevent an escalation of tensions between the Soviet Union and the West.', 'movieId': '708', 'title': 'The Living Daylights'}, 'count': 1}, {'n2': {'overview': 'Cars fly, trees fight back, and a mysterious house-elf comes to warn Harry Potter at the start of his second year at Hogwarts. Adventure and danger await when bloody writing on a wall announces: The Chamber Of Secrets Has Been Opened. To save Hogwarts will require all of Harry, Ron and Hermione’s magical abilities and courage.', 'movieId': '672', 'title': 'Harry Potter and the Chamber of Secrets'}, 'count': 1}, {'n2': {'overview': 'A shy woman, endowed with the speed, reflexes, and senses of a cat, walks a thin line between criminal and hero, even as a detective doggedly pursues her, fascinated by both of her personas', 'movieId': '314', 'title': 'Catwoman'}, 'count': 1}, {'n2': {'overview': "The lifelong friendship between Rafe McCawley and Danny Walker is put to the ultimate test when the two ace fighter pilots become entangled in a love triangle with beautiful Naval nurse Evelyn Johnson. But the rivalry between the friends-turned-foes is immediately put on hold when they find themselves at the center of Japan's devastating attack on Pearl Harbor on Dec. 7, 1941.", 'movieId': '676', 'title': 'Pearl Harbor'}, 'count': 1}, {'n2': {'overview': "Andy moves to New York to work in the fashion industry. Her boss is extremely demanding, cruel and won't let her succeed if she doesn't fit into the high class elegant look of their magazine.", 'movieId': '350', 'title': 'The Devil Wears Prada'}, 'count': 1}, {'n2': {'overview': "Harry Potter has lived under the stairs at his aunt and uncle's house his whole life. But on his 11th birthday, he learns he's a powerful wizard—with a place waiting for him at the Hogwarts School of Witchcraft and Wizardry. As he learns to harness his newfound powers with the help of the school's kindly headmaster, Harry uncovers the truth about his parents' deaths—and about the villain who's to blame.", 'movieId': '671', 'title': "Harry Potter and the Philosopher's Stone"}, 'count': 1}]
            # print(movies)
    return render_template('recomendation.html', movies=movies, name=name)