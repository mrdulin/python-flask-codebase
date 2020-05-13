from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/updatecontact', methods=['POST', 'GET'])
def update_contact():
    if request.method == 'POST':
        try:
            return 'success'
        except Exception as e:
            return str(e), 400
    else:
        return render_template('updatecontact.html')
