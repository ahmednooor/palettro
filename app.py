from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from cs50 import SQL
import operator
import sys
import optparse
import time


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
ind = 0
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
        ind = 0
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
        ind = 0
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



@app.route('/palette/<id>')
def singlePalette(id):
    palettes = db.execute("SELECT * FROM palettes WHERE id=:id", id=id)
    if len(palettes) != 0:
        return render_template("single_palette.html", success=True, palette=palettes[0])
    else:
        return render_template("single_palette.html", status="Palette not found.", success=False)



@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        color_1 = request.form["color_1"] if request.form["color_1"] else 0
        color_2 = request.form["color_2"] if request.form["color_2"] else 0
        color_3 = request.form["color_3"] if request.form["color_3"] else 0
        color_4 = request.form["color_4"] if request.form["color_4"] else 0
        color_5 = request.form["color_5"] if request.form["color_5"] else 0
        color_6 = request.form["color_6"] if request.form["color_6"] else 0
        color_7 = request.form["color_7"] if request.form["color_7"] else 0
        color_8 = request.form["color_8"] if request.form["color_8"] else 0

        palettes = db.execute("SELECT * FROM palettes WHERE color_1=:color_1 AND color_2=:color_2 AND color_3=:color_3 AND color_4=:color_4 AND color_5=:color_5 AND color_6=:color_6 AND color_7=:color_7 AND color_8=:color_8", color_1=color_1, color_2=color_2, color_3=color_3, color_4=color_4, color_5=color_5, color_6=color_6, color_7=color_7, color_8=color_8)

        if len(palettes) != 1:
            db.execute("INSERT INTO palettes (color_1, color_2, color_3, color_4, color_5, color_6, color_7, color_8) VALUES (:color_1, :color_2, :color_3, :color_4, :color_5, :color_6, :color_7, :color_8)", color_1=color_1, color_2=color_2, color_3=color_3, color_4=color_4, color_5=color_5, color_6=color_6, color_7=color_7, color_8=color_8)

            palettes = db.execute("SELECT * FROM palettes WHERE color_1=:color_1 AND color_2=:color_2 AND color_3=:color_3 AND color_4=:color_4 AND color_5=:color_5 AND color_6=:color_6 AND color_7=:color_7 AND color_8=:color_8", color_1=color_1, color_2=color_2, color_3=color_3, color_4=color_4, color_5=color_5, color_6=color_6, color_7=color_7, color_8=color_8)

            return redirect('/palette/' + str(palettes[0]["id"]))
        else:
            return render_template("single_palette.html", status="Palette already exists.", success=False)

    else: 
        return render_template("create.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python app.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print "Missing required argument: -p/--port"
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(args.port), debug=False)


