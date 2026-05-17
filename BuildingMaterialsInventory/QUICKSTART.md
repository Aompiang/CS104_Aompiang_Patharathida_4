# Quick Start Guide

Get the Building Materials Inventory System running in 2 minutes!

## Prerequisites
- Python 3.7+
- pip (Python package manager)

## Installation & Launch (Windows)

### 1. Open Command Prompt/PowerShell

### 2. Navigate to project directory
```powershell
cd "c:\Users\User\Desktop\CS104_Final\BuildingMaterialsInventory"
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

### 4. Create database with mock data
```powershell
python init_db.py
```

**Expected output:**
```
✓ Database initialized successfully with mock data!
```

### 5. Run the application
```powershell
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
```

### 6. Open in browser
Open your browser and go to:
```
http://localhost:5000
```

## What You'll See

✅ **Dashboard** — Real-time statistics (updates every 10 seconds)
- 13 Products
- Inventory value: ฿677,200
- Low stock alerts
- Best-selling items

✅ **Products Management** — Full CRUD
- View all 13 products
- Add, Edit, Delete products
- Stock status indicators

✅ **Suppliers Management** — Full CRUD
- View all 13 suppliers
- Manage contact information
- Link to products

✅ **Warehouses Management** — Full CRUD
- View all 13 warehouse locations
- Assign managers
- Track by location

## Features Explained

### Low Stock Alert
- Formula: Current Stock < (Initial Quantity × 30%)
- Example: If you ordered 100 units, alert triggers at < 30 units

### Real-time Dashboard
- Updates automatically every 10 seconds
- No page refresh needed
- Shows live inventory status

### Mock Data
- 13 building material products
- 13 suppliers across Thailand
- 13 distribution warehouses
- 20+ transaction records

## Database Location
```
./inventory.db
```

The database is auto-created on first run with sample data.

## Stopping the Application

In the terminal window, press:
```
Ctrl + C
```

## For Production Deployment

See `DEPLOYMENT.md` for detailed PythonAnywhere instructions.

## File Structure

```
BuildingMaterialsInventory/
├── app.py                    # Flask application
├── init_db.py               # Database initialization
├── wsgi.py                  # Production WSGI entry point
├── inventory.db             # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── README.md                # Full documentation
├── DEPLOYMENT.md            # PythonAnywhere guide
├── QUICKSTART.md            # This file
└── templates/
    ├── base.html            # Layout template
    ├── index.html           # Dashboard
    ├── products/            # Product CRUD pages
    ├── suppliers/           # Supplier CRUD pages
    └── warehouses/          # Warehouse CRUD pages
```

## Common Issues

### "ModuleNotFoundError: No module named 'flask'"
```powershell
pip install -r requirements.txt
```

### "Address already in use"
The port 5000 is occupied. Either:
- Close other Flask instances
- Or modify the port in `app.py` (change `port=5000` to another number)

### Database locked
- Close all Flask instances
- Run app.py again

## Next Steps

1. ✅ Run the app locally
2. ✅ Explore all features
3. ✅ Add your own products/suppliers/warehouses
4. 📘 Read `README.md` for detailed documentation
5. 🚀 Deploy to PythonAnywhere (see `DEPLOYMENT.md`)

## Support

- Flask docs: https://flask.palletsprojects.com/
- SQLite docs: https://www.sqlite.org/docs.html
- PythonAnywhere: https://www.pythonanywhere.com/help/

Happy inventory managing! 🎉
