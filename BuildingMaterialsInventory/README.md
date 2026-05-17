# Building Materials Inventory Management System

A Flask-based web application for managing building materials inventory with real-time dashboard, products, suppliers, and warehouses management.

## Features

- **Real-time Dashboard** — Automatically updates every 10 seconds (AJAX polling)
  - Total products count
  - Inventory value
  - Low stock items (< 30% of initial quantity)
  - Best-selling products
  - Recent movements
  - Warehouse and supplier counts

- **CRUD Operations** for:
  - **Products** — Create, read, update, delete with SKU, pricing, and stock management
  - **Suppliers** — Manage supplier information and contact details
  - **Warehouses** — Multiple warehouse management with location and manager tracking

- **Database** — SQLite with 5 tables and 13+ records per table
  - Categories, Suppliers, Products, Warehouses, Stock Movements

- **Responsive UI** — Bootstrap 5 based interface with clean navigation

## Database Schema

### Tables:
1. **categories** — Product categories
2. **suppliers** — Supplier information
3. **products** — Product details with pricing and stock
4. **warehouses** — Warehouse locations and managers
5. **stock_movements** — IN/OUT/ADJUST transaction logs

### Low-Stock Logic:
- Low stock = current stock < 30% of `initial_quantity`
- Example: If initial_quantity = 100, low stock alert triggers at < 30 units

## Installation & Setup

### Local Development

1. **Clone or download the project folder**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize the database with mock data:**
```bash
python init_db.py
```
This creates `inventory.db` with sample data (13+ records per table).

4. **Run the Flask application:**
```bash
python app.py
```

5. **Open in browser:**
```
http://localhost:5000
```

## Project Structure

```
BuildingMaterialsInventory/
├── app.py                    # Flask application (routes and logic)
├── init_db.py               # Database initialization script
├── inventory.db             # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── templates/
    ├── base.html            # Base layout template
    ├── index.html           # Dashboard page
    ├── products/
    │   ├── list.html        # Products listing page
    │   └── form.html        # Product add/edit form
    ├── suppliers/
    │   ├── list.html        # Suppliers listing page
    │   └── form.html        # Supplier add/edit form
    └── warehouses/
        ├── list.html        # Warehouses listing page
        └── form.html        # Warehouse add/edit form
```

## Usage

### Dashboard
- View real-time statistics (updates every 10 seconds)
- See inventory value, low-stock items, best sellers
- Quick action buttons to add new items

### Products Management
- Add/Edit/Delete products
- Set initial quantity (for low-stock calculation)
- Assign categories and suppliers
- Track current stock levels

### Suppliers Management
- Add/Edit/Delete supplier information
- Store contact details and address
- Link suppliers to products

### Warehouses Management
- Add/Edit/Delete warehouse locations
- Assign managers to each warehouse
- Track warehouse-specific stock movements

## Deployment on PythonAnywhere

### Step 1: Upload files to PythonAnywhere
1. Log in to https://www.pythonanywhere.com/
2. Go to **Files** tab
3. Create a new folder (e.g., `building_materials_inventory`)
4. Upload all files from your project

### Step 2: Create a Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Python 3.X** version
4. Select **Flask**
5. Set source code directory to your project folder
6. Set working directory accordingly

### Step 3: Create virtual environment
1. Go to **Consoles** tab
2. Start a **Bash console**
3. Navigate to your project directory:
```bash
cd /home/your_username/building_materials_inventory
```

4. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Initialize database:
```bash
python init_db.py
```

### Step 4: Configure WSGI file
1. In **Web** tab, click on your web app
2. Under **Code section**, click on the **WSGI configuration file link**
3. Replace the Flask section with:
```python
import sys
path = '/home/your_username/building_materials_inventory'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

4. Save and reload your web app

### Step 5: Verify deployment
1. Visit your PythonAnywhere URL
2. Test CRUD operations
3. Verify dashboard updates work

## Mock Data Included

- **13 Products** — Building materials (cement, steel, lumber, paint, tiles, fasteners, etc.)
- **13 Suppliers** — Building material suppliers across Thailand
- **13 Warehouses** — Distribution centers and storage facilities
- **20+ Stock Movements** — IN/OUT transactions for realistic data
- **5 Categories** — Organized product types

## Technical Details

- **Framework:** Flask 2.3.3
- **Database:** SQLite3
- **Frontend:** Bootstrap 5.3.0, Chart.js 3.9.1
- **Real-time Updates:** AJAX Polling (10-second interval)
- **Python Version:** 3.X
- **Deployment:** PythonAnywhere compatible

## Notes

- All dates in database use ISO format (YYYY-MM-DD)
- Currency displayed as Thai Baht (฿) — modify CSS if needed
- AJAX polling is optimized for PythonAnywhere (no WebSockets needed)
- Database file is auto-generated on first run

## Support & Troubleshooting

**Q: Dashboard not updating?**
- Check browser console (F12) for JavaScript errors
- Verify `/api/dashboard-stats` endpoint returns JSON
- Try hard refresh (Ctrl+F5)

**Q: Database not found?**
- Run `python init_db.py` to create database and mock data

**Q: PythonAnywhere app not loading?**
- Check WSGI configuration file
- Verify virtual environment is activated
- Check error logs in PythonAnywhere console

## License

This project is for educational purposes.
