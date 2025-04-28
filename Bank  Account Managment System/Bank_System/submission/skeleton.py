# Enhanced Bank Account Management System

# 🏦 Data Structures to Store Information
account_holders = []  # Account names
balances = []  # Account balances
transaction_histories = []  # Account transaction logs
loans = []  # Account loan details

MAX_LOAN_AMOUNT = 10000
INTEREST_RATE = 0.03


def display_menu():
    """Main menu for banking system."""
    print("\n🌟 Welcome to Enhanced Bank System 🌟")
    print("1️⃣ Create Account")
    print("2️⃣ Deposit Money")
    print("3️⃣ Withdraw Money")
    print("4️⃣ Check Balance")
    print("5️⃣ List All Accounts")
    print("6️⃣ Transfer Funds")
    print("7️⃣ View Transaction History")
    print("8️⃣ Apply for Loan")
    print("9️⃣ Repay Loan")
    print("🔟 Identify Credit Card Type")
    print("0️⃣ Exit")


def create_account():
    """Create a new account."""
    name = input("Your name is: ")
    if name not in account_holders:
        account_holders.append(name)
        balances.append(0)
        loans.append(0)
        transaction_histories.append([])
        print("✅Your account has been created.")
    else:
        print("❌There already exists a account with that name.")


def deposit():
    """Deposit money into an account."""
    name = input("Enter your account name: ")
    if name in account_holders:
        index = account_holders.index(name)
        while True:
            try:
                amount = float(input("Enter your amount deposit: "))
                if amount > 0:
                    balances[index] += amount
                    transaction_histories[index].append(f"Deposit {amount:.2f}$")
                    print(f"✅You successfully deposited {amount:.2f}$")
                    break
                else:
                    print("🔄❌You cannot deposit less or equal on zero. Please try again")
                    continue
            except ValueError:
                print("🔄❌Amount must be integer. Please try again")
    else:
        print("❌That account does not exist.")


def withdraw():
    """Withdraw money from an account."""
    name = input("Enter your account name: ")
    if name in account_holders:
        index = account_holders.index(name)
        while True:
            try:
                amount = float(input("Enter your amount withdraw: "))
                if (amount > 0) and (amount <= balances[index]):
                    balances[index] -= amount
                    transaction_histories[index].append(f"Withdraw {amount:.2f}$")
                    print(f"✅You successfully withdrawn {amount:.2f}$")
                    break
                else:
                    print(
                        "🔄❌You cannot withdraw less or equal on zero or your balance is less than amount you want withdraw. Please try again.")
                    continue
            except ValueError:
                print("🔄❌Withdraw not possible. Please enter a integer")
    else:
        print("❌That account does not exist.")


def check_balance():
    """Check balance of an account."""
    name = input("Enter your account name: ")
    if name in account_holders:
        index = account_holders.index(name)
        print(f"{balances[index]:.2f}$")
    else:
        print("❌This account does not exist in the system.")


def list_accounts():
    """List all account holders and details."""
    if len(account_holders) > 0:
        for n in range(len(account_holders)):
            print(f"{n + 1}. Account holder: {account_holders[n]}, Balance: {balances[n]:.2f}$, Loans: {loans[n]:.2f}$")
    else:
        print("❌There are no created accounts.")


def transfer_funds():
    """Transfer funds between two accounts."""
    name = input("Enter your account name: ")
    if name in account_holders:
        index = account_holders.index(name)
        while True:
            try:
                amount = float(input("Enter amount for transfer: "))
                if (amount > 0) and (amount <= balances[index]):
                    second_name = input("Enter destination account name:  ")
                    if second_name in account_holders:
                        second_index = account_holders.index(second_name)
                        balances[index] -= amount
                        transaction_histories[index].append(f"Transfer {amount:.2f}$ to {second_name}")
                        balances[second_index] += amount
                        transaction_histories[second_index].append(f"Received +{amount:.2f}$ from {name}")
                        print(f"✅You successfully transferred {amount:.2f}$ to {second_name}")
                        break
                    else:
                        print("❌This name is not in the system.")
                        break
                else:
                    print(
                        "🔄❌You cannot transfer less or equal on zero or you don't have enough balance. Please try again.")
                    continue
            except ValueError:
                print("🔄❌Please enter a number.")
    else:
        print("❌This name is not in the system.")


