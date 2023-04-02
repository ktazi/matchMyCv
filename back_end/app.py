import json
import psycopg2
from flask import Flask, jsonify, request
from  flask_uploads import UploadSet, configure_uploads, ALL
from flask_cors import CORS
import os.path
from pathlib import Path
from pdf2image import convert_from_path
import os
import pytesseract
import re
from nltk.corpus import stopwords
import spacy
import threading
from nltk.corpus import stopwords


DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

Cors = CORS(app)

CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)

conn = psycopg2.connect(
        host="localhost",
        database="name_db",
        user='user_db',
        password='password_db')


cur = conn.cursor()
nlp = spacy.load('fr_core_news_md')

"""

MISC FONCTION SITE WEB    

"""

def new_annonce(name, employer, obl, opt, pref):
    global conn, cur
    cur.execute('insert into announce (name_annonce, name_employer, pourc_ob, pourc_opt, pourc_pref) '
            'VALUES (%s, %s, %s, %s, %s)',
            (name,
             employer, 
             obl,
             opt,
             pref)
            )
    conn.commit()

def get_annonce():
    global conn, cur
    cur.execute("select * from announce")
    return cur.fetchall()

def get_last_skill_id():
    global conn, cur
    cur.execute("select id_skill From skills order by id_skill desc limit 1")
    return cur.fetchall()[0][0]

def get_id_skills_annonce(id_annonce):
    global conn, cur
    cur.execute("select id_skill from skills where id_annonce = " + str(id_annonce))
    return [i[0]for i in cur.fetchall()]


def add_skill(name, id_annonce, obl, opt, pref):
    global conn, cur
    if check_annonce(id_annonce) :
        cur.execute('insert into skills (name_skill, id_annonce, type_ob, type_opt, type_pref) values (%s, %s, %s, %s, %s);', 
                    (name,id_annonce,obl, opt, pref))
        conn.commit()

def check_annonce(numb_annonce):
    cur.execute("select * from announce where id_annonce ="+str(numb_annonce)+";" )
    return len(cur.fetchall())>0

def get_last_annonce_id():
    global conn, cur
    cur.execute("select id_annonce From announce order by id_annonce desc limit 1")
    return cur.fetchall()[0][0]

def get_annonce_and_skills(id_annonce):
    global conn, cur
    if check_annonce(id_annonce) :
        cur.execute("select * from announce where id_annonce ="+str(id_annonce)+";" )
        annonce = cur.fetchall()
        cur.execute("select * from skills where id_annonce ="+str(id_annonce)+";" )
        skills = cur.fetchall()
        rep = {"annonce":annonce, "skills":skills}
        return rep

def get_last_cv_id():
    global conn, cur
    cur.execute("select id_cv from cv order by id_cv desc limit 1")
    return cur.fetchall()[0][0]


def modif_scores(score,id_annonce , obl, opt):
    global conn, cur
    if obl :
        cur.execute("update announce set pourc_ob = '"+ str(score) +"' where id_annonce="+str(id_annonce)+";")
        conn.commit()
    elif opt :
        cur.execute("update announce set pourc_opt = '"+ str(score) +"' where id_annonce="+str(id_annonce)+";")
        conn.commit()
    else :
        cur.execute("update announce set pourc_pref = '"+ str(score) +"' where id_annonce="+str(id_annonce)+";")
        conn.commit()



def get_skills_cv(id_cv):
    global conn, cur
    cur.execute("""
    select cv.id_cv, skills.id_skill, type_ob, type_opt, type_pref, name_skill, checked from cv 
    left join
    (select * from note) as notes
    on notes.id_cv = cv.id_cv
    left join
    (select * from skills) as skills
    on notes.id_skill = skills.id_skill
    where cv.id_cv = """ + str(id_cv)+";")
    return cur.fetchall()

