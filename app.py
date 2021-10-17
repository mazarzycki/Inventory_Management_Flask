from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
db = SQLAlchemy(app)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Stock %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        goods_name = request.form['name']
        goods_category = request.form['category']
        goods_unit = request.form['unit']
        goods_value = request.form['value']
        goods_quantity = request.form['quantity']
        
        new_good = Stock(name = goods_name, category = goods_category, unit = goods_unit, value = goods_value, quantity = goods_quantity )

        try:
            db.session.add(new_good)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        goods = Stock.query.order_by(Stock.date_created).all()
        return render_template('index.html', goods=goods)

 
@app.route('/delete/<int:id>')
def delete(id):
    good_to_delete = Stock.query.get_or_404(id)

    try:
        db.session.delete(good_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that item'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Stock.query.get_or_404(id)

    if request.method == 'POST':
        item.name = request.form['name']
        item.category = request.form['category']
        item.unit = request.form['unit']
        item.value = request.form['value']
        item.quantity = request.form['quantity']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your item.'

    else:
        return render_template('update.html', item = item )


if __name__ == "__main__":
    app.run(debug=True)
