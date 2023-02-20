from tkinter import ttk
from tkinter import *
import sqlite3

class Medicine:

    db_name = "database.db"

    def __init__(self, window):
        self.window = window
        self.window.title("Anaid Pharmacy")

        # Creating a Frame Container
        frame= LabelFrame(self.window, text="Register a new Product")
        frame.grid(row=0, column=0, columnspan=3, pady=10)

        # Inputs
        Label(frame, text="Product: ").grid(row=1, column=0)
        self.product = Entry(frame)
        self.product.grid(row=1, column=1)
        Label(frame, text="Pack: ").grid(row=2, column=0)
        self.pack = Entry(frame)
        self.pack.grid(row=2, column=1)
        Label(frame, text="Amount: ").grid(row=3, column=0)
        self.amount = Entry(frame)
        self.amount.grid(row=3, column=1)

        # Buttons 
        ttk.Button(frame, text="Save Product", command=self.add_product).grid(row=4, columnspan=2, sticky=W+E)
        ttk.Button(text="DELETE", command=self.delete_product).grid(row=6, column=0, sticky=W+E)
        ttk.Button(text="EDIT", command=self.edit_product).grid(row=6, column=1, sticky=W+E)

        # Output Messages
        self.message = Label(text="", fg="red")
        self.message.grid(row=4, column=0, columnspan=2, sticky=W+E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=("Product", "Pack", "Amount"), show="headings")
        self.tree.grid(row=5, column=0, columnspan=2)
        self.tree.heading("#1", text="Product", anchor=CENTER)
        self.tree.heading("#2", text="Pack", anchor=CENTER)
        self.tree.heading("#3", text="Amount", anchor=CENTER)

        self.get_products()

    
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    
    def get_products(self):
        #cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #quering data 
        query = "SELECT * FROM medicine ORDER BY product DESC"
        db_rows = self.run_query(query)
        #filling data 
        for row in db_rows:            
            self.tree.insert("", 0, values=row[1:])
    
    
    def validation(self):
        return len(self.product.get()) != 0 and len(self.pack.get()) != 0 and len(self.amount.get()) != 0

 
    def add_product(self):
        if self.validation():
            query = "INSERT INTO medicine VALUES(NULL, ?, ?, ?)"
            parameters = (self.product.get(), self.pack.get(), self.amount.get())
            self.run_query(query, parameters)
            self.message["text"] = f"Product {self.product.get()} added Successfully"   
            self.product.delete(0, END) 
            self.pack.delete(0, END)
            self.amount.delete(0, END)   
        else:
            self.message["text"] = "Product, Pack and Amount are required"

        self.get_products()

    
    def delete_product(self):
        try:
            self.tree.item(self.tree.selection())["values"][0]
        except IndexError as e:
            self.message["text"] = "Please Select a Record"
            return
        
        name = self.tree.item(self.tree.selection())["values"][0]       
        query = "DELETE FROM medicine WHERE product = ?"
        self.run_query(query, parameters=(name, ))
        self.message["text"] = f"Record {name} Deleted Successfully"
        self.get_products()

    def edit_product(self):
        self.message["text"]=""
        try:
            self.tree.item(self.tree.selection())["values"][0]
        except IndexError as e:
            self.message["text"] = "Please Select a Record"
            return
        name = self.tree.item(self.tree.selection())["values"][0]  
        old_pack = self.tree.item(self.tree.selection())["values"][1]
        old_amount= self.tree.item(self.tree.selection())["values"][2]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Edit Product"

        #Old product name
        Label(self.edit_wind, text="Old Product Name: ").grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state="readonly").grid(row=0, column=2)

        #New product name
        Label(self.edit_wind, text="New Product Name: ").grid(row=1, column=1)
        new_product=Entry(self.edit_wind)
        new_product.grid(row=1, column=2)

        #Old pack
        Label(self.edit_wind, text="Old Pack: ").grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_pack), state="readonly").grid(row=2, column=2)

        #New pack
        Label(self.edit_wind, text="New Pack: ").grid(row=3, column=1)
        new_pack=Entry(self.edit_wind)
        new_pack.grid(row=3, column=2)

        #Old amount
        Label(self.edit_wind, text="Old Amount: ").grid(row=4, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_amount), state="readonly").grid(row=4, column=2)

        #New amount  
        Label(self.edit_wind, text="New Amount: ").grid(row=5, column=1)
        new_amount=Entry(self.edit_wind)
        new_amount.grid(row=5, column=2)

        ttk.Button(self.edit_wind, text="Update", command=lambda: self.edit_records(new_product.get(), 
        name, new_pack.get(), old_pack, new_amount.get(), old_amount)).grid(row=6, column=2, sticky=W)
    
    def edit_records(self, new_product, name, new_pack, old_pack, new_amount, old_amount):
        query = "UPDATE medicine SET product = ?, pack = ?, amount = ? WHERE product = ? AND pack = ? AND amount = ?"
        parameters = (new_product, new_pack, new_amount, name, old_pack, old_amount)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message["text"] = f"Record {name} Update Successfully"
        self.get_products()
           


if __name__ == "__main__":
    window = Tk()
    application = Medicine(window)
    window.mainloop()