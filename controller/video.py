from flask import Blueprint, render_template

video = Blueprint("video", __name__)


@video.route('/video')
def home():
    return render_template('/monitor.html')