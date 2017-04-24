from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from cs50 import SQL
import operator

# configure flask
app = Flask(__name__)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///colors.db")

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


inx = 0
ind = 20
@app.route('/')
def index():
    global inx
    global ind
    if request.args.get("more"):
        ind = ind + int(request.args.get("more"))
        palettes = db.execute("SELECT * FROM palettes")
        palettes.reverse()
        if ind > len(palettes):
            ind = len(palettes)

        palettes = palettes[inx:ind]
        inx = ind
        return jsonify(palettes)
    elif request.args.get("id"):
        id = int(request.args.get("id"))
        palette = db.execute("SELECT * FROM palettes WHERE id=:id", id=id)
        palette[0]["hearts"] += 1
        db.execute("UPDATE palettes SET hearts=:hearts WHERE id=:id", hearts=palette[0]["hearts"], id=id)
        return jsonify(palette)
    elif request.args.get("idd"):
        id = int(request.args.get("idd"))
        palette = db.execute("SELECT * FROM palettes WHERE id=:id", id=id)
        palette[0]["hearts"] -= 1
        db.execute("UPDATE palettes SET hearts=:hearts WHERE id=:id", hearts=palette[0]["hearts"], id=id)
        return jsonify(palette)
    else:
        inx = 0
        ind = 20
        palettes = db.execute("SELECT * FROM palettes")
        palettes.reverse()
        if ind > len(palettes):
            ind = len(palettes)
        palettes = palettes[inx:ind]
        inx = ind
        return render_template("index.html", palettes=palettes)


@app.route('/popular')
def popular():
    global inx
    global ind
    if request.args.get("more"):
        ind = ind + int(request.args.get("more"))
        palettes = db.execute("SELECT * FROM palettes")
        palettes = sorted(palettes, key=operator.itemgetter("hearts"), reverse=True)
        print(inx, ind)
        if ind > len(palettes):
            ind = len(palettes)

        palettes = palettes[inx:ind]
        inx = ind
        return jsonify(palettes)
    elif request.args.get("id"):
        id = int(request.args.get("id"))
        palette = db.execute("SELECT * FROM palettes WHERE id=:id", id=id)
        palette[0]["hearts"] += 1
        db.execute("UPDATE palettes SET hearts=:hearts WHERE id=:id", hearts=palette[0]["hearts"], id=id)
        return jsonify(palette)
    elif request.args.get("idd"):
        id = int(request.args.get("idd"))
        palette = db.execute("SELECT * FROM palettes WHERE id=:id", id=id)
        palette[0]["hearts"] -= 1
        db.execute("UPDATE palettes SET hearts=:hearts WHERE id=:id", hearts=palette[0]["hearts"], id=id)
        return jsonify(palette)
    else:
        inx = 0
        ind = 20
        palettes = db.execute("SELECT * FROM palettes")
        palettes = sorted(palettes, key=operator.itemgetter("hearts"), reverse=True)
        print(inx, ind)                
        if ind > len(palettes):
            ind = len(palettes)
        palettes = palettes[inx:ind]
        inx = ind
        return render_template("popular.html", palettes=palettes)
    

@app.route('/favourites')
def favourites():
    if request.args.get("idf"):
        id = request.args.get("idf")
        palette = db.execute("SELECT * FROM palettes WHERE id=:id", id=id)
        return jsonify(palette)
    elif request.args.get("id"):
        id = int(request.args.get("id"))
        palette = db.execute("SELECT * FROM palettes WHERE id=:id", id=id)
        palette[0]["hearts"] += 1
        db.execute("UPDATE palettes SET hearts=:hearts WHERE id=:id", hearts=palette[0]["hearts"], id=id)
        return jsonify(palette)
    elif request.args.get("idd"):
        id = int(request.args.get("idd"))
        palette = db.execute("SELECT * FROM palettes WHERE id=:id", id=id)
        palette[0]["hearts"] -= 1
        db.execute("UPDATE palettes SET hearts=:hearts WHERE id=:id", hearts=palette[0]["hearts"], id=id)
        return jsonify(palette)
    return render_template("favourites.html")



@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        palettes = db.execute("SELECT * FROM palettes WHERE color_1=:color_1 AND color_2=:color_2 AND color_3=:color_3 AND color_4=:color_4", color_1=request.form["color_1"], color_2=request.form["color_2"], color_3=request.form["color_3"], color_4=request.form["color_4"])

        if len(palettes) != 1:
            db.execute("INSERT INTO palettes (color_1, color_2, color_3, color_4) VALUES (:color_1, :color_2, :color_3, :color_4)", color_1=request.form["color_1"], color_2=request.form["color_2"], color_3=request.form["color_3"], color_4=request.form["color_4"])

            return render_template("submit_status.html", status="Palette added successfully.", success=True)
        else:
            return render_template("submit_status.html", status="Palette already exists.", success=False)

        return request.form["color_1"] + request.form["color_2"] + request.form["color_3"] + request.form["color_4"]
    else: 
        return render_template("create.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
