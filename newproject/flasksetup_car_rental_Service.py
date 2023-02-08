from flask import Flask, render_template,url_for, request
import os
from carrentalservice import connectMongo


app = Flask(__name__)


picFolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picFolder


posts = [{'author': 'kartikeya','title':'Student'},{'project':'Car rental service','University':'SRH'}]



@app.route("/", methods=["POST"])
@app.route("/home")
def getvalue():
    lst1 = []
    usenum = request.form["UseCase"]
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'pexels-oleksandr-pidvalnyi-376361.jpg')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'],'pexels-yurii-hlei-1545743.jpg')
    pic3 = os.path.join(app.config['UPLOAD_FOLDER'],'pexels-alex-azabache-3879065.jpg')
    pic4 = os.path.join(app.config['UPLOAD_FOLDER'],'pexels-aleksey-kuprikov-3786091.jpg')
    print(usenum)
    
    usercasenumberoutput = connectMongo(usenum)
    print(usercasenumberoutput)
    return render_template('home.html',usecase=usenum , posts = posts , user_image = pic1 ,user_image2 = pic2, user_image3 = pic3,user_image4 = pic4,finuse = usercasenumberoutput)


@app.route("/")
@app.route("/home")  # to return the html
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'pexels-oleksandr-pidvalnyi-376361.jpg')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'],'pexels-yurii-hlei-1545743.jpg')
    pic3 = os.path.join(app.config['UPLOAD_FOLDER'],'pexels-alex-azabache-3879065.jpg')
    pic4 = os.path.join(app.config['UPLOAD_FOLDER'],'pexels-aleksey-kuprikov-3786091.jpg')
    return render_template('home.html', posts = posts , user_image = pic1 , user_image2 = pic2 ,user_image4 = pic4, user_image3 = pic3)






if __name__ == "__main__":
    app.run(debug = True)


"""

@app.route("/")
@app.route("/home")  # to return the html
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'icons8-sedan-64.jpg')
    return render_template('home.html', posts = posts , user_image = pic1)
"""