import os
from io import BytesIO

from flask import Flask, render_template, request, send_file, session

import parser

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    url = request.form['url']
    session['url'] = url
    number_of_signatures = parser.get_number_of_signatures_for_petition(url)
    return render_template('output.html', number_of_signatures=number_of_signatures)


@app.route('/download')
def download():
    url = session.get('url', None)
    petition_code = url.split('/')[-1]
    json = parser.get_signatories_for_petition(url)
    json_io = BytesIO(json.getvalue().encode('utf8'))
    return send_file(json_io, download_name=f'signatories_{petition_code}.json', mimetype='json', as_attachment=True)


if __name__ == '__main__':
    app.run()
