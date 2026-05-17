import sqlite3
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with schema and mock data"""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript("""
    -- Categories Table
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    );
    
    -- Suppliers Table
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT,
        email TEXT,
        address TEXT
    );
    
    -- Products Table
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        unit TEXT,
        cost_price REAL,
        sell_price REAL,
        initial_quantity INTEGER,
        stock INTEGER,
        supplier_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(category_id),
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    );
    
    -- Warehouses Table
    CREATE TABLE IF NOT EXISTS warehouses (
        warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        manager TEXT
    );
    
    -- Stock Movements Table
    CREATE TABLE IF NOT EXISTS stock_movements (
        movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        warehouse_id INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('IN','OUT','ADJUST')),
        quantity INTEGER NOT NULL,
        unit_price REAL,
        remark TEXT,
        date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
    );
    """)
    
    # Insert Categories (5 categories)
    categories = [
        ("Concrete & Cement", "Concrete and cement products"),
        ("Structural Steel", "Steel bars and structural materials"),
        ("Lumber & Wood", "Wooden materials and lumber"),
        ("Finishing Materials", "Paint, tiles, and finishes"),
        ("Hardware & Fasteners", "Screws, nails, bolts, and hardware"),
    ]
    cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)
    
    # Insert Suppliers (13 suppliers)
    suppliers = [
        ("Bangkok Cement Ltd.", "Sombat Saejung", "081-1234567", "sombat@bangkokcemnet.co.th", "123 Rama 4 Rd., Bangkok"),
        ("Northern Building Supply", "Niran Phumsawat", "081-2345678", "niran@northernbs.co.th", "456 Vibhavadi Rd., Bangkok"),
        ("Quality Steel Trading", "Anita Somjai", "081-3456789", "anita@qualitysteel.co.th", "789 Sukhumvit Rd., Bangkok"),
        ("Timber House Co.", "Somchai Ruangwiset", "081-4567890", "somchai@timberhouse.co.th", "321 Chaoen Rd., Chiang Mai"),
        ("Paint & Coating Solutions", "Wipa Suwanmethas", "081-5678901", "wipa@paintcosol.co.th", "654 Petchburi Rd., Bangkok"),
        ("Metro Hardware Center", "Krit Sunthararat", "081-6789012", "krit@metrohardware.co.th", "987 Silom Rd., Bangkok"),
        ("Eco Building Materials", "Fon Napaswan", "081-7890123", "fon@ecobuild.co.th", "741 Phraya Rd., Bangkok"),
        ("Premium Tile Distributors", "Pairot Chamsai", "081-8901234", "pairot@premiumtile.co.th", "852 Ladprao Rd., Bangkok"),
        ("Fast Logistics Steel", "Nuttaya Seangpet", "081-9012345", "nuttaya@fastlogistics.co.th", "963 Khlong Toei Rd., Bangkok"),
        ("Sunshine Lumber Yard", "Wattana Photinan", "082-0123456", "wattana@sunshunelumber.co.th", "159 Pathumwan, Bangkok"),
        ("Global Construction Supply", "Sita Jirajiraphol", "082-1234567", "sita@globalconst.co.th", "753 Rama 2 Rd., Bangkok"),
        ("Direct Fasteners Wholesale", "Yutaka Yamamoto", "082-2345678", "yutaka@directfasteners.co.th", "456 Ramkhamhaeng Rd., Bangkok"),
        ("Smart Building Tech", "Pattama Kusala", "082-3456789", "pattama@smartbuildtech.co.th", "321 Asok Rd., Bangkok"),
    ]
    cursor.executemany("""
        INSERT INTO suppliers (name, contact_person, phone, email, address) 
        VALUES (?, ?, ?, ?, ?)
    """, suppliers)
    
    # Insert Warehouses (13 warehouses)
    warehouses = [
        ("Main Warehouse Bangkok", "Bangkok, Khlong Toei", "Somchai Mungpetch"),
        ("North Regional Hub", "Chiang Mai, Muang", "Panumart Suksai"),
        ("East Regional Hub", "Rayong, Muang", "Siriporn Kanyarata"),
        ("South Regional Hub", "Songkhla, Hat Yai", "Montri Boonnag"),
        ("West Storage Facility", "Kanchanaburi, Muang", "Orawan Sunthara"),
        ("Secondary Bangkok WH", "Bangkok, Lat Phrao", "Niran Phumsawat"),
        ("Temporary Storage A", "Bangkok, Don Muang", "Arjun Raiwind"),
        ("Temporary Storage B", "Bangkok, Minburi", "Somsri Pattanakul"),
        ("Distribution Center 1", "Samut Prakarn, Muang", "Pitchaya Seuamung"),
        ("Distribution Center 2", "Nonthaburi, Pak Kret", "Kornprom Chaiwong"),
        ("Quality Control Lab WH", "Bangkok, Dusit", "Ananya Wisetpol"),
        ("Emergency Reserve WH", "Bangkok, Huai Khwang", "Pawarit Sungkhamanee"),
        ("Customer Pickup Point", "Bangkok, Bangna", "Nattha Kanthapan"),
    ]
    cursor.executemany("""
        INSERT INTO warehouses (name, location, manager) 
        VALUES (?, ?, ?)
    """, warehouses)
    
    # Insert Products (13 products)
    products = [
        ("SKU001", "Portland Cement 50kg", 1, "bag", 85.00, 120.00, 500, 380, 1),
        ("SKU002", "Steel Rebar 16mm", 2, "pcs", 45.00, 65.00, 1000, 650, 3),
        ("SKU003", "Teak Lumber Grade A", 3, "m³", 8500.00, 12000.00, 100, 45, 4),
        ("SKU004", "Premium Interior Paint 1L", 4, "can", 120.00, 180.00, 300, 220, 5),
        ("SKU005", "Ceramic Tile 60x60cm", 4, "box", 650.00, 950.00, 200, 120, 8),
        ("SKU006", "Stainless Steel Bolt M10", 5, "kg", 25.00, 40.00, 500, 320, 12),
        ("SKU007", "Galvanized Nails 5cm", 5, "kg", 15.00, 25.00, 400, 180, 6),
        ("SKU008", "Wooden Door Frame 80cm", 3, "pcs", 280.00, 420.00, 150, 80, 4),
        ("SKU009", "Aluminum Window Frame", 2, "pcs", 350.00, 520.00, 100, 45, 3),
        ("SKU010", "Brick Clay Standard", 1, "1000pcs", 1200.00, 1800.00, 50, 25, 7),
        ("SKU011", "Electrical Wire 2.5mm", 5, "roll", 180.00, 280.00, 200, 95, 9),
        ("SKU012", "Plywood Sheet 3mm", 3, "sheet", 180.00, 270.00, 300, 140, 4),
        ("SKU013", "Waterproof Sealant 500ml", 4, "tube", 95.00, 150.00, 250, 80, 5),
    ]
    cursor.executemany("""
        INSERT INTO products (sku, name, category_id, unit, cost_price, sell_price, 
                             initial_quantity, stock, supplier_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products)
    
    # Insert Stock Movements (20+ movements across different dates)
    movements = []
    base_date = datetime.now() - timedelta(days=60)
    
    movement_templates = [
        (1, 1, "IN", 100, 85.00, "Received from supplier"),
        (2, 2, "IN", 200, 45.00, "Received from supplier"),
        (1, 1, "OUT", 50, 120.00, "Sold to customer"),
        (3, 3, "IN", 10, 8500.00, "Received from supplier"),
        (4, 1, "IN", 50, 120.00, "Received from supplier"),
        (5, 4, "IN", 40, 650.00, "Received from supplier"),
        (6, 5, "IN", 150, 25.00, "Received from supplier"),
        (7, 6, "IN", 100, 15.00, "Received from supplier"),
        (8, 2, "OUT", 30, 420.00, "Sold to contractor"),
        (9, 3, "OUT", 20, 520.00, "Sold to contractor"),
        (2, 4, "OUT", 150, 65.00, "Sold to bulk order"),
        (10, 5, "IN", 15, 1200.00, "Received from supplier"),
        (11, 1, "IN", 80, 180.00, "Received from supplier"),
        (12, 2, "OUT", 80, 270.00, "Sold to project"),
        (13, 6, "IN", 100, 95.00, "Received from supplier"),
        (1, 3, "OUT", 60, 120.00, "Sold to bulk"),
        (4, 4, "OUT", 40, 180.00, "Sold to retail"),
        (7, 1, "OUT", 70, 25.00, "Sold to contractor"),
        (3, 5, "OUT", 30, 12000.00, "Sold to project"),
        (12, 3, "IN", 60, 180.00, "Received from supplier"),
    ]
    
    for i, (prod_id, wh_id, mov_type, qty, price, remark) in enumerate(movement_templates):
        movement_date = base_date + timedelta(days=i*3)
        movements.append((prod_id, wh_id, mov_type, qty, price, remark, movement_date.strftime("%Y-%m-%d")))
    
    cursor.executemany("""
        INSERT INTO stock_movements (product_id, warehouse_id, type, quantity, unit_price, remark, date) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, movements)
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully with mock data!")

if __name__ == "__main__":
    init_database()
