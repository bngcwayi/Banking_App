import tkinter as tk
from tkinter import messagebox
import re
import datetime
import hashlib
import random
import string


class BankAccount:
    accounts = []

    def __init__(self, username, password, account_type):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.balance = 0
        self.account_type = account_type
        self.transactions = []
        BankAccount.accounts.append(self)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

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
        if amount >= 20 and amount <= self.balance:
            self.balance -= amount
            self.log_transaction("Withdrawal", amount)
            return f"Withdrew R {amount}. Current balance: R {self.balance}"
        elif amount < 20:
            return "Minimum withdrawal amount is R 20. Withdrawal denied."
        else:
            return "Insufficient funds. Withdrawal denied."

    def log_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now()
        transaction_info = f"{timestamp}: {transaction_type} of R{amount}"
        self.transactions.append(transaction_info)
        with open("transaction_log.txt", "a") as file:
            file.write(f" Transaction History for: {self.username}: \n{transaction_info}\n")


def is_valid_password(password):
    return re.match(r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]).{8,}$", password) is not None


def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    return password


class BankAppGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bug Bank Limited")
        self.master.configure(bg='light blue')

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 400
        window_height = 500
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        self.master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.label = tk.Label(master, text="Bug Bank Limited", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.button_create_account = tk.Button(master, text="Create Account", command=self.create_account, width=30)
        self.button_create_account.pack(pady=10)

        self.button_login = tk.Button(master, text="Login", command=self.login, width=30)
        self.button_login.pack(pady=10)

        self.button_deposit = tk.Button(master, text="Deposit", command=self.deposit, width=30)
        self.button_deposit.pack(pady=10)

        self.button_withdraw = tk.Button(master, text="Withdraw", command=self.withdraw, width=30)
        self.button_withdraw.pack(pady=10)

        self.button_check_balance = tk.Button(master, text="Check Balance", command=self.check_balance, width=30)
        self.button_check_balance.pack(pady=10)

        self.button_account_list = tk.Button(master, text="Account Holder List", command=self.account_list, width=30)
        self.button_account_list.pack(pady=10)

        self.button_exit = tk.Button(master, text="Exit", command=master.destroy, width=30)
        self.button_exit.pack(pady=10)

        self.forgot_frame = tk.LabelFrame(master, text="Forgot Password")
        self.forgot_frame.pack(padx=20, pady=10)

        self.forgot_username_label = tk.Label(self.forgot_frame, text="Enter Username:")
        self.forgot_username_label.grid(row=0, column=0)
        self.forgot_username = tk.Entry(self.forgot_frame)
        self.forgot_username.grid(row=0, column=1)

        self.forgot_button = tk.Button(self.forgot_frame, text="Reset Password", command=self.forgot_password)
        self.forgot_button.grid(row=1, columnspan=2, pady=5)

        self.current_account = None

    def forgot_password(self):
        username = self.forgot_username.get()
        account = BankAccount.get_account_by_username(username)

        if account:
            choice = self.show_input_dialog(
                f"Do you want to reset password with a generated password?\n\nYes/No:").lower()
            if choice == "yes":
                new_password = generate_password()
                account.password_hash = account._hash_password(new_password)
                messagebox.showinfo("Password Reset", f"Password reset successful!\nNew password: {new_password}")
            elif choice == "no":
                new_password = self.show_input_dialog(
                    "Enter your new password (at least 8 characters with 1 number, 1 capital letter, and 1 special character):")
                if not is_valid_password(new_password):
                    messagebox.showerror("Error", "Invalid password format. Please try again.")
                    return
                confirm_password = self.show_input_dialog("Confirm your new password:", password=True)
                if new_password != confirm_password:
                    messagebox.showerror("Error", "Passwords do not match. Please try again.")
                    return
                account.password_hash = account._hash_password(new_password)
                messagebox.showinfo("Password Reset", "Password reset successful!")
            else:
                messagebox.showerror("Error", "Invalid choice. Please enter 'yes' or 'no'.")
        else:
            messagebox.showerror("Error", "Username not found. Please enter a valid username.")
<<<<<<< Updated upstream
            return


        
=======
>>>>>>> Stashed changes

    def create_account(self):
        create_account_window = tk.Toplevel(self.master)
        create_account_window.title("Create Account")
        create_account_window.configure(bg='light blue',  width=30, padx=15, pady=15)

        reg_username_label = tk.Label(create_account_window, text="Username:",)
        reg_username_label.pack(pady=10)
        reg_username = tk.Entry(create_account_window)
        reg_username.pack(pady=10)

        reg_password_label = tk.Label(create_account_window, text="Password:")
        reg_password_label.pack(pady=10)
        reg_password = tk.Entry(create_account_window, show="*")
        reg_password.pack(pady=10)

        register_button = tk.Button(create_account_window, text="Register", command=lambda: self.register(reg_username.get(), reg_password.get(), create_account_window))
        register_button.pack(pady=10)

    def register(self, username, password, create_account_window):
        if username and password:
            existing_account = BankAccount.get_account_by_username(username)

            if existing_account:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            else:
                account_type = self.show_input_dialog("Choose account type (1 for Cheque, 2 for Savings):")

                if not account_type:
                    messagebox.showerror("Error", "Account type cannot be empty.")
                    create_account_window.destroy()
                    return

                if account_type == "1":
                    account = BankAccount(username, password, "Cheque")
                    messagebox.showinfo("Account Created", f"Checking account created for {username}.")
                elif account_type == "2":
                    account = BankAccount(username, password, "Savings")
                    messagebox.showinfo("Account Created", f"Savings account created for {username}.")
                else:
                    messagebox.showerror("Error", "Invalid account type choice. Please choose 1 for Cheque or 2 for Savings.")

                self.current_account = account
                create_account_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    def login(self):
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        login_window.configure(bg='light blue', width=30, padx=15, pady=15)

        login_username_label = tk.Label(login_window, text="Username:")
        login_username_label.pack(pady=5)
        login_username = tk.Entry(login_window)
        login_username.pack(pady=5)

        login_password_label = tk.Label(login_window, text="Password:")
        login_password_label.pack(pady=5)
        login_password = tk.Entry(login_window, show="*")
        login_password.pack(pady=5)

        login_button = tk.Button(login_window, text="Login", command=lambda: self.login_user(login_username.get(), login_password.get(), login_window))
        login_button.pack(pady=10)

    def login_user(self, username, password, login_window):
        if username and password:
            account = BankAccount.get_account_by_username(username)
            if account and account.password_hash == account._hash_password(password):
                messagebox.showinfo("Success", "Login Successful!")
                self.current_account = account
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    def deposit(self):
        if self.current_account:
            amount = self.show_input_dialog("Enter the deposit amount: R ")
            if amount:
                try:
                    amount = float(amount)
                    if amount > 0:
                        messagebox.showinfo("Deposit", self.current_account.deposit(amount))
                    else:
                        messagebox.showerror("Error", "Invalid amount. Please enter a positive number.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter a numerical value.")
        else:
            messagebox.showerror("Error", "Please login first.")

    def withdraw(self):
        if self.current_account:
            amount = self.show_input_dialog("Enter the withdrawal amount (minimum R 20): R ")
            if amount:
                try:
                    amount = float(amount)
                    if amount > 0:
                        messagebox.showinfo("Withdrawal", self.current_account.withdraw(amount))
                    else:
                        messagebox.showerror("Error", "Invalid amount. Please enter a positive number.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter a numerical value.")
        else:
            messagebox.showerror("Error", "Please login first.")

    def check_balance(self):
        if self.current_account:
            messagebox.showinfo("Balance", self.current_account.check_balance())
        else:
            messagebox.showerror("Error", "Please login first.")

    def account_list(self):
        top = tk.Toplevel(self.master)
        top.title("Account Holder List")
        account_info = "\nAccount Holder List:\n"
        for acc in BankAccount.accounts:
            account_info += f"Username: {acc.username}, Account Type: {acc.account_type}, \nBalance: R {acc.balance}\n"
        label_account_list = tk.Label(top, text=account_info)
        label_account_list.pack(padx=10, pady=10)
        button_close = tk.Button(top, text="Close", command=top.destroy)
        button_close.pack(pady=10)
        window_width = label_account_list.winfo_reqwidth() + 20
        window_height = label_account_list.winfo_reqheight() + button_close.winfo_reqheight() + 60
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        top.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def show_input_dialog(self, prompt, password=False):
        top = tk.Toplevel(self.master)
        top.title("Dialog")
        top.configure(bg='light blue')
        label = tk.Label(top, text=prompt)
        label.pack(pady=10)
        var = tk.StringVar()
        entry = tk.Entry(top, textvariable=var, show='*' if password else '')
        entry.pack(pady=10)

        def ok():
            if var.get():
                top.destroy()
            else:
                messagebox.showerror("Error", "Input cannot be empty.")
                top.lift()

        button_ok = tk.Button(top, text="OK", command=ok)
        button_ok.pack(pady=10)
        window_width = max(label.winfo_reqwidth(), entry.winfo_reqwidth()) + 40
        window_height = label.winfo_reqheight() + entry.winfo_reqheight() + button_ok.winfo_reqheight() + 60
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        top.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.master.wait_window(top)
        return var.get()


def main():
    root = tk.Tk()
    app = BankAppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
