from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import SubmitField
from PIL import Image
import os
import numpy as np
import pandas

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
    top_colours = None
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
        top_colours = extract(uploaded_image)
        return render_template("index.html", form=form, image=uploaded_image)
    return render_template("index.html", form=form, image=uploaded_image)


@app.errorhandler(413)
def largefile_error(error):
    return redirect(url_for("home"))


def extract(uploaded_image):
    img = Image.open(uploaded_image)
    img_array = np.array(img)

    # Each height goes along the row stating the colours
    # img_array is an array of a list of heights. Each height list contains a list of its rows. Each row list contains
    # colour elements

    list_of_colours = []
    for height_list in img_array:
        for row in height_list:
            colour_tuple = (row[0], row[1], row[2])
            # This is a specific format thing where "02X" means change to hexadecimal
            hex_string = "#%02X%02X%02X" % colour_tuple
            list_of_colours.append(hex_string)
    colours = pandas.Series(list_of_colours)
    top_colours = colours.value_counts().index.tolist()[0:10]

    return top_colours


if __name__ == "__main__":
    app.run(debug=True)