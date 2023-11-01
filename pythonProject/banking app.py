print("========================================")
print("========================================")
print("===== WELCOME TO BUG BANK LIMITED =====")
print("========================================")
print("========================================")
while True:

    choice = input("Would you like to make a transaction? (Enter the corresponding number)\n1. Yes\n2. No\n")
    print(
        "--------------------------------------------------------------------------------")
    if choice == "No":
        break

    if choice == "Yes":
        transaction_type = input(
            "Would you like to make a deposit or withdrawal?\n1. Deposit\n2. Withdrawal\n")

        if transaction_type == "Yes":
            amount = input("How much would you like to deposit? ")
            make_deposit(amount)
        elif transaction_type == "No":
            amount = input("How much would you like to withdraw? ")
            make_withdrawal(amount)
        else:
            print("You provided an invalid input.")
            continue

    current_balance = get_balance()
    print(f"Current balance: {current_balance}")

print("Thank you for using the Banking Application!")
