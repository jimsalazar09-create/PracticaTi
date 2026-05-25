from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300), default=" ")
    prioridad = db.Column(db.String(10), default="media")
    estado = db.Column(db.String(20), default="pendiente")
    asignado_a = db.Column(db.String(50), default=" ")
    def __repr__(self):
        return f"<Task {self.id} - {self.titulo}>"
    