def compute_score(id_cv):
    global conn, cur
    cur.execute("""
    select sum(score) from 
    (
    select 
    case when checked then
        case when type_opt then pourc_opt
            when type_ob then pourc_ob
            else pourc_pref
        end 
        else 0 
        end as score
        
        from note
    left join
    (
        select * from announce

    ) as annonce
    on annonce.id_annonce = note.id_annonce

    left join
    (
        select * from skills
    )
    as skills
    on skills.id_skill = note.id_skill
    where id_cv ="""+ str(id_cv)+""")
    as cvscore;
    """)
    return cur.fetchall()[0][0]

def compute_score_estim(id_cv):
    cur.execute("select parsed from cv where id_cv ="+str(id_cv))
    parsed = cur.fetchall()[0][0]
    if parsed : 
        cur.execute("select cv_name from cv where id_cv ="+str(id_cv))
        cv_name = cur.fetchall()[0][0]
        cur.execute("""select id_cv, id_skill,
        case when type_opt then pourc_opt
                    when type_ob then pourc_ob
                    else pourc_pref
                end
        from cv
        left join announce on announce.id_annonce=cv.id_annonce
        left join skills on skills.id_annonce = cv.id_annonce
        where id_cv = """+str(id_cv))
        skills = cur.fetchall()
        f = open('config.json')
        config = json.load(f)
        path_txt = config["path_txt_server"]+"/"+cv_name[:-3]+"txt"
        matched = match_cv(id_cv, path_txt)
        score = 0
        for i in matched.keys() :
            for skill in skills :
                if skill[1]==i:
                    if dict(matched)[i]:
                        score += skill[2]
        return score
    return 0

"""

PARSING

"""
def from_pdf_to_png(path):
    images = convert_from_path(path)
    return images

# Tessaract
def from_png_to_text(img):
    """Convert png to text"""
    text = pytesseract.image_to_string(img[0])
    return text

def cv_preprocessing(string,  path_txt):
    # Remove all special characters but keep spaces and accents
    cleaned_text = re.sub(r'[^a-zA-Z0-9À-ÿ\s]+', ' ', " ".join(string.replace("\n", " ").split()).lower())  

    # Remove stopwords
    pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('french')) + r')\b\s*')
    sw_text = pattern.sub('', cleaned_text)

    # lematization
    nlp = spacy.load('fr_core_news_md')
    lemmatized_text = ' '.join([token.lemma_ for token in nlp(sw_text)])
    file_obj = open(path_txt, "w+", encoding="utf-8")
    file_obj.write(lemmatized_text)
    file_obj.close()

def parsing(path_pdf, path_txt, id_cv):
    """Parse pdf to text"""
    file = Path(path_txt)
    if not file.exists():
        image = from_pdf_to_png(path_pdf)
        text = from_png_to_text(image)
        cv_preprocessing(text, path_txt)
    cur.execute("update cv set parsed=true where id_cv = "+ str(id_cv) +";")
    conn.commit() 

def parse_cv(name_pdf, id_cv):
    f = open('config.json')
    config = json.load(f)
    path_txt = config["path_txt_server"]+"/"+name_pdf[:-3]+"txt"
    path_pdf = config["path_pdf_server"]+"/"+name_pdf
    t1 = threading.Thread(target=parsing, args=(path_pdf,path_txt, id_cv, ))
    t1.start()

"""

MATCHING

"""

def match_cv(id_cv, path_txt):
    cur.execute("""
        select name_skill, id_skill  from cv
        left join 
        (
	        select * from skills
        ) as skills
        on skills.id_annonce = cv.id_annonce
        where id_cv = """+str(id_cv)+";")
    tableau_competences = cur.fetchall()
    return matching_f(tableau_competences, path_txt)

def offer_preprocess(offer):
    """Preprocess a string"""
    pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('french')) + r')\b\s*')
    
    lema_comp = []
    for competence in offer:
        lema_comp.append((' '.join([token.lemma_ for token in nlp(pattern.sub('', competence[0]))]), competence[1]))

    return lema_comp


