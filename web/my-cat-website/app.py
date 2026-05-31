from flask import Flask, request, jsonify, render_template
import random

# TODO: figure out if I want them to have the flag or not
give_flag = False

class Cat:
    is_happy = False
    
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "color": self.color,
            "is_happy": self.is_happy
        }

# https://www.asciiart.eu/animals/cats
cat_ascii = [
    """    |\\__/,|   (`\\
  _.|o o  |_   ) )
-(((---(((--------
""",
"""      |\\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\\ (  `'-'
    '---''(_/--'  `-'\\_) 
""",
""" _._     _,-'""`-._
(,-.`._,'(       |\\`-/|
    `-.-' \\ )-`( , o o)
          `-    \\`_`"'-
""",
"""           __..--''``---....___   _..._    __
 /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
///_.-' _..--.'_    \\                    `( ) ) // //
/ (_..-' // (< _     ;_..__               ; `' / ///
 / // // //  `-._,_)' // / ``--...____..-' /// / //
""",
""" |\\__/,|   (`\\
 |_ _  |.--.) )
 ( T   )     /
(((^_(((/(((_/
"""
]

def merge(src, dst):
    # Recursive merge function
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("cat_form.html")

@app.route("/cat", methods=["POST"])
def create_cat():
    """
    Expects JSON payload like:
    {
        "name": "Whiskers",
        "age": 3,
        "color": "tabby",
        "is_happy": true
    }
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    print(data)

    # Basic validation
    required_fields = ["name", "age", "color"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # make the cat
    cat = Cat()
    merge(data, cat)
    cat = cat.to_dict()

    if give_flag and cat.get("is_happy"):
        return render_template("flag.html", cat=cat, cat_ascii=cat_ascii)

    print(cat)
    return render_template("cat.html", ascii_art=random.choice(cat_ascii), **cat)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, debug=False)
