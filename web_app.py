from flask import Flask, render_template, request

import parser

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    url = request.form['url']
    number_of_signatures = parser.get_number_of_signatures_for_petition(url)
    return "There are {} signatures for this petition".format(number_of_signatures)


if __name__ == '__main__':
    app.run()
