import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_widgets()
        
        # Load initial data
        self.load_data()
    
    def init_database(self):
        """Initialize SQLite database and create table if not exists"""
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                supplier TEXT,
                last_updated TEXT
            )
        ''')
        self.conn.commit()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Title
        title_label = tk.Label(self.root, text="Inventory Management System", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left frame - Input form
        left_frame = tk.LabelFrame(main_frame, text="Item Details", font=('Arial', 10, 'bold'),
                                  bg='#f0f0f0', padx=10, pady=10)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Input fields
        fields = [
            ("Name:", "name"),
            ("Category:", "category"),
            ("Quantity:", "quantity"),
            ("Price:", "price"),
            ("Supplier:", "supplier")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(left_frame, text=label, bg='#f0f0f0', anchor='w').grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(left_frame, width=25)
            entry.grid(row=i, column=1, pady=5, padx=(5, 0))
            self.entries[field] = entry
        
        # Buttons frame
        button_frame = tk.Frame(left_frame, bg='#f0f0f0')
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)
        
        # Buttons
        tk.Button(button_frame, text="Add Item", command=self.add_item, 
                 bg='#4CAF50', fg='white', width=12).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Item", command=self.update_item,
                 bg='#2196F3', fg='white', width=12).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Item", command=self.delete_item,
                 bg='#f44336', fg='white', width=12).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Clear", command=self.clear_entries,
                 bg='#FF9800', fg='white', width=12).grid(row=1, column=1, padx=5, pady=5)
        
        # Right frame - Data display
        right_frame = tk.LabelFrame(main_frame, text="Inventory Items", font=('Arial', 10, 'bold'),
                                   bg='#f0f0f0', padx=10, pady=10)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Search frame
        search_frame = tk.Frame(right_frame, bg='#f0f0f0')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left')
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_items)
        
        # Treeview for data display
        columns = ('ID', 'Name', 'Category', 'Quantity', 'Price', 'Supplier', 'Last Updated')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief='sunken', 
                             anchor='w', bg='#f0f0f0')
        status_bar.pack(side='bottom', fill='x')
    
    def load_data(self):
        """Load data from database into treeview"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            self.cursor.execute("SELECT * FROM inventory ORDER BY name")
            rows = self.cursor.fetchall()
            
            for row in rows:
                # Format price with 2 decimal places
                formatted_row = list(row)
                formatted_row[4] = f"${row[4]:.2f}"  # Format price
                self.tree.insert('', 'end', values=formatted_row)
            
            self.status_var.set(f"Loaded {len(rows)} items")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load data: {str(e)}")
    
    def add_item(self):
        """Add new item to inventory"""
        try:
            # Get data from entries
            name = self.entries['name'].get().strip()
            category = self.entries['category'].get().strip()
            quantity = self.entries['quantity'].get().strip()
            price = self.entries['price'].get().strip()
            supplier = self.entries['supplier'].get().strip()
            
            # Validate required fields
            if not name or not category or not quantity or not price:
                messagebox.showwarning("Input Error", "Please fill in all required fields")
                return
            
            # Validate numeric fields
            try:
                quantity = int(quantity)
                price = float(price)
                if quantity < 0 or price < 0:
                    raise ValueError("Negative values not allowed")
            except ValueError:
                messagebox.showwarning("Input Error", "Quantity must be integer and Price must be numeric")
                return
            
            # Insert into database
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''
                INSERT INTO inventory (name, category, quantity, price, supplier, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, category, quantity, price, supplier, current_time))
            
            self.conn.commit()
            self.load_data()
            self.clear_entries()
            self.status_var.set("Item added successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add item: {str(e)}")
    
    def update_item(self):
        """Update selected item"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an item to update")
            return
        
        try:
            item_id = self.tree.item(selected[0])['values'][0]
            
            # Get data from entries
            name = self.entries['name'].get().strip()
            category = self.entries['category'].get().strip()
            quantity = self.entries['quantity'].get().strip()
            price = self.entries['price'].get().strip()
            supplier = self.entries['supplier'].get().strip()
            
            # Validate required fields
            if not name or not category or not quantity or not price:
                messagebox.showwarning("Input Error", "Please fill in all required fields")
                return
            
            # Validate numeric fields
            try:
                quantity = int(quantity)
                price = float(price)
                if quantity < 0 or price < 0:
                    raise ValueError("Negative values not allowed")
            except ValueError:
                messagebox.showwarning("Input Error", "Quantity must be integer and Price must be numeric")
                return
            
            # Update database
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''
                UPDATE inventory 
                SET name=?, category=?, quantity=?, price=?, supplier=?, last_updated=?
                WHERE id=?
            ''', (name, category, quantity, price, supplier, current_time, item_id))
            
            self.conn.commit()
            self.load_data()
            self.clear_entries()
            self.status_var.set("Item updated successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update item: {str(e)}")
    
    def delete_item(self):
        """Delete selected item"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an item to delete")
            return
        
        item_name = self.tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?"):
            try:
                item_id = self.tree.item(selected[0])['values'][0]
                self.cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
                self.conn.commit()
                self.load_data()
                self.clear_entries()
                self.status_var.set("Item deleted successfully")
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete item: {str(e)}")
    
    def on_item_select(self, event):
        """Populate form fields when item is selected"""
        selected = self.tree.selection()
        if not selected:
            return
        
        item_values = self.tree.item(selected[0])['values']
        
        # Clear entries first
        self.clear_entries()
        
        # Populate entries with selected item data
        self.entries['name'].insert(0, item_values[1])
        self.entries['category'].insert(0, item_values[2])
        self.entries['quantity'].insert(0, str(item_values[3]))
        
        # Remove dollar sign from price for editing
        price_str = str(item_values[4]).replace('$', '')
        self.entries['price'].insert(0, price_str)
        
        self.entries['supplier'].insert(0, item_values[5] if item_values[5] else "")
    
    def clear_entries(self):
        """Clear all input fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def search_items(self, event=None):
        """Search items based on search term"""
        search_term = self.search_var.get().strip()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if search_term:
                self.cursor.execute('''
                    SELECT * FROM inventory 
                    WHERE name LIKE ? OR category LIKE ? OR supplier LIKE ?
                    ORDER BY name
                ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            else:
                self.cursor.execute("SELECT * FROM inventory ORDER BY name")
            
            rows = self.cursor.fetchall()
            
            for row in rows:
                formatted_row = list(row)
                formatted_row[4] = f"${row[4]:.2f}"
                self.tree.insert('', 'end', values=formatted_row)
            
            self.status_var.set(f"Found {len(rows)} items")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Search failed: {str(e)}")
    
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