def view_transaction_history():
    """View transactions for an account."""
    name = input("Enter your account name: ")
    if name in account_holders:
        index = account_holders.index(name)
        print(', '.join(transaction_histories[index]))
    else:
        print("❌This account does not exist in the system.")


def apply_for_loan():
    """Allow user to apply for a loan."""
    name = input("Enter your account name: ")
    if name in account_holders:
        index = account_holders.index(name)
        while True:
            try:
                amount = float(input("Enter amount for loan: "))
                if amount <= 0:
                    print("🔄❌Please enter a positive amount.")
                    continue
                if amount > MAX_LOAN_AMOUNT:
                    print("🔄❌Max amount for loan is 10000$. Please enter again.")
                    continue
                break
            except ValueError:
                print("🔄❌Please enter a valid number.")

        interest_rate = amount * INTEREST_RATE
        return_amount = interest_rate + amount
        loan_amount = loans[index]
        new_loan_amount = loan_amount + amount
        print(
            f"⚠️⚠️If you take out a loan of {amount:.2f}$ you will have to repay {return_amount:.2f}$ with interest rate⚠️⚠️")
        answer = input("Are you sure you want loans(Y/N): ")
        if answer.lower() == 'y':
            if new_loan_amount <= MAX_LOAN_AMOUNT:
                balances[index] += amount
                transaction_histories[index].append(f"Loan {amount:.2f}$")
                loans[index] += amount
                print("✅You are approved for a loan.")
            else:
                print("❌You will exceed the maximum loan amount.")
        else:
            print("❌Loan application cancelled.")
    else:
        print("❌This account does not exist in the system.")


def repay_loan():
    """Allow user to repay a loan."""
    name = input("Enter your account name: ")
    if name in account_holders:
        index = account_holders.index(name)
        loans_name = loans[index] + (INTEREST_RATE * loans[index])
        print(f"⚠️You have a {loans_name:.2f}$ loan⚠️")
        while True:
            try:
                amount = float(input("Please enter the amount for the deduct loan: "))
                if amount <= 0:
                    print("🔄❌Amount must be greater than zero.")
                    continue
                if amount <= balances[index]:
                    balances[index] -= amount
                    transaction_histories[index].append(f"Loan {amount:.2f}$")
                    loans_name -= amount
                    loans[index] = loans_name
                    if loans[index] < 0:
                        loans[index] = 0
                    if loans[index] <= 0:
                        print("🎉You have successfully repaid your loan.")
                        break
                    else:
                        print(f"️⚠️Remaining loan repayment amount {loans_name:.2f}$⚠️")
                    break
                else:
                    print("🔄❌Insufficient balance. Please try with less amount")
                    continue
            except ValueError:
                print("🔄❌Please enter a valid number.")
    else:
        print("❌This account does not exist in the system.")


def identify_card_type():
    """Identify type of credit card."""
    while True:
        card_number = input("Enter first 4 digits of card number: ")
        if len(str(card_number)) < 4:
            print("🔄Your card number is less than 4. Please enter again.")
            continue
        break
    master_card = ["51", "52", "53", "54", "55"]
    if card_number[0] == "4":
        print("💳Card typs: VISA")
    elif card_number[:2] in master_card:
        print("💳Card typs: MasterCard")
    elif card_number.startswith("34") or card_number.startswith("37"):
        print("💳Card typs: American Express")
    else:
        print("❌No match card type")


def main():
    """Run the banking system."""
    while True:
        display_menu()
        choice = int(input("Enter your choice: "))
        # Map choices to functions
        if choice == 1:
            create_account()
        elif choice == 2:
            deposit()
        elif choice == 3:
            withdraw()
        elif choice == 4:
            check_balance()
        elif choice == 5:
            list_accounts()
        elif choice == 6:
            transfer_funds()
        elif choice == 7:
            view_transaction_history()
        elif choice == 8:
            apply_for_loan()
        elif choice == 9:
            repay_loan()
        elif choice == 10:
            identify_card_type()
        elif choice == 0:
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Try again!")


if __name__ == "__main__":
    main()
