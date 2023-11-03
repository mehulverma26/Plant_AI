from flask import Flask, render_template, request
from markupsafe import Markup
from model import predict_image
import utils

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        try:
            file = request.files["file"]
            if file:
                img = file.read()
                prediction = predict_image(img)
                print(prediction)
                if prediction in utils.disease_dic:
                    res = Markup(utils.disease_dic[prediction])
                    return render_template("display.html", status=200, result=res)
                else:
                    return render_template(
                        "index.html", status=400, res="Invalid Prediction"
                    )
            else:
                return render_template("index.html", status=400, res="No File Uploaded")
        except Exception as e:
            return render_template(
                "index.html", status=500, res="Internal Server Error"
            )

    return render_template("index.html", status=405, res="Method Not Allowed")


if __name__ == "__main__":
    app.run(debug=True)
