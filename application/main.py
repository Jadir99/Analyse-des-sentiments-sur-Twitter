# test
import analyse_sentiment as an 
from flask import Flask ,render_template,request
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/puthushtag')
def gethashtag():
    return render_template('analyse.html')

@app.route('/result',methods=["POST","GET"])
def insert_url():
    # this is for geting the extract the name taht i will put in the url for searching
    
    path=an.login(request.form['hashtag'])
    statistiques=an.clean_data(path)

    return render_template('result.html', statistiques=statistiques)


# // voir la page pour insere le name d'utilisateur
@app.route('/searchByName')
def byuserame():
    return render_template('byname.html',all="jadir")

@app.route('/result_byname',methods=["POST","GET"])
def insert_name():
    # this is for geting the extract the name taht i will put in the url for searching
    
    path=an.search_byname(request.form['username'])
    statistiques=an.clean_data(path)

    return render_template('result.html', statistiques=statistiques)
    # return render_template('result.html',liste=statistiques)



if __name__ == '__main__':
    app.run(debug=True,port=5000,use_reloader=False)