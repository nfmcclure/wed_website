import os
import csv
from flask import Flask
from flask import render_template, url_for, redirect
from wtforms import Form, FormField, BooleanField, StringField, validators, SelectField, TextAreaField
from flask import request, flash

app = Flask(__name__, static_url_path='')


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


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/ceremony")
def ceremony():
    return render_template('ceremony.html')


@app.route("/accommodations")
def accommodations():
    return render_template('accommodations.html')


@app.route("/ourstory")
def ourstory():
    return render_template('ourstory.html')


@app.route("/schedule")
def schedule():
    return render_template('schedule.html')


@app.route("/beers")
def beers():
    return render_template('beers.html')

@app.route("/registry")
def registry():
    return render_template('registry.html')


# RSVP form class
class RsvpForm(Form):
    name = StringField('Name', [validators.length(min=3, max=25, message="Must be between 3 and 25 charaters."),])
    email = StringField('Email Address', [validators.Email(message="Must be a valid email address.")])
    num_guest_list = [('1', '1'), ('2', '2')]
    num_guests = SelectField('Number of Guests', choices=num_guest_list, validators=[validators.DataRequired()])
    comments = TextAreaField("Additional Comments", default="Let us know any special needs or additional comments/concerns!")


# Save information to a CSV file
def save2csv(csv_file, info_dict):
    if not os.path.exists(csv_file):
        with open(csv_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([info_dict['name'], info_dict['email'],
                             info_dict['number_guests'],
                             info_dict['comments']])
    else:
        with open(csv_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([info_dict['name'], info_dict['email'],
                             info_dict['number_guests'],
                             info_dict['comments']])

@app.route("/rsvp", methods=['GET', 'POST'])
def rsvp():
    form = RsvpForm(request.form)
    if request.method == 'POST' and form.validate():
        info_dict = {'name': form.name.data,
                     'email': form.email.data,
                     'number_guests': form.num_guests.data,
                     'comments': form.comments.data}
        csv_file = 'static/db/rsvp.csv'
        save2csv(csv_file=csv_file, info_dict=info_dict)
        #print('{}: {}'.format(info_dict['name'], info_dict['email']))
        flash('RSVP sent, thanks!')
        return redirect(url_for('rsvp'))
    return render_template('rsvp.html', form=form)


@app.route("/visitinfo")
def visitinfo():
    return render_template('visitinfo.html')


if __name__ == '__main__':
    app.secret_key = 'frankwalker217'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()