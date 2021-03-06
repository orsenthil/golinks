#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, VARCHAR

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update({
    'DEBUG'                         : bool(os.environ.get('DEBUG', False)),
    'SECRET_KEY'                    : os.environ.get('SECRET_KEY', 'CHANGE-ME'),
    'SQLALCHEMY_DATABASE_URI'       : os.environ.get('MYSQL_DB', "sqlite:///:memory:"),
    'SQLALCHEMY_COMMIT_ON_TEARDOWN' : True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

with app.open_resource('resources/create_table.sql', mode='r') as f:
    db.session.execute(f.read())

db.session.commit()


manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))

# Model


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


# Views

class GoLinkForm(FlaskForm):
    go = StringField("go/", validators=[DataRequired()])
    url = StringField("redirect to", validators=[DataRequired()])
    submit = SubmitField("Create")


class GoLinkEditForm(FlaskForm):
    go = StringField("go/", validators=[DataRequired()])
    url = StringField("new url", validators=[DataRequired()])
    update = SubmitField("Update")
    cancel = SubmitField("Cancel")


# Controllers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=["GET"])
def index():
    link_details = LinksTable.query.with_entities(LinksTable.id, LinksTable.name, LinksTable.url).all()
    return render_template("index.html", link_details=link_details, user=session.get('user'))


@app.route('/<go>')
def goto(go):
    go_link = LinksTable.query.filter_by(name=go).first()

    if go_link is None:
        return redirect("/")

    redirect_response = redirect(go_link.url, code=302)

    redirect_response.headers.add('Last-Modified', datetime.now())
    redirect_response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    redirect_response.headers.add('Pragma', 'no-cache')

    return redirect_response


@app.route('/new', methods=["GET", "POST"])
def new():
    form = GoLinkForm()

    if form.validate_on_submit():
        go = form.go.data
        url = form.url.data

        number_s_in_go = go.count("%s")
        number_s_in_url = url.count("%s")

        if number_s_in_go != number_s_in_url:
            flash("Please check your variable substitution.")
            return redirect("/new")

        session.pop('_flashes', None)

        user = session.get('user', 'default-user')
        username = 'name'# user.get('name')
        userid = 101 # user.get('id', 101)

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


@app.route('/edit/<id>', methods=["GET", "POST"])
def edit(id):
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


if __name__ == '__main__':
    manager.run()
