
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class ToDo(db.Model):
    Sno= db.Column(db.Integer, primary_key=True)
    Title= db.Column(db.String(100),nullable=False)
    Desc= db.Column(db.String(600), nullable=False)
    date_of_cre= db.Column(db.DateTime, default=datetime.utcnow)
   

    def __repr__(self) -> str:
        return (f"{self.Sno} , {self.Title}")


@app.route('/')
def hello_world():
    return "x"


@app.route('/render', methods=['GET', 'POST'])
def render():
    if request.method=='POST':
        Title=request.form['Title']
        Desc=request.form['Desc']
        todo = ToDo(Title=Title, Desc=Desc)
        db.session.add(todo)
        db.session.commit()
    AllToDo=ToDo.query.all()
    return render_template('index.html', AllToDo=AllToDo)


@app.route('/delete/<int:snn>')
def delete(snn):
    AllToDo=ToDo.query.filter_by(Sno=snn).first()
    db.session.delete(AllToDo)
    db.session.commit()
    return redirect('/render')

   
@app.route('/update/<int:sn>', methods=['GET', 'POST'])
def update(sn):
    if request.method=='POST':
        Title=request.form['Title']
        Desc=request.form['Desc']
        tod=ToDo.query.filter_by(Sno=sn).first()
        tod.Title=Title
        tod.Desc=Desc
        db.session.add(tod)
        db.session.commit()  
        return redirect('/render')
    AllToDo=ToDo.query.filter_by(Sno=sn).first()
    return render_template('update.html', AllToDo=AllToDo) 
    


if __name__=="__main__":
    app.run(debug=True, port=8080)