def matching_f(offer, lem_resume_path):
    """Match a list of competences with a lemmatized resume"""
    # read the lemmatized resume
    with open(lem_resume_path, 'r', encoding='utf-8') as file:
        lem_resume = file.read()

    list_comp = offer_preprocess(offer)

    comp_dict = {}
    # find all occurences of a substring in a string
    for competence in list_comp:
        if competence[0] in lem_resume:
            comp_dict[competence[1]] = True
        else:
            comp_dict[competence[1]] = False
            
    return comp_dict

"""

ROUTES

"""

#Ajout de nouvelle annonce et selection des annonces
@app.route('/annonce', methods=['GET', 'POST'])
def annonce():
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        #ajout annonce
        new_annonce(post_data['name'], post_data['employer'],  post_data['obl'],  post_data['opt'], post_data['pref'])
        id_annonce = get_last_annonce_id()
        #ajout skills
        for skill_ob in post_data['skill_ob'] :
            add_skill(skill_ob, id_annonce, True, False, False)
        for skill_opt in post_data['skill_opt'] :
            add_skill(skill_opt, id_annonce, False, True, False)
        for skill_pref in post_data['skill_pref'] :
            add_skill(skill_pref, id_annonce, False, False, True)
        resp = jsonify({"message":"successfully added"})
        return resp
    resp = jsonify(get_annonce())
    return resp

#Information sur une annonce
@app.route('/info', methods=["GET"])
def annonce_info():
    id_annonce = request.args.get("id_annonce")
    annonce = get_annonce_and_skills(id_annonce)
    return jsonify(annonce)

#modification nom annonce
@app.route('/modifAnnonceNom', methods=['POST'])
def modify_name_annonce():
    post_data = request.get_json()
    id_annonce = post_data["id_annonce"]
    nom = post_data["nom_annonce"]
    cur.execute("update announce set name_annonce = '"+ nom +"' where id_annonce="+id_annonce+";")
    conn.commit()
    return jsonify({"modif":"OK"})


#modification nom employeur dans annonce
@app.route('/modifAnnonceEmployeur', methods=['POST'])
def modify_name_employeur():
    post_data = request.get_json()
    id_annonce = post_data["id_annonce"]
    nom_employeur = post_data["nom_employeur"]
    cur.execute("update announce set name_employer = '"+ nom_employeur +"' where id_annonce="+id_annonce+";")
    conn.commit()
    return jsonify({"modif":"OK"})

#modif score dans annonce 
@app.route('/modifAnnonceScore', methods=["POST"])
def modify_score_annonce():
    post_data = request.get_json()
    score = post_data["score"]
    id_annonce = post_data["id_annonce"]
    obl = post_data["obl"]
    opt = post_data["opt"]
    modif_scores(score,id_annonce , obl, opt)
    return jsonify({"modif":"OK"})

#supression skill dans annonce
@app.route('/suppAnnonceSkill', methods=['POST'])
def supp_skill():
    post_data = request.get_json()
    id_skill = post_data["id_skill"]
    cur.execute("delete from note where id_skill="+str(id_skill) +";")
    conn.commit()
    cur.execute("delete from skills where id_skill="+str(id_skill) +";")
    conn.commit()
    return jsonify({"supp":"OK"})

#ajout skill dans annonce
@app.route('/addAnnonceSkill', methods=["POST"])
def add_skill_annonce():
    post_data = request.get_json()
    name = post_data["name"]
    id_annonce = post_data["id_annonce"]
    obl = post_data["obl"]
    opt = post_data["opt"] 
    pref = post_data["pref"] 
    add_skill(name,id_annonce, obl, opt, pref)
    id_skill = get_last_skill_id()
    print(id_skill)
    cur.execute("select id_cv from cv where id_annonce="+str(id_annonce))
    id_cvs = [i[0] for i in cur.fetchall()]
    for id_cv in id_cvs :
        print(id_cv)
        cur.execute('INSERT INTO note (id_cv, id_annonce, id_skill) VALUES (%s, %s, %s)', (id_cv, id_annonce, id_skill))
        conn.commit()
    return jsonify({"id_skill":id_skill})


