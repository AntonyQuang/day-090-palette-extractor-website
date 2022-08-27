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
                                                       ])
    submit = SubmitField()

@app.route("/", methods=["GET", "POST"])
def home():
    uploaded_image = None
    form = ImageForm()
    if form.validate_on_submit():
        # Getting the folder to delete any old files
        image_folder = app.config['UPLOAD_FOLDER']
        # os.listdir creates a list of files in the image folder, but not the complete path
        for junk_file in os.listdir(image_folder):
            # Deletes the images in the folder
            os.remove(os.path.join(image_folder, junk_file))
        # Save the uploaded file
        file = form.image.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        uploaded_image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("Photo Saved")
        return render_template("index.html", form=form, image=uploaded_image)
    return render_template("index.html", form=form, image=uploaded_image)


@app.errorhandler(413)
def largefile_error(error):
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)