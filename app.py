from flask import Flask, render_template, request, redirect, url_for, abort
from models import *

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return render_template('index.html', wishes=get_all_wishes(), total=get_total_cost())

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        errors = validate(request.form['name'], request.form['price'])
        if errors:
            return render_template('add.html', errors=errors)
        add_wish(request.form['name'], request.form['price'], request.form.get('url',''), request.form.get('status','хочу'))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/wish/<int:id>')
def detail(id):
    wish = get_wish(id)
    if not wish:
        abort(404)
    return render_template('detail.html', wish=wish)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    wish = get_wish(id)
    if not wish:
        abort(404)
    if request.method == 'POST':
        errors = validate(request.form['name'], request.form['price'])
        if errors:
            return render_template('edit.html', wish=wish, errors=errors)
        update_wish(id, request.form['name'], request.form['price'], request.form.get('url',''), request.form.get('status','хочу'))
        return redirect(url_for('index'))
    return render_template('edit.html', wish=wish)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if get_wish(id):
        delete_wish(id)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    q = request.args.get('q', '')
    if not q:
        return redirect(url_for('index'))
    return render_template('index.html', wishes=search_wishes(q), total=0)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
