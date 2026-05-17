from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Make datetime available in all templates
@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row to dict"""
    if row:
        return dict(row)
    return None

# ======================== DASHBOARD ROUTES ========================
@app.route('/')
def index():
    """Dashboard homepage"""
    return render_template('index.html')

@app.route('/api/dashboard-stats')
def get_dashboard_stats():
    """API endpoint for realtime dashboard stats (AJAX polling)"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Total products count
        cursor.execute("SELECT COUNT(*) as total FROM products")
        total_products = cursor.fetchone()['total']
        
        # Total stock value
        cursor.execute("SELECT SUM(stock * cost_price) as total_value FROM products")
        total_value = cursor.fetchone()['total_value'] or 0
        
        # Low stock items (< 30% of initial quantity)
        cursor.execute("""
            SELECT COUNT(*) as count FROM products 
            WHERE stock < (initial_quantity * 0.3)
        """)
        low_stock_count = cursor.fetchone()['count']
        
        # Best selling product (highest OUT quantity)
        cursor.execute("""
            SELECT p.name, SUM(sm.quantity) as total_sold
            FROM stock_movements sm
            JOIN products p ON sm.product_id = p.product_id
            WHERE sm.type = 'OUT'
            GROUP BY sm.product_id
            ORDER BY total_sold DESC
            LIMIT 1
        """)
        best_seller = cursor.fetchone()
        best_seller_name = best_seller['name'] if best_seller else "N/A"
        best_seller_qty = best_seller['total_sold'] if best_seller else 0
        
        # Recent movements (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) as count FROM stock_movements
            WHERE date >= date('now', '-7 days')
        """)
        recent_movements = cursor.fetchone()['count']
        
        # Total warehouses
        cursor.execute("SELECT COUNT(*) as total FROM warehouses")
        total_warehouses = cursor.fetchone()['total']
        
        # Total suppliers
        cursor.execute("SELECT COUNT(*) as total FROM suppliers")
        total_suppliers = cursor.fetchone()['total']
        
        stats = {
            'total_products': total_products,
            'total_value': round(total_value, 2),
            'low_stock_count': low_stock_count,
            'best_seller': best_seller_name,
            'best_seller_qty': best_seller_qty,
            'recent_movements': recent_movements,
            'total_warehouses': total_warehouses,
            'total_suppliers': total_suppliers,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(stats)
    finally:
        conn.close()

# ======================== PRODUCTS ROUTES ========================
@app.route('/products')
def list_products():
    """List all products"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, c.name as category_name, s.name as supplier_name,
               CASE WHEN p.stock < (p.initial_quantity * 0.3) 
                    THEN 'Low Stock' ELSE 'OK' END as stock_status
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
        ORDER BY p.product_id
    """)
    products = cursor.fetchall()
    conn.close()
    return render_template('products/list.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """Add new product"""
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO products 
                (sku, name, category_id, unit, cost_price, sell_price, 
                 initial_quantity, stock, supplier_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request.form['sku'],
                request.form['name'],
                request.form['category_id'],
                request.form['unit'],
                float(request.form['cost_price']),
                float(request.form['sell_price']),
                int(request.form['initial_quantity']),
                int(request.form['stock']),
                request.form['supplier_id'] if request.form['supplier_id'] else None
            ))
            conn.commit()
            return redirect(url_for('list_products'))
        except Exception as e:
            return f"Error: {str(e)}", 400
        finally:
            conn.close()
    
    # GET: fetch categories and suppliers
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    cursor.execute("SELECT * FROM suppliers ORDER BY name")
    suppliers = cursor.fetchall()
    conn.close()
    
    return render_template('products/form.html', 
                         categories=categories, suppliers=suppliers, product=None)

@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    """Edit existing product"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        try:
            cursor.execute("""
                UPDATE products 
                SET sku=?, name=?, category_id=?, unit=?, cost_price=?, 
                    sell_price=?, initial_quantity=?, stock=?, supplier_id=?
                WHERE product_id=?
            """, (
                request.form['sku'],
                request.form['name'],
                request.form['category_id'],
                request.form['unit'],
                float(request.form['cost_price']),
                float(request.form['sell_price']),
                int(request.form['initial_quantity']),
                int(request.form['stock']),
                request.form['supplier_id'] if request.form['supplier_id'] else None,
                product_id
            ))
            conn.commit()
            conn.close()
            return redirect(url_for('list_products'))
        except Exception as e:
            conn.close()
            return f"Error: {str(e)}", 400
    
    # GET: fetch product and form data
    cursor.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
    product = dict_from_row(cursor.fetchone())
    
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    cursor.execute("SELECT * FROM suppliers ORDER BY name")
    suppliers = cursor.fetchall()
    conn.close()
    
    return render_template('products/form.html', 
                         categories=categories, suppliers=suppliers, product=product)

@app.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """Delete product"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM products WHERE product_id=?", (product_id,))
        conn.commit()
        return redirect(url_for('list_products'))
    except Exception as e:
        return f"Error: {str(e)}", 400
    finally:
        conn.close()

# ======================== SUPPLIERS ROUTES ========================
@app.route('/suppliers')
def list_suppliers():
    """List all suppliers"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers ORDER BY supplier_id")
    suppliers = cursor.fetchall()
    conn.close()
    return render_template('suppliers/list.html', suppliers=suppliers)

@app.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    """Add new supplier"""
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO suppliers (name, contact_person, phone, email, address)
                VALUES (?, ?, ?, ?, ?)
            """, (
                request.form['name'],
                request.form['contact_person'],
                request.form['phone'],
                request.form['email'],
                request.form['address']
            ))
            conn.commit()
            return redirect(url_for('list_suppliers'))
        except Exception as e:
            return f"Error: {str(e)}", 400
        finally:
            conn.close()
    
    return render_template('suppliers/form.html', supplier=None)

@app.route('/suppliers/<int:supplier_id>/edit', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    """Edit existing supplier"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        try:
            cursor.execute("""
                UPDATE suppliers 
                SET name=?, contact_person=?, phone=?, email=?, address=?
                WHERE supplier_id=?
            """, (
                request.form['name'],
                request.form['contact_person'],
                request.form['phone'],
                request.form['email'],
                request.form['address'],
                supplier_id
            ))
            conn.commit()
            conn.close()
            return redirect(url_for('list_suppliers'))
        except Exception as e:
            conn.close()
            return f"Error: {str(e)}", 400
    
    cursor.execute("SELECT * FROM suppliers WHERE supplier_id=?", (supplier_id,))
    supplier = dict_from_row(cursor.fetchone())
    conn.close()
    
    return render_template('suppliers/form.html', supplier=supplier)

@app.route('/suppliers/<int:supplier_id>/delete', methods=['POST'])
def delete_supplier(supplier_id):
    """Delete supplier"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM suppliers WHERE supplier_id=?", (supplier_id,))
        conn.commit()
        return redirect(url_for('list_suppliers'))
    except Exception as e:
        return f"Error: {str(e)}", 400
    finally:
        conn.close()

# ======================== WAREHOUSES ROUTES ========================
@app.route('/warehouses')
def list_warehouses():
    """List all warehouses"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM warehouses ORDER BY warehouse_id")
    warehouses = cursor.fetchall()
    conn.close()
    return render_template('warehouses/list.html', warehouses=warehouses)

@app.route('/warehouses/add', methods=['GET', 'POST'])
def add_warehouse():
    """Add new warehouse"""
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO warehouses (name, location, manager)
                VALUES (?, ?, ?)
            """, (
                request.form['name'],
                request.form['location'],
                request.form['manager']
            ))
            conn.commit()
            return redirect(url_for('list_warehouses'))
        except Exception as e:
            return f"Error: {str(e)}", 400
        finally:
            conn.close()
    
    return render_template('warehouses/form.html', warehouse=None)

@app.route('/warehouses/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit existing warehouse"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        try:
            cursor.execute("""
                UPDATE warehouses 
                SET name=?, location=?, manager=?
                WHERE warehouse_id=?
            """, (
                request.form['name'],
                request.form['location'],
                request.form['manager'],
                warehouse_id
            ))
            conn.commit()
            conn.close()
            return redirect(url_for('list_warehouses'))
        except Exception as e:
            conn.close()
            return f"Error: {str(e)}", 400
    
    cursor.execute("SELECT * FROM warehouses WHERE warehouse_id=?", (warehouse_id,))
    warehouse = dict_from_row(cursor.fetchone())
    conn.close()
    
    return render_template('warehouses/form.html', warehouse=warehouse)

@app.route('/warehouses/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete warehouse"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM warehouses WHERE warehouse_id=?", (warehouse_id,))
        conn.commit()
        return redirect(url_for('list_warehouses'))
    except Exception as e:
        return f"Error: {str(e)}", 400
    finally:
        conn.close()

if __name__ == '__main__':
    # Set debug=True for development, False for production
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
