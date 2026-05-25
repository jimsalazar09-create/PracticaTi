from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Task

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskboard.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


with app.app_context():
    db.create_all()



@app.route("/")
def index():
    estado = request.args.get("estado", "")
    q      = request.args.get("q", "")
    tareas = Task.query

    if estado:
        tareas = tareas.filter_by(estado=estado)
    if q:
        tareas = tareas.filter(Task.titulo.contains(q))

    tareas = tareas.all()
    return render_template("index.html", tareas=tareas, estado=estado, q=q)

@app.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nueva = Task(
            titulo      = request.form["titulo"],
            descripcion = request.form["descripcion"],
            prioridad   = request.form["prioridad"],
            asignado_a  = request.form["asignado_a"],
        )
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")



@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    tarea = Task.query.get_or_404(id)
    if request.method == "POST":
        tarea.titulo      = request.form["titulo"]
        tarea.descripcion = request.form["descripcion"]
        tarea.prioridad   = request.form["prioridad"]
        tarea.asignado_a  = request.form["asignado_a"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", tarea=tarea)



@app.route("/eliminar/<int:id>")
def eliminar(id):
    tarea = Task.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for("index"))



@app.route("/toggle/<int:id>", methods=["POST"])
def toggle(id):
    tarea = Task.query.get_or_404(id)
    estados = ["pendiente", "en progreso", "completada"]
    i = estados.index(tarea.estado)
    tarea.estado = estados[(i + 1) % len(estados)]
    db.session.commit()
    return jsonify({"nuevo_estado": tarea.estado})


if __name__ == "__main__":
    app.run(debug=True)
