import tkinter as tk
from tkinter import messagebox
import sqlite3

class BankManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")

        # Connect to the database
        self.conn = sqlite3.connect("bank_management.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Variables
        self.account_number = tk.StringVar()
        self.name = tk.StringVar()
        self.balance = tk.StringVar()

        # UI Elements
        tk.Label(root, text="Account Number").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.account_number).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.name).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Balance").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.balance).grid(row=2, column=1, padx=10, pady=10)

        tk.Button(root, text="Add Account", command=self.add_account).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(root, text="View Accounts", command=self.view_accounts).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(root, text="Delete Account", command=self.delete_account).grid(row=3, column=2, padx=10, pady=10)

        self.accounts_listbox = tk.Listbox(root)
        self.accounts_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS accounts
               (account_number TEXT PRIMARY KEY, name TEXT, balance REAL)'''
        )
        self.conn.commit()

    def add_account(self):
        account_number = self.account_number.get()
        name = self.name.get()
        balance = self.balance.get()

        if account_number and name and balance:
            try:
                self.cursor.execute(
                    "INSERT INTO accounts (account_number, name, balance) VALUES (?, ?, ?)",
                    (account_number, name, balance)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Account added successfully")
                self.clear_entries()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Account number already exists")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def view_accounts(self):
        self.accounts_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM accounts")
        accounts = self.cursor.fetchall()
        for account in accounts:
            self.accounts_listbox.insert(tk.END, account)

    def delete_account(self):
        selected_account = self.accounts_listbox.get(tk.ACTIVE)
        if selected_account:
            self.cursor.execute("DELETE FROM accounts WHERE account_number = ?", (selected_account[0],))
            self.conn.commit()
            messagebox.showinfo("Success", "Account deleted successfully")
            self.view_accounts()

    def clear_entries(self):
        self.account_number.set("")
        self.name.set("")
        self.balance.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankManagementApp(root)
    root.mainloop()
