# 🧺 SmartWash Pro — Professional Laundry Management System

**Owner: Suresh Gopi** | Version 1.0 | Built with Flask + MySQL

---

## 🚀 QUICK SETUP GUIDE

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

---

### Step 1: Clone / Extract the Project

```bash
cd smartwash-pro
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

```bash
mysql -u root -p
```

Then inside MySQL:
```sql
SOURCE schema.sql;
```

OR import via phpMyAdmin → Import → select `schema.sql`

### Step 5: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your MySQL credentials:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=smartwash_pro
SECRET_KEY=your-random-secret-key
```

### Step 6: Run the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 🔐 DEFAULT LOGIN CREDENTIALS

| Role  | Username    | Password   |
|-------|-------------|------------|
| Admin | sureshgopi  | Admin@123  |
| Staff | staff1      | Admin@123  |

> ⚠️ Change passwords immediately after first login!

---

## 📁 PROJECT STRUCTURE

```
smartwash/
├── app.py                 # Main Flask application
├── schema.sql             # MySQL database schema
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── README.md              # This file
│
├── models/
│   ├── __init__.py
│   └── database.py        # DB connection & decorators
│
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Login/logout
│   ├── dashboard.py       # Dashboard
│   ├── orders.py          # Order management
│   ├── customers.py       # Customer management
│   ├── reports.py         # Reports & analytics
│   ├── expenses.py        # Expense tracking
│   └── api.py             # REST API endpoints
│
├── services/
│   ├── __init__.py
│   ├── order_service.py   # Barcode, pricing logic
│   └── pdf_service.py     # Invoice PDF generation
│
├── templates/
│   ├── base.html          # Base layout (sidebar + navbar)
│   ├── auth/login.html
│   ├── dashboard/index.html
│   ├── orders/            # new_order, view_order, index
│   ├── customers/         # index, view
│   ├── reports/           # index
│   └── expenses/          # index
│
└── static/
    ├── css/main.css        # Premium SaaS styles
    ├── js/main.js          # Interactive JavaScript
    ├── uploads/            # Customer uploads
    └── pdfs/               # Generated invoices
```

---

## 🌐 DEPLOYMENT (Production)

### Using Gunicorn + Nginx

```bash
# Install gunicorn (already in requirements.txt)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/smartwash/static;
        expires 30d;
    }
}
```

### Run as Service (systemd)

Create `/etc/systemd/system/smartwash.service`:
```ini
[Unit]
Description=SmartWash Pro
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/smartwash
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable smartwash
sudo systemctl start smartwash
```

---

## 🔧 API ENDPOINTS

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/scan-barcode` | Fetch order by barcode |
| POST | `/api/calculate-price` | Calculate order price |
| GET  | `/api/pricing` | Get all pricing |
| GET  | `/api/search-customer` | Search customer by phone |
| POST | `/api/send-whatsapp/{id}` | Send WhatsApp notification |
| GET  | `/api/dashboard-stats` | Live dashboard stats |

---

## 📊 DATABASE TABLES

| Table | Description |
|-------|-------------|
| `users` | Admin & staff accounts |
| `customers` | Customer profiles |
| `orders` | Laundry orders |
| `order_items` | Per-garment breakdown |
| `payments` | Payment records |
| `expenses` | Business expenses |
| `logs` | Activity audit trail |
| `service_pricing` | Price configuration |

---

## 🎨 FEATURES SUMMARY

✅ **Dashboard** — Live stats, charts, activity feed  
✅ **New Order** — Auto customer lookup, item-wise pricing, barcode generation  
✅ **Order Tracking** — Barcode scanner (camera or manual), status updates  
✅ **PDF Invoices** — Professional invoice with QR code, downloadable  
✅ **WhatsApp** — One-click notification links (confirmation, ready, invoice)  
✅ **Reports** — Daily/weekly/monthly with charts  
✅ **Expenses** — Category-wise tracking with profit calculation  
✅ **Customers** — Full profile with order history  
✅ **Dark Mode** — Toggle with preference memory  
✅ **Responsive** — Mobile + tablet + desktop  
✅ **Role-Based Access** — Admin vs Staff permissions  
✅ **Security** — Password hashing (bcrypt), activity logging, SQL injection prevention  

---

## 📞 SUPPORT

**SmartWash Pro** — Built for Suresh Gopi's Professional Laundry Business  
For support: suresh@smartwashpro.com
