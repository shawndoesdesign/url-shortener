from flask import Flask, render_template, flash, url_for, redirect
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Optional, URL
import shutil
import os.path
ext = '.html'
globalfinal = 'none'

app = Flask(__name__, template_folder='./links', static_folder='assets')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class ShortenForm(FlaskForm):
    url = StringField(validators=[InputRequired(), URL(message="That is not a valid URL!"), Length(
        min=4, max=20)], render_kw={"placeholder": "Enter a URL"})
    slug = StringField(validators=[Optional(), Length(
        min=4, max=10)], render_kw={"placeholder": "Enter a Slug"})
    submit = SubmitField("Shorten!")


@app.route('/<id>', methods=['GET', 'POST'])
def find(id):
    find = "./links/{}{}".format(id, ext)

    if os.path.isfile(find) == True:

        stuff = "{}{}".format(id, ext)

        return render_template(stuff)

    if os.path.isfile(find) == False:

        return render_template('404.html')


@app.route('/', methods=['GET', 'POST'])
def shorten():
    form = ShortenForm()
    find = "./links/{}{}".format(id, ext)

    if os.path.isfile('./links/' + str(form.slug.data) + ext) == True:
        flash('That slug already exists! Please try another one or use a random slug.', 'error')
        return redirect('error')

    if form.validate_on_submit():
        if(len(form.slug.data)) == 0:
            random = str(uuid.uuid4())[:5]
            print(random)
            source = "./links/template.html"
            destination = "./links/" + random + ext

            if ShortenForm(url=str(form.url.data)).validate() == False:
                flash('That is not a valid URL!', 'error')
                return redirect('error')

            shutil.copyfile(source, destination)

            with open(destination, 'r') as file:
                filedata = file.read()

            filedata = filedata.replace('abcdefghijkl', form.url.data)

            with open(destination, 'w') as file:
                file.write(filedata)

            flash('https://stu.sh/' + random)

            return redirect('done')

        source = "./links/template.html"
        destination = "./links/" + str(form.slug.data) + ext

        shutil.copyfile(source, destination)

        with open(destination, 'r') as file:
            filedata = file.read()

        filedata = filedata.replace('abcdefghijkl', str(form.url.data))

        with open(destination, 'w') as file:
            file.write(filedata)

        flash('http://localhost:5000' + form.slug.data, 'success')

        return redirect('done')

    return render_template('shorten.html', form=form)


@app.route('/done')
def done():
    return render_template("done.html")


@app.route('/error')
def error():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)