#Upload des CV
@app.route('/upload', methods=["POST"])
def upload():
    post_data = request.get_json()
    id_annonce = post_data["id_annonce"]
    id_skills = get_id_skills_annonce(id_annonce)
    for filename in post_data["cv_names"]:
        cur.execute('INSERT INTO cv (cv_name, id_annonce) VALUES (%s, %s)', (filename, id_annonce))
        conn.commit()
        id_cv = get_last_cv_id()
        for skill in id_skills :
            cur.execute('INSERT INTO note (id_cv, id_annonce, id_skill) VALUES (%s, %s, %s)', (id_cv, id_annonce, skill))
            conn.commit()
        parse_cv(filename, id_cv)    
    return jsonify({"message":"successfully added"})

#recuperation des CV + infos par annonce
@app.route('/cv', methods=["GET"])
def get_cv():
    print(request.args.get("id_annonce"))
    id_annonce = request.args.get("id_annonce")
    if check_annonce(id_annonce) :
        cur.execute("select * from cv where id_annonce="+str(id_annonce)+ " order by score desc ,score_suggere desc ;" )
        return jsonify(cur.fetchall())
    return jsonify({"message" : "NOT OK"})

#recuperation des donnees d'un cv
@app.route('/cvdata', methods=["GET"])
def get_cv_score():
    print(request.args.get("id_cv"))
    id_cv= request.args.get("id_cv")
    cur.execute("select * from cv where id_cv="+str(id_cv)+ ";" )
    return jsonify(cur.fetchall())

#recuperation des infos sur un cv
@app.route('/infoCV', methods=["GET"])
def get_info_cv():
    id_cv = request.args.get("id_cv")
    return jsonify(get_skills_cv(id_cv))

#changement statut check d'un skill d'un CV
@app.route('/checkCV', methods=["POST"])
def change_check():
    post_data = request.get_json()
    id_cv = post_data["id_cv"]
    id_skill = post_data["id_skill"]
    #updating check status
    cur.execute("update note set checked= not checked where id_cv="+str(id_cv)+" and id_skill="+str(id_skill)+";")
    conn.commit()
    #updating score of CV
    score = compute_score(id_cv)
    cur.execute("update cv set score="+str(score) +" where id_cv="+str(id_cv)+";")
    return jsonify({"message" : "OK"})

#avoir les recommandations par skill pour cv
@app.route('/getRecommandation', methods=["GET"])
def reco_skill():
    f = open('config.json')
    config = json.load(f)
    id_cv = request.args.get("id_cv")
    path_txt = config["path_txt_server"]+"/"+request.args.get("pdf_name")[:-3]+"txt"
    print(path_txt)
    return jsonify(match_cv(id_cv, path_txt))

#changer le statut d'un CV de note
@app.route('/isnote', methods=["GET"])
def changer_not_statut():
    id_cv = request.args.get("id_cv")
    cur.execute("update cv set is_note = true where id_cv="+str(id_cv)+";")
    conn.commit()
    return jsonify("OK")

#calculer les scores d'estimation des CV
@app.route('/estimNoteAnnonce', methods=["POST"])
def estim_note():
    post_data = request.get_json()
    id_annonce = post_data["id_annonce"]
    cur.execute("select id_cv from cv where id_annonce="+str(id_annonce)+" and not is_note")
    id_cvs = [i[0] for i in cur.fetchall()]
    for id_cv in id_cvs :
        score = compute_score_estim(id_cv)
        cur.execute("update cv set score_suggere="+str(score)+" where id_cv="+str(id_cv))
        conn.commit()
    return jsonify("OK")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)