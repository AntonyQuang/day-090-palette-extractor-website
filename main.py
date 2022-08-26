from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import SubmitField
from wtforms.validators import InputRequired
import os
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = "a"
app.config['UPLOAD_FOLDER'] = "static/files"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB
Bootstrap(app)


class ImageForm(FlaskForm):
    image = FileField("Upload your image", validators=[FileRequired(),
                                                       FileAllowed(["jpg", "png"], "Images only!"),
                                                       InputRequired()])
    submit = SubmitField()

@app.route("/", methods=["GET"])
def home():

    form = ImageForm()

    return render_template("index.html", form=form)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        print("Photo saved")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)