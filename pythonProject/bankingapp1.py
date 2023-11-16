import PIL
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import datetime
import hashlib
import random
import string
import pyperclip  # Import the pyperclip library
class BankAccount:
    accounts = []
    def __init__(self, username, password, account_type):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.balance = 0
        self.account_type = account_type
        self.transactions = []
        BankAccount.accounts.append(self)
        self._write_to_file(username, self.password_hash)
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    def _write_to_file(self, username, password_hash):
        with open("bank_data.txt", "a") as file:
            file.write(f"{username}:{password_hash}\n")
    @classmethod
    def get_account_by_username(cls, username):
        for account in cls.accounts:
            if account.username == username:
                return account
        return None
    def check_balance(self):
        return f"Current balance: R {self.balance}"
    def deposit(self, amount):
        self.balance += amount
        self.log_transaction("Deposit", amount)
        return f"Deposited R {amount}. \nCurrent balance: R {self.balance}"
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.log_transaction("Withdrawal", amount)
            return f"Withdrew R {amount}. Current balance: R {self.balance}"
        else:
            return "Insufficient funds. Withdrawal denied."
    def log_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now()
        transaction_info = f"{timestamp}: {transaction_type} of R{amount}"
        self.transactions.append(transaction_info)
        with open("transaction_log.txt", "a") as file:
            file.write(
                f" Transaction History for: {self.username}: \n{transaction_info}\n"
            )
def is_valid_password(password):
    return re.match(
        r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]).{8,}$", password
    ) is not None
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(12))
    return password
class BankAppGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bug Bank Limited")
        # Load the image and resize it
        welcome_image = Image.open("bugbank.png")
        welcome_image = welcome_image.resize((200, 200), PIL.Image.Resampling.LANCZOS)
        welcome_image = ImageTk.PhotoImage(welcome_image)
        # Create a label to display the resized image
        self.image_label = tk.Label(master, image=welcome_image)
        self.image_label.image = welcome_image  # Keep a reference to avoid garbage collection
        self.image_label.pack(pady=10)
        self.label = tk.Label(master, text="Bug Bank Limited", font=("Helvetica Bold", 16))
        self.label.pack(pady=10)
        self.button_create_account = tk.Button(
            master, text="Create Account", command=self.create_account, bg="green", fg="white", width="20"
        )
        self.button_create_account.pack(pady=5)
        self.button_login = tk.Button(master, text="Login", command=self.login, bg="green", fg="white", width="20")
        self.button_login.pack(pady=5)
        self.button_deposit = tk.Button(
            master, text="Deposit", command=self.deposit, width=18, bg="teal", fg="black"
        )
        self.button_deposit.pack(pady=5)
        self.button_withdraw = tk.Button(
            master, text="Withdraw", command=self.withdraw, width=18, bg="teal", fg="black"
        )
        self.button_withdraw.pack(pady=5)
        self.button_check_balance = tk.Button(
            master, text="Check Balance", command=self.check_balance, bg="teal", fg="black", width="18"
        )
        self.button_check_balance.pack(pady=5)
        self.button_show_transactions = tk.Button(
            master, text="Show Transactions", command=self.show_transactions, bg="teal", fg="black", width="18"
        )
        self.button_show_transactions.pack(pady=5)
        self.button_account_list = tk.Button(
            master, text="Account Holder List", command=self.account_list, bg="teal", fg="black", width="18"
        )
        self.button_account_list.pack(pady=5)
        self.button_forgot_password = tk.Button(
            master, text="Forgot Password?", command=self.forgot_password, bg="orange", fg="black", width="15"
        )
        self.button_forgot_password.pack(pady=5)
        self.button_exit = tk.Button(master, text="Exit", command=self.exit_program, bg="red", fg="white", width="15")
        self.button_exit.pack(pady=5)
        self.current_account = None
    def toggle_eye(self, entry):
        current_show_state = entry.cget("show")
        entry.config(show="" if current_show_state == "*" else "")
    def create_account(self):
        username = self.show_input_dialog("Enter your username:")
        generated_password = generate_password()
        print(f"Generated password: {generated_password}")
        choice = self.show_input_dialog(
            "Do you want to use the generated password? (yes/no):"
        ).lower()
        if choice == "yes":
            password = generated_password
        elif choice == "no":
            password = self.show_input_dialog(
                "Enter your password (at least 8 characters with 1 number, 1 capital letter, and 1 special character):"
            )
            if not is_valid_password(password):
                messagebox.showerror(
                    "Error", "Invalid password format. Please try again."
                )
                return
            confirm_password = self.show_input_dialog(
                "Confirm your password:", password=True
            )
            if password != confirm_password:
                messagebox.showerror(
                    "Error", "Passwords do not match. Please try again."
                )
                return
        else:
            messagebox.showerror(
                "Error", "Invalid choice. Please enter 'yes' or 'no'."
            )
            return
        existing_account = BankAccount.get_account_by_username(username)
        if existing_account:
            messagebox.showerror(
                "Error", "Username already exists. Please choose a different username."
            )
        else:
            account_type = self.show_input_dialog(
                "Choose account type (1 for Cheque, 2 for Savings):"
            )
            if account_type == "1":
                account = BankAccount(username, password, "Cheque")
                messagebox.showinfo(
                    "Account Created", f"Checking account created for {username}."
                )
                self.current_account = account
            elif account_type == "2":
                account = BankAccount(username, password, "Savings")
                messagebox.showinfo(
                    "Account Created", f"Savings account created for {username}."
                )
                self.current_account = account
            else:
                messagebox.showerror(
                    "Error",
                    "Invalid account type choice. Please choose 1 for Cheque or 2 for Savings.",
                )
    def login(self):
        username = self.show_input_dialog("Enter your username:")
        password = self.show_input_dialog("Enter your password:", password=True)
        account = BankAccount.get_account_by_username(username)
        if account and account.password_hash == hashlib.sha256(
            password.encode()
        ).hexdigest():
            messagebox.showinfo("Login Successful", f"Welcome back, {username}.")
            self.current_account = account
        else:
            messagebox.showerror(
                "Error", "Invalid username or password. Login failed."
            )
    def deposit(self):
        if self.current_account:
            amount = self.show_num_keypad("Enter the deposit amount:")
            try:
                amount = float(amount)
                if amount > 0:
                    messagebox.showinfo(
                        "Success", self.current_account.deposit(amount)
                    )
                else:
                    messagebox.showerror(
                        "Error", "Invalid amount. Please enter a positive number."
                    )
            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid input. Please enter a numerical value."
                )
        else:
            messagebox.showerror("Error", "Please login first.")
    def withdraw(self):
        if self.current_account:
            amount = self.show_num_keypad("Enter the withdrawal amount:")
            try:
                amount = float(amount)
                if amount > 0:
                    messagebox.showinfo(
                        "Success", self.current_account.withdraw(amount)
                    )
                else:
                    messagebox.showerror(
                        "Error", "Invalid amount. Please enter a positive number."
                    )
            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid input. Please enter a numerical value."
                )
        else:
            messagebox.showerror("Error", "Please login first.")
    def check_balance(self):
        if self.current_account:
            messagebox.showinfo("Balance", self.current_account.check_balance())
        else:
            messagebox.showerror("Error", "Please login first.")
    def show_transactions(self):
        if self.current_account:
            transactions_text = "\nTransaction History:\n"
            for transaction in self.current_account.transactions:
                transactions_text += f"{transaction}\n"
            messagebox.showinfo(
                "Transaction History", f"Transaction History for {self.current_account.username}:\n{transactions_text}"
            )
        else:
            messagebox.showerror("Error", "Please login first.")
    def account_list(self):
        print("\nAccount Holder List:")
        for acc in BankAccount.accounts:
            print(
                f"Username: {acc.username}, Account Type: {acc.account_type}, \nBalance: R {acc.balance}"
            )
    def forgot_password(self):
        username = self.show_input_dialog("Enter your username:")
        account = BankAccount.get_account_by_username(username)
        if account:
            choice = self.show_input_dialog(
                "Do you want to use a generated password? (yes/no):"
            ).lower()
            if choice == "yes":
                new_password = generate_password()
            elif choice == "no":
                new_password = self.show_input_dialog(
                    "Enter your new password (at least 8 characters with 1 number, 1 capital letter, and 1 special character):",
                    password=True
                )
                if not is_valid_password(new_password):
                    messagebox.showerror(
                        "Error", "Invalid password format. Please try again."
                    )
                    return
                confirm_password = self.show_input_dialog(
                    "Confirm your new password:", password=True
                )
                if new_password != confirm_password:
                    messagebox.showerror(
                        "Error", "Passwords do not match. Please try again."
                    )
                    return
            else:
                messagebox.showerror(
                    "Error", "Invalid choice. Please enter 'yes' or 'no'."
                )
                return
            account.password_hash = account._hash_password(new_password)
            messagebox.showinfo("Password Reset", f"Your new password is: {new_password}")
            # Copy the new password to the clipboard
            pyperclip.copy(new_password)
            messagebox.showinfo("Password Copied", "Your new password has been copied to the clipboard.")
        else:
            messagebox.showerror(
                "Error", "Username not found. Please enter a valid username."
            )
    def show_input_dialog(self, prompt, password=False):  # show and hide password
        top = tk.Toplevel(self.master)
        label = tk.Label(top, text=prompt)
        label.pack(pady=10)
        var = tk.StringVar()
        entry = tk.Entry(top, textvariable=var, show="*" if password else "")
        entry.pack(pady=10)
        if password:
            eye_button = tk.Button(
                top,
                text="👁",
                command=lambda: self.toggle_eye(entry),
            )
            eye_button.pack(pady=5)
        def ok():
            value = var.get()
            if not value:
                messagebox.showerror("Error", "Please enter a value.")
            else:
                top.destroy()
        button_ok = tk.Button(top, text="OK", command=ok)
        button_ok.pack(pady=10)
        def on_closing():
            messagebox.showinfo("Transaction Cancelled", "Transaction Cancelled")
            top.destroy()
        top.protocol("WM_DELETE_WINDOW", on_closing)
        self.master.wait_window(top)
        return var.get()
    def show_num_keypad(self, prompt):
        top = tk.Toplevel(self.master)
        top.title(prompt)
        var = tk.StringVar()
        entry = tk.Entry(
            top, textvariable=var, justify="right", font=("Helvetica Bold", 16)
        )
        entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        buttons = [
            "7", "8", "9",
            "4", "5", "6",
            "1", "2", "3",
            "0", ".", "<"
        ]
        row_val = 1
        col_val = 0
        for button in buttons:
            tk.Button(
                top,
                text=button,
                width=5,
                height=2,
                command=lambda b=button: self.num_button_click(var, entry, b),
            ).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 2:
                col_val = 0
                row_val += 1
        clear_button = tk.Button(
            top, text="Clear", command=lambda: self.clear_entry(entry), width=5, height=2
        )
        clear_button.grid(row=row_val, column=0, columnspan=2, padx=5, pady=5)
        def on_cancel():
            nonlocal result
            result = None  # Set result to None when Cancel is clicked
            top.destroy()
        button_cancel = tk.Button(
            top, text="Cancel", command=on_cancel, width=5, height=2
        )
        button_cancel.grid(row=row_val + 1, column=2, padx=5, pady=5)
        result = None
        def on_ok():
            nonlocal result
            try:
                result = float(var.get())
                top.destroy()
            except ValueError:
                result = None  # Set result to None if conversion to float fails
                top.destroy()
        button_ok = tk.Button(
            top, text="OK", command=on_ok, width=5, height=2
        )
        button_ok.grid(row=row_val, column=2, padx=5, pady=5)
        def on_closing():
            nonlocal result
            result = None  # Set result to None when window is closed
            top.destroy()
        top.protocol("WM_DELETE_WINDOW", on_closing)
        top.wait_window(top)
        # Check if the user clicked the "OK" button and entered a valid numerical value
        return result
    def num_button_click(self, var, entry, button): # step indexing removing last value from the list.
        current_value = var.get()
        if button == "<":
            new_value = current_value[:-1]
        else:
            new_value = current_value + button
        var.set(new_value)
        entry.icursor(tk.END)  # Move cursor to the end of the entry
    def clear_entry(self, entry): # returns value entered, to the default, which is zero.
        entry.delete(0, tk.END)
    def exit_program(self):
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            messagebox.showinfo("Exit", "Thank you for using Bug Bank Limited. Goodbye!")
            self.master.destroy()
def main():
    root = tk.Tk()
    app = BankAppGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()