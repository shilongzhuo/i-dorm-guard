from flask import Blueprint, render_template

notice = Blueprint("notice", __name__)


@notice.route('/notice_board')
def notice_board():
    return render_template('/notice/notice_board.html')


@notice.route('/article')
def article():
    return render_template('/notice/article.html')


@notice.route('/article_1')
def article_1():
    return render_template('/notice/article_1.html')

@notice.route('/article_2')
def article_2():
    return render_template('/notice/article_2.html')
