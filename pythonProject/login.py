import tkinter as tk
from tkinter import messagebox
from bankingapp1 import BankAppGUI, BankAccount, generate_password

def register():
    username = reg_username.get()
    password = reg_password.get()

    if username and password:
        # Save username and password (for example, in a database or file)
        # Here, for simplicity, I'll create an instance of BankAccount
        account = BankAccount(username, password, "Savings")
        messagebox.showinfo("Success", "Registration Successful!\nYou can now login.")
    else:
        messagebox.showerror("Error", "Please enter both username and password.")

def login():
    username = login_username.get()
    password = login_password.get()

    if username and password:
        # Check username and password (compare with stored data)
        account = BankAccount.get_account_by_username(username)
        if account and account.password_hash == account._hash_password(password):
            messagebox.showinfo("Success", "Login Successful!")
            open_bank_app(account)  # Open the banking app if login is successful
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    else:
        messagebox.showerror("Error", "Please enter both username and password.")

def open_bank_app(account):
    root.destroy()  # Close the login/register window
    root_bank = tk.Tk()
    app = BankAppGUI(root_bank)
    root_bank.mainloop()

def forgot_password():
    username = forgot_username.get()

    if username:
        # Implement logic to reset the password (for example, send a reset link to the user's email)
        messagebox.showinfo("Success", f"Password reset link sent to {username}'s email!")
    else:
        messagebox.showerror("Error", "Please enter your username.")

# Create main window
root = tk.Tk()
root.title("Login/Register")

# Register frame
register_frame = tk.LabelFrame(root, text="Register")
register_frame.pack(padx=20, pady=10)

reg_username_label = tk.Label(register_frame, text="Username:")
reg_username_label.grid(row=0, column=0)
reg_username = tk.Entry(register_frame)
reg_username.grid(row=0, column=1)

reg_password_label = tk.Label(register_frame, text="Password:")
reg_password_label.grid(row=1, column=0)
reg_password = tk.Entry(register_frame, show="*")
reg_password.grid(row=1, column=1)

register_button = tk.Button(register_frame, text="Register", command=register)
register_button.grid(row=2, columnspan=2, pady=5)

# Login frame
login_frame = tk.LabelFrame(root, text="Login")
login_frame.pack(padx=20, pady=10)

login_username_label = tk.Label(login_frame, text="Username:")
login_username_label.grid(row=0, column=0)
login_username = tk.Entry(login_frame)
login_username.grid(row=0, column=1)

login_password_label = tk.Label(login_frame, text="Password:")
login_password_label.grid(row=1, column=0)
login_password = tk.Entry(login_frame, show="*")
login_password.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, columnspan=2, pady=5)

# Forgot Password frame
forgot_frame = tk.LabelFrame(root, text="Forgot Password")
forgot_frame.pack(padx=20, pady=10)

forgot_username_label = tk.Label(forgot_frame, text="Enter Username:")
forgot_username_label.grid(row=0, column=0)
forgot_username = tk.Entry(forgot_frame)
forgot_username.grid(row=0, column=1)

forgot_button = tk.Button(forgot_frame, text="Reset Password", command=forgot_password)
forgot_button.grid(row=1, columnspan=2, pady=5)

root.mainloop()
