from flask import render_template, Blueprint, send_file
from utils.funcs import split_into_groups, load_projects
import os


pw = Blueprint('pw', __name__)


@pw.route("/")
def home():
    return render_template('pw/index.html')


@pw.route("/.well-known/acme-challenge/<file>")
def ssl(file):
    directory_path = '/var/www/certbot'
    file_path = os.path.join(directory_path, file)
    return send_file(file_path)


@pw.route("/cv")
def cv():
    return render_template('pw/cv.html')


@pw.route("/projects")
def projects():
    projects = split_into_groups(load_projects())
    return render_template('pw/projects.html', projects=projects)


@pw.route("/skills")
def skills():
    return render_template('pw/skills.html')
