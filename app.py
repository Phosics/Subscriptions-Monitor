from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)  # USD, EUR, ILS
    billing_cycle = db.Column(db.String(10), nullable=False)  # monthly, yearly
    next_renewal = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Subscription {self.name}>'

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Get current month's subscriptions
    current_month = date.today().month
    current_year = date.today().year
    
    # Get subscriptions that will renew this month
    monthly_subscriptions = Subscription.query.filter(
        db.extract('month', Subscription.next_renewal) == current_month,
        db.extract('year', Subscription.next_renewal) == current_year
    ).all()
    
    # Calculate total cost by currency
    totals = {'USD': 0, 'EUR': 0, 'ILS': 0}
    for sub in monthly_subscriptions:
        totals[sub.currency] += sub.cost
    
    # Get all subscriptions for display
    all_subscriptions = Subscription.query.order_by(Subscription.next_renewal).all()
    
    # Get upcoming renewals (next 30 days)
    thirty_days_from_now = date.today() + timedelta(days=30)
    upcoming_renewals = Subscription.query.filter(
        Subscription.next_renewal <= thirty_days_from_now,
        Subscription.next_renewal >= date.today()
    ).order_by(Subscription.next_renewal).all()
    
    return render_template('index.html', 
                         monthly_subscriptions=monthly_subscriptions,
                         totals=totals,
                         all_subscriptions=all_subscriptions,
                         upcoming_renewals=upcoming_renewals,
                         date=date,
                         timedelta=timedelta)

@app.route('/add', methods=['GET', 'POST'])
def add_subscription():
    if request.method == 'POST':
        name = request.form['name']
        cost = float(request.form['cost'])
        currency = request.form['currency']
        billing_cycle = request.form['billing_cycle']
        next_renewal = datetime.strptime(request.form['next_renewal'], '%Y-%m-%d').date()
        
        subscription = Subscription(
            name=name,
            cost=cost,
            currency=currency,
            billing_cycle=billing_cycle,
            next_renewal=next_renewal
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        flash('Subscription added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_subscription(id):
    subscription = Subscription.query.get_or_404(id)
    
    if request.method == 'POST':
        subscription.name = request.form['name']
        subscription.cost = float(request.form['cost'])
        subscription.currency = request.form['currency']
        subscription.billing_cycle = request.form['billing_cycle']
        subscription.next_renewal = datetime.strptime(request.form['next_renewal'], '%Y-%m-%d').date()
        subscription.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Subscription updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', subscription=subscription)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_subscription(id):
    subscription = Subscription.query.get_or_404(id)
    db.session.delete(subscription)
    db.session.commit()
    
    flash('Subscription deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/api/subscriptions')
def api_subscriptions():
    subscriptions = Subscription.query.all()
    return jsonify([{
        'id': sub.id,
        'name': sub.name,
        'cost': sub.cost,
        'currency': sub.currency,
        'billing_cycle': sub.billing_cycle,
        'next_renewal': sub.next_renewal.strftime('%Y-%m-%d'),
        'created_at': sub.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for sub in subscriptions])

if __name__ == '__main__':
    app.run(debug=True, port=5002) 