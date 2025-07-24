# Subscriptions-Monitor

A Flask web application for monitoring and managing your subscriptions. Track your monthly and yearly subscriptions, monitor renewal dates, and keep track of your spending across different currencies.

## Features

- **Dashboard Overview**: See your total subscription costs for the current month
- **Multi-Currency Support**: Track subscriptions in USD ($), EUR (€), and ILS (₪)
- **Billing Cycles**: Support for both monthly and yearly subscriptions
- **Renewal Tracking**: Monitor upcoming renewals and overdue payments
- **CRUD Operations**: Add, edit, and delete subscriptions
- **Modern UI**: Beautiful, responsive interface built with Bootstrap 5

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Subscriptions-Monitor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## Usage

### Adding a Subscription
1. Click "Add Subscription" in the navigation
2. Fill in the subscription details:
   - **Name**: Descriptive name (e.g., "Netflix", "Spotify")
   - **Cost**: Amount in your chosen currency
   - **Currency**: USD, EUR, or ILS
   - **Billing Cycle**: Monthly or Yearly
   - **Next Renewal Date**: When the subscription will next charge you

### Managing Subscriptions
- **View**: All subscriptions are displayed on the main dashboard
- **Edit**: Click the edit icon (pencil) next to any subscription
- **Delete**: Click the delete icon (trash) and confirm the deletion

### Dashboard Features
- **Monthly Totals**: See how much you'll pay this month by currency
- **Upcoming Renewals**: View subscriptions renewing in the next 30 days
- **Overdue Alerts**: Subscriptions past their renewal date are highlighted
- **Quick Actions**: Easy access to add, edit, and delete functions

## Database

The application uses SQLite with the following schema:

```sql
CREATE TABLE subscription (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cost FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    billing_cycle VARCHAR(10) NOT NULL,
    next_renewal DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

- `GET /` - Main dashboard
- `GET /add` - Add subscription form
- `POST /add` - Create new subscription
- `GET /edit/<id>` - Edit subscription form
- `POST /edit/<id>` - Update subscription
- `POST /delete/<id>` - Delete subscription
- `GET /api/subscriptions` - JSON API for all subscriptions

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: SQLite
- **Styling**: Custom CSS with gradients and animations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.