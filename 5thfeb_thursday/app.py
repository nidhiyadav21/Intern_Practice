from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)


#Flask App Routing
@app.route('/',methods=['GET'])
def hello_world():
        return '<h1>Hello, World!</h1>'
@app.route('/hello',methods=['GET'])
def index():
        return "<h1>Welcome to PyCharm!</h1>"


#Variable Rule
@app.route('/success/<int:score>',methods=['GET'])
def success(score):
        return "The person has passed and the score is:" + str(score)

@app.route('/fail/<int:score>',methods=['GET'])
def failure(score):
        return "The person has failed and the score is:" + str(score)

@app.route('/form',methods=['GET','POST'])
def form():
        if request.method == "GET":
                return render_template("form.html")
        else:
            maths = float(request.form['maths'])
            science = float(request.form['science'])
            history = float(request.form['history'])

            average_marks = ((maths+science+history)/3)

            res= ""
            if average_marks >= 50:
                    res="success"
            else:
                    res="failure"
            return redirect(url_for(res,score=average_marks))

           # return render_template("form.html",score=average_marks)





if __name__ == "__main__":
        app.run(debug=True)