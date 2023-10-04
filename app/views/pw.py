from flask import render_template, Blueprint
from utils.funcs import split_into_groups, load_projects

pw = Blueprint('pw', __name__)


@pw.route("/")
def home():
    return render_template('pw/index.html')


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
