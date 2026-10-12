import click
from flask.cli import with_appcontext
from .extensions import db


@click.command("create_table")
@with_appcontext
def create_table():
    db.create_all()


@click.command("query1")
@with_appcontext
def query1():
    pass
