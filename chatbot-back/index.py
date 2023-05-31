from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
from flask_mysqldb import MySQL




app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'user'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

bot = ChatBot("chatbot", read_only=False,
    logic_adapters=[
    
        {
            "import_path":"chatterbot.logic.BestMatch",
            "default_response":"désolé , j'ai pas bien compris",
            "maximum_similarity_threshold":0.9
        }

        ])



trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
     "chatterbot.corpus.french",
     "chatterbot.corpus.french.greetings",
     "chatterbot.corpus.french.conversations"
    )
trainer = ListTrainer(bot)
trainer.train ( [
                "salut",
                "salut toi,comment je peux t'aider ?",
                "bonjour",
                "bonjour,comment je peux t'aider ?",
                "bonsoir",
                "bonsoir,comment je peux t'aider ?",
                "en forme ?",
                "oui ça va ,comment je peux t'aider ?",
                "comment va tu ?",
                "ça va bien ,comment je peux t'aider ?",
                "ça va ",
                "Je vais bien merci,comment je peux t'aider ?"           
 ])

trainer.train ( [
    "merci beaucoup",
    "De rien ",
    "au revoir",
    "à bientot",
    "bye",
    "Bye",
    "à tout à l'heure",
    "à bientot"        
 ])
trainer.train ( [
   "quel est le principe du football?",
   "Deux équipes de 11 joueurs dont un gardien de but (plus trois remplaçants) s'affrontent autour d'un ballon rond le plus souvent en cuir. Les matchs ne peuvent se disputer à moins de 7 joueurs par équipe (gardien compris).Les joueurs ne peuvent toucher le ballon ni avec les mains ni avec les bras.",        
   "comment jouer le football?",
   "Deux équipes de 11 joueurs dont un gardien de but (plus trois remplaçants) s'affrontent autour d'un ballon rond le plus souvent en cuir. Les matchs ne peuvent se disputer à moins de 7 joueurs par équipe (gardien compris).Les joueurs ne peuvent toucher le ballon ni avec les mains ni avec les bras.",
   "quelles sont les règles du football? ",
   "Il ya 17 lois principaux dans le football.Vous pouvez visitez ce site pour plusieurs explications https://fr.wikipedia.org/wiki/Lois_du_jeu ",     
   "la premier league 2018-2019 ",
   "Premier League 2018/2019 / statut: Completed / Nombre de club: 20 / Nombre totale des matches : 380 / Nombre totale des semaines jouées : 38 ",
   "quelles sont les équipes du premier league 2018-2019",
   "Arsenal FC / Tottenham Hotspur FC / Manchester City FC / Leicester City FC / Crystal Palace FC / Everton FC / Burnley FC / Southampton FC / AFC Bournemouth / Manchester United FC / Liverpool FC / Chelsea FC / West Ham United FC / Watford FC / Newcastle United FC / Cardiff City FC / Fulham FC / Brighton & Hove Albion FC / Huddersfield Town FC / Wolverhampton Wanderers FC",
   "quelles sont les statiques du premier league 2018-2019 ",
   "Premier League 2018/2019 / statut: Completed / Nombre de club: 20 / Nombre totale des matches : 380 / Nombre totale des semaines jouées : 38 ",
   " les statiques du premier league 2018-2019 ",
   "Premier League 2018/2019 / statut: Completed / Nombre de club: 20 / Nombre totale des matches : 380 / Nombre totale des semaines jouées : 38 ",
   "quel est le champion du premier league 2018-2019",
   "Manchester City",
   "le champion du premier league 2018-2019",
   "Manchester City",
   "quels sont les matches de la premiere semaine du premier league 2018-2019",
   "Manchester United vs Leicester City	2	1	Old Trafford (Manchester) | Newcastle United vs Tottenham Hotspur	1	2	St. James' Park (Newcastle upon Tyne) | AFC Bournemouth vs Cardiff City	2	0	Vitality Stadium (Bournemouth- Dorset)  | Fulham vs Crystal Palace	0	2	Craven Cottage (London) | Huddersfield Town vs Chelsea	0	3	John Smith's Stadium (Huddersfield- West Yorkshire) | Watford vs Brighton & Hove Albion	2	0	Vicarage Road (Watford) | Wolverhampton Wanderers vs Everton	2	2	Molineux Stadium (Wolverhampton- West Midlands) | Liverpool vs West Ham United	4	0	Anfield (Liverpool) | Southampton vs Burnley	0	0	St. Mary's Stadium (Southampton- Hampshire) | Arsenal vs Manchester City	0	2	Emirates Stadium (London)",
   "la premiere semaine du premier league 2018-2019",
   "Manchester United vs Leicester City	2	1	Old Trafford (Manchester) | Newcastle United vs Tottenham Hotspur	1	2	St. James' Park (Newcastle upon Tyne) | AFC Bournemouth vs Cardiff City	2	0	Vitality Stadium (Bournemouth- Dorset)  | Fulham vs Crystal Palace	0	2	Craven Cottage (London) | Huddersfield Town vs Chelsea	0	3	John Smith's Stadium (Huddersfield- West Yorkshire) | Watford vs Brighton & Hove Albion	2	0	Vicarage Road (Watford) | Wolverhampton Wanderers vs Everton	2	2	Molineux Stadium (Wolverhampton- West Midlands) | Liverpool vs West Ham United	4	0	Anfield (Liverpool) | Southampton vs Burnley	0	0	St. Mary's Stadium (Southampton- Hampshire) | Arsenal vs Manchester City	0	2	Emirates Stadium (London)"
 
 
 
 ])


@app.route('/signup', methods=['POST'])
def signup():
    # Parse the JSON request body
    data = request.get_json()
    
    # Extract the user information from the JSON object
    userName = data['userName']
    email = data['email']
    password = data['password']
    numeroTel = data['numeroTel']
    
    # Add the user to the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE userName = %s", (userName,))
    user = cur.fetchone()
    if user is None:
        cur.execute("INSERT INTO user (userName, email, password, numeroTel) VALUES (%s, %s, %s, %s)", (userName, email, password, numeroTel))
        mysql.connection.commit()
        cur.close()
        # Return a JSON response indicating success
        return jsonify({'success': True})
    else:
        # Return a JSON response indicating failure
        return jsonify({'success': False, 'message': 'Utilisateur existe deja'})

    

@app.route('/signin', methods=['POST'])
def signin():
    # Parse the JSON request body
    data = request.get_json()
    
    # Extract the username and password from the JSON object
    userName = data['userName']
    password = data['password']
    
    # Look up the user in the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE userName = %s AND password = %s", (userName, password))
    user = cur.fetchone()
    cur.close()
    
    if user is None:
        # Return a JSON response indicating failure
        return jsonify({'success': False, 'message': 'Invalid username or password'})
    else:
        # Return a JSON response indicating success
        return jsonify({'success': True})


    
@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')
    return str(bot.get_response(userText))    
if __name__ == "__main__":
    app.run(debug=True)

