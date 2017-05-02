#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from requests_oauthlib import OAuth2Session
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, VARCHAR
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/golinks"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


app.config.update({
  'DEBUG': bool(os.environ.get('DEBUG')),
  'SECRET_KEY': os.environ.get('SECRET_KEY', 'CHANGEME'),
  'GOOGLE_CLIENT_ID': os.environ.get('GOOGLE_CLIENT_ID'),
  'GOOGLE_CLIENT_SECRET': os.environ.get('GOOGLE_CLIENT_SECRET'),
})


if app.debug:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if not app.config['GOOGLE_CLIENT_ID'] or not app.config['GOOGLE_CLIENT_SECRET']:
    raise RuntimeError('Environment not set up.')


class LinksTable(db.Model):
    __tablename__ = 'LinksTable'
    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR(45), unique=True)
    url = db.Column(VARCHAR(45))
    hits = db.Column(BIGINT)
    username = db.Column(VARCHAR(45))
    userid = db.Column(BIGINT)
    created_at = db.Column(DATETIME)

    def __repr__(self):
        return '<LinksTable http://go/%r (%r) >' % (self.name, self.url)


@app.route('/auth', defaults={'action': 'login'})
@app.route('/auth/<action>')
def auth(action):
    # Store some useful destinations in session
    if not request.args.get('state'):
        session['last'] = request.referrer or url_for('index')

        if 'next' in request.args:
            session['next'] = url_for(request.args['next'])
        else:
            session['next'] = session['last']

    google = OAuth2Session(
            app.config['GOOGLE_CLIENT_ID'],
            scope=['https://www.googleapis.com/auth/userinfo.email',
                   'https://www.googleapis.com/auth/userinfo.profile'],
            redirect_uri=url_for('auth', _external=True),
            state=session.get('state'))

    # Initial client request, no `state` from OAuth redirect
    if not request.args.get('state'):
        url, state = google.authorization_url('https://accounts.google.com/o/oauth2/auth', access_type='offline')
        session['state'] = state
        return redirect(url)

    # Error returned from Google
    if request.args.get('error'):
        error = request.args['error']
        return redirect(session['last'])

    # Redirect from google with OAuth2 state
    token = google.fetch_token(
            'https://accounts.google.com/o/oauth2/token',
            client_secret=app.config['GOOGLE_CLIENT_SECRET'],
            authorization_response=request.url)

    user = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()

    user['token'] = token
    session['user'] = user
    return redirect(session['next'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class GoLinkForm(FlaskForm):
    go = StringField("go/", validators=[DataRequired()])
    url = StringField("redirect to", validators=[DataRequired()])
    submit = SubmitField("Create")


class GoLinkEditForm(FlaskForm):
    go = StringField("go/", validators=[DataRequired()])
    url = StringField("new url", validators=[DataRequired()])
    update = SubmitField("Update")
    cancel = SubmitField("Cancel")


@app.route('/new', methods=["GET", "POST"])
def new():
    if not session.get('user'):
        return render_template("authenticate.html")

    form = GoLinkForm()

    if form.validate_on_submit():
        go = form.go.data
        url = form.url.data

        session.pop('_flashes', None)

        user = session.get('user')
        username = user.get('name', 'noname')
        userid = user.get('id', 101)

        go_link_exists = LinksTable.query.filter_by(name=go).first()

        if go_link_exists is None:
            link = LinksTable(name=go, url=url, hits=0, username=username, userid=userid, created_at=datetime.utcnow())
            db.session.add(link)
        else:
            flash("http://go/{go} link already exists. Please choose a different name.".format(go=go))

        form.go.data = ''
        form.url.data = ''
        return redirect("/")

    return render_template("new.html", form=form)


@app.route('/', methods=["GET"])
def index():
    link_details = LinksTable.query.with_entities(LinksTable.id, LinksTable.name, LinksTable.url).all()
    return render_template("index.html", link_details=link_details, user=session.get('user'))


@app.route('/edit/<id>', methods=["GET", "POST"])
def edit(id):
    if not session.get('user'):
        return render_template("authenticate.html")

    form = GoLinkEditForm()
    golink = LinksTable.query.get(id)

    if form.validate_on_submit():
        url = form.url.data
        golink.url = url
        db.session.commit()

        form.go.data = ""
        form.url.data = ""
        return redirect("/")

    return render_template("edit.html", form=form, user=session.get('user'))


@app.route('/logout', methods=["GET"])
def logout():
    if session.get("user"):
        del session['user']
    return redirect("/")


@app.route('/<go>')
def go(go):
    go_link = LinksTable.query.filter_by(name=go).first()
    if go_link is None:
        return redirect("/")

    redirect_response = redirect(go_link.url, code=302)

    redirect_response.headers.add('Last-Modified', datetime.now())
    redirect_response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    redirect_response.headers.add('Pragma', 'no-cache')

    return redirect_response


@app.route('/login')
def login():
    """Simple view to display info returned from Google (or a link to login)."""
    return render_template("login.html", user=session.get('user'))

if __name__ == '__main__':
    manager.run()
