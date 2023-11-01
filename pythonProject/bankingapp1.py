import re
import datetime # shows timestamps and date for transactions.
import hashlib # it masks the user's password, into hash characters.

# this class stores the user bank account info
class BankAccount:
    accounts = []

    def __init__(self, username, password, account_type):
        self.username = username
        self.password_hash = self._hash_password(password) # password input masker.
        self.balance = 0
        self.account_type = account_type
        self.transactions = []
        BankAccount.accounts.append(self)
        self._write_to_file(username, self.password_hash)


    def _hash_password(self, password):
        # Use hashlib to securely hash the password
        return hashlib.sha256(password.encode()).hexdigest()

# takes user's username and password, and records into the txt file.
    def _write_to_file(self, username, password_hash):
        with open("bank_data.txt", "a") as file:
            file.write(f"{username}:{password_hash}\n")

# check for user account
    @classmethod
    def get_account_by_username(cls, username):
        for account in cls.accounts:
            if account.username == username:
                return account
        return None

# check user account balance
    def check_balance(self):
        return f"Current balance: R {self.balance}"

# to deposit money in user account and also record the transaction
    def deposit(self, amount):
        self.balance += amount
        self.log_transaction("Deposit", amount)
        return f"Deposited R {amount}. \nCurrent balance: R {self.balance}"

# to withdraw money from user account and also record the transaction
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.log_transaction("Withdrawal", amount)
            return f"Withdrew R {amount}. Current balance: R {self.balance}"
        else:
            return "Insufficient funds. Withdrawal denied."

# this logs the user transaction with the timestamp to the transaction_log.txt file
    def log_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now()
        transaction_info = f"{timestamp}: {transaction_type} of R{amount}"
        self.transactions.append(transaction_info)
        with open("transaction_log.txt", "a") as file:
            file.write(f"{self.username}: \n{transaction_info}\n")

# regular expressions for password validation
def is_valid_password(password):
    return re.match(r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]).{8,}$", password) is not None

# welcoming message and request username input
def create_account():
    print("++++++++++++++++++++")
    print("Welcome to BugBank!")
    print("++++++++++++++++++++")
    username = input("Enter your username: ")

# checks for password validation, if a username already exists, whether user selects cheque(1) or savings(2) account
    # if user enters the wrong required input, it will catch an error.
    while True:
        password = input("Enter your password (at least 8 characters with 1 number, 1 capital letter, and 1 special character): ")
        if is_valid_password(password):
            existing_account = BankAccount.get_account_by_username(username)
            if existing_account:
                print("Username already exists. Please choose a different username.")
            else:
                account_type = input("Choose account type (1 for Cheque, 2 for Savings): ")
                if account_type == "1":
                    account = BankAccount(username, password, "Cheque")
                    print(f"Checking account created for {username}.")
                    return account
                elif account_type == "2":
                    account = BankAccount(username, password, "Savings")
                    print(f"Savings account created for {username}.")
                    return account
                else:
                    print("Invalid account type choice. Please choose 1 for Cheque or 2 for Savings.")
        else:
            print("Invalid password. Please try again.")

# if the user tries to login the account and if the password is invalid an error message pops up.
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    account = BankAccount.get_account_by_username(username)
    if account and account.password_hash == hashlib.sha256(password.encode()).hexdigest():
        print(f"Login successful! Welcome back, {username}.")
        return account
    else:
        print("Invalid username or password. Login failed.")
        return None

# This function prints these options
def main():
    while True:
        print("++++++++++++++++++++++++")
        print("=== Bug Bank Limited ===")
        print("++++++++++++++++++++++++")
        print("\nOptions:")
        print("1. Create Account")
        print("2. Login")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Check Balance")
        print("6. Account Holder List")
        print("7. Exit")
        choice = input("Enter your choice: ")

# If user enters a number outside the option it will request the user to put the valid option
        if choice == "1":
            account = create_account()
            if account:
                BankAccount.accounts.append(account)
        elif choice == "7":
            print("Thank you for using Bug Bank. Goodbye!")
            break
        elif choice == "2":
            account = login()
        elif choice == "3":
            if account:
                try:
                    amount = float(input("Enter the deposit amount: R "))
                    if amount > 0:
                        print(account.deposit(amount))
                    else:
                        print("Invalid amount. Please enter a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a numerical value.")
            else:
                print("Please login first.")
        elif choice == "4":
            if account:
                try:
                    amount = float(input("Enter the withdrawal amount: R "))
                    if amount > 0:
                        print(account.withdraw(amount))
                    else:
                        print("Invalid amount. Please enter a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a numerical value.")
            else:
                print("Please login first.")
        elif choice == "5":
            if account:
                print(account.check_balance())
            else:
                print("Please login first.")
        elif choice == "6":
            print("\nAccount Holder List:")
            for acc in BankAccount.accounts:
                print(f"Username: {acc.username}, Account Type: {acc.account_type}, \nBalance: R {acc.balance}")
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()