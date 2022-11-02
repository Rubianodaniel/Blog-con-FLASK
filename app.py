
from flask import Flask,render_template,redirect,request

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/drubianm/Desktop/blog/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__="posts"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)
    texto = db.Column (db.String, nullable=False)

    def __init__(self,titulo,texto):
        self.titulo = titulo
        self.texto = texto

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    posts = Post.query.order_by(Post.fecha.desc()).all()
    return render_template("home.html", posts = posts)

@app.route("/add")
def add():
    return render_template("agregar.html")

@app.route("/create_post", methods=["POST"])
def create_post():
    titulo = request.form.get("titulo")
    texto = request.form.get("texto")
    post = Post(titulo=titulo,texto=texto)
    db.session.add(post)
    db.session.commit()
    return redirect("/")
    
@app.route("/delete",methods=["POST"])
def delete():
    post_id = request.form.get("post_id")
    post = db.session.query(Post).filter(Post.id==post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/")




if __name__=='__main__':
    app.run(debug=True)