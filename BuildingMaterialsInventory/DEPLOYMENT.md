# Deployment Guide for PythonAnywhere

This guide walks you through deploying the Building Materials Inventory System to PythonAnywhere.

## Prerequisites

- PythonAnywhere account (free or paid)
- Internet connection
- Local copy of the project files

## Step-by-Step Deployment

### Step 1: Upload Project Files to PythonAnywhere

1. **Log in to PythonAnywhere** — https://www.pythonanywhere.com/
2. **Go to the Files tab** — Click on "Files" in the top menu
3. **Create a new folder** for your project:
   - Create directory: `/home/your_username/building_materials_inventory`
4. **Upload all project files** into this folder using the web interface or bash:

```bash
# Alternative: Use bash to clone/download
cd /home/your_username/
mkdir -p building_materials_inventory
cd building_materials_inventory
# Then upload files via web interface or use SCP
```

Files to upload:
- `app.py`
- `wsgi.py`
- `init_db.py`
- `requirements.txt`
- `README.md`
- `DEPLOYMENT.md`
- `templates/` (entire folder with subfolders)

### Step 2: Create Virtual Environment

1. **Open Bash Console** in PythonAnywhere:
   - Go to Consoles > New console > Bash

2. **Create and activate virtual environment:**

```bash
cd /home/your_username/building_materials_inventory
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Initialize database:**

```bash
python init_db.py
```

You should see:
```
✓ Database initialized successfully with mock data!
```

### Step 3: Create Web App

1. **Go to Web tab** in PythonAnywhere
2. **Click "Add a new web app"**
3. **Select domain** — Choose your PythonAnywhere domain (e.g., `username.pythonanywhere.com`)
4. **Choose Python version** — Select Python 3.X (3.9 or higher)
5. **Select "Flask"** as the framework
6. **Specify source code directory:**
   - Enter: `/home/your_username/building_materials_inventory`

### Step 4: Configure WSGI File

1. **In Web tab**, find your web app
2. **Click on "WSGI configuration file"** link
3. **Replace the entire content** with:

```python
"""
WSGI configuration for Building Materials Inventory
"""
import sys
import os

# Add project to path
path = '/home/your_username/building_materials_inventory'
if path not in sys.path:
    sys.path.insert(0, path)

# Activate virtual environment
activate_this = '/home/your_username/building_materials_inventory/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Flask app
from app import app as application
application.config['DEBUG'] = False
```

4. **Save the file**

### Step 5: Configure Virtualenv

1. **In Web tab**, under "Virtualenv section"
2. **Enter the path:**
```
/home/your_username/building_materials_inventory/venv
```
3. **Save**

### Step 6: Reload Web App

1. **In Web tab**, click the green "Reload" button
2. **Wait a few seconds** for the app to restart
3. **Check for errors** in the "Log files" section

### Step 7: Access Your App

Visit your web app at:
```
https://username.pythonanywhere.com
```

You should see the Building Materials Inventory dashboard!

## Troubleshooting

### Issue: 502 Bad Gateway

**Solution:**
- Check Web tab logs for errors
- Ensure virtualenv path is correct
- Verify WSGI file has correct imports
- Check that Flask app starts locally (`python app.py`)

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
- Activate virtualenv: `source venv/bin/activate`
- Reinstall requirements: `pip install -r requirements.txt`
- Reload web app in PythonAnywhere

### Issue: Database file not found (500 error)

**Solution:**
- Run `python init_db.py` again from bash console
- Ensure file permissions: `chmod 755 inventory.db`
- Check that database path in `app.py` matches working directory

### Issue: Static files or templates not loading

**Solution:**
- Ensure correct directory structure:
```
building_materials_inventory/
  ├── app.py
  ├── wsgi.py
  ├── inventory.db
  ├── templates/
  │   ├── base.html
  │   ├── index.html
  │   ├── products/
  │   ├── suppliers/
  │   └── warehouses/
```
- Reload web app after verifying structure

## Performance Notes

- **Real-time Dashboard**: Uses AJAX polling (10 seconds) — PythonAnywhere compatible
- **Database**: SQLite is fine for small deployments (< 1000 daily users)
- **For larger scale**: Consider upgrading to PostgreSQL

## Monitoring

1. **Check logs** regularly — Web tab > Log files
2. **Monitor server response** — Check CPU/Memory in dashboards
3. **Watch error logs** if users report issues

## Backup

PythonAnywhere includes backups, but for important data:

```bash
# Download database locally from bash console
# Or backup via Files interface
```

## Custom Domain

To use a custom domain (paid account):
1. Go to Web tab > Custom domains
2. Follow PythonAnywhere's DNS setup instructions

## Security Notes

- `DEBUG = False` is set in `wsgi.py` for production
- Consider adding HTTPS redirect (PythonAnywhere supports HTTPS free)
- Regularly update dependencies: `pip list --outdated`

## Support

For PythonAnywhere-specific issues, visit:
- https://www.pythonanywhere.com/help/

For application issues, check:
- Flask documentation: https://flask.palletsprojects.com/
- SQLite documentation: https://www.sqlite.org/docs.html
