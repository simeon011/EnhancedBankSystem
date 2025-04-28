from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from Bank_System.submission import skeleton


class TestMain(TestCase):
    def setUp(self):
        skeleton.account_holders = ["Simeon", "Ivan"]
        skeleton.balances = [1500, 1000]
        skeleton.transaction_histories = [["Deposit 1500"], ["Deposit 1000"]]
        skeleton.loans = [50, 100]

    def test_account_holders(self):
        skeleton.account_holders = ["Simeon", "Ivan"]
        index = skeleton.account_holders.index("Simeon")
        self.assertEqual("Simeon", skeleton.account_holders[index])

    def test_balance(self):
        index = skeleton.account_holders.index("Simeon")
        self.assertEqual(skeleton.balances[index], 1500)

    def test_transaction_histories(self):
        index = skeleton.account_holders.index("Simeon")
        self.assertEqual(["Deposit 1500"], skeleton.transaction_histories[index])

    def test_loans(self):
        index = skeleton.account_holders.index("Simeon")
        self.assertEqual(50, skeleton.loans[index])

    #create_account
    @patch('builtins.input', return_value="Boiko")
    @patch('sys.stdout', new_callable=StringIO)
    def test_create_account(self, mock_stdout, mock_input):
        skeleton.create_account()
        self.assertIn("Boiko", skeleton.account_holders)
        self.assertEqual(0, skeleton.balances[2])
        self.assertEqual([], skeleton.transaction_histories[2])
        self.assertEqual(0, skeleton.loans[2])
        output = mock_stdout.getvalue().strip()
        self.assertEqual("✅Your account has been created.", output)

    #create_account
    @patch('builtins.input', return_value="Simeon")
    @patch('sys.stdout', new_callable=StringIO)
    def test_existing_account_name(self, mock_stdout, mock_input):
        skeleton.create_account()
        skeleton.account_holders = ["Simeon", "Ivan"]
        skeleton.balances = [100]
        skeleton.transaction_histories = [["Deposit 100"]]
        skeleton.loans = [50]
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌There already exists a account with that name.", output)

    #deposit
    @patch('builtins.input', side_effect=["Simeon", 100])
    @patch('sys.stdout', new_callable=StringIO)
    def test_deposit_amount_in_existing_account(self, mock_stdout, mock_input):
        skeleton.account_holders = ["Simeon"]
        skeleton.balances = [1500, 1000]
        skeleton.transaction_histories = [["Deposit 1500"], ["Deposit 1000"]]
        skeleton.loans = [50, 100]
        skeleton.deposit()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("✅You successfully deposited 100.00$", output)
        self.test_transaction_histories = [["Deposit 1500", "Deposit 100"], ["Deposit 1000"]]
        self.assertEqual(1600, skeleton.balances[0])

    #deposit
    @patch('builtins.input', side_effect=["Simeon", "abc", -50, 0, 100])
    @patch('sys.stdout', new_callable=StringIO)
    def test_deposit_amount(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        skeleton.deposit()
        output = mock_stdout.getvalue().strip()
        self.assertIn("🔄❌Amount must be integer. Please try again", output)  #"abc"
        self.assertIn("🔄❌You cannot deposit less or equal on zero. Please try again", output)  #-50
        self.assertIn("🔄❌You cannot deposit less or equal on zero. Please try again", output)  #0
        self.assertIn("✅You successfully deposited 100.00$", output)
        self.assertEqual(["Deposit 1500", "Deposit 100.00$"], skeleton.transaction_histories[index])
        self.assertEqual(1600, skeleton.balances[index])

    #deposit
    @patch('builtins.input', return_value="Grigor")
    @patch('sys.stdout', new_callable=StringIO)
    def test_deposit_amount_in_not_existing_account(self, mock_stdout, mock_input):
        skeleton.deposit()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌That account does not exist.", output)  #"Grigor"

    #withdraw
    @patch('builtins.input', side_effect=["Simeon", "abc", -100, 2000, 0, 500])
    @patch('sys.stdout', new_callable=StringIO)
    def test_withdraw_amount(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        skeleton.withdraw()
        output = mock_stdout.getvalue().strip()
        self.assertIn("🔄❌Withdraw not possible. Please enter a integer", output)  #"abc"
        self.assertIn(
            "🔄❌You cannot withdraw less or equal on zero or your balance is less than amount you want withdraw. Please try again.",
            output)  #-100
        self.assertIn(
            "🔄❌You cannot withdraw less or equal on zero or your balance is less than amount you want withdraw. Please try again.",
            output)  #2000
        self.assertIn(
            "🔄❌You cannot withdraw less or equal on zero or your balance is less than amount you want withdraw. Please try again.",
            output)  #0
        self.assertIn("✅You successfully withdrawn 500.00$", output)
        self.assertEqual(["Deposit 1500", "Withdraw 500.00$"], skeleton.transaction_histories[index])
        self.assertEqual(1000, skeleton.balances[index])

    # withdraw
    @patch('builtins.input', return_value="Grigor")
    @patch('sys.stdout', new_callable=StringIO)
    def test_withdraw_amount_from_not_existing_account(self, mock_stdout, mock_input):
        skeleton.withdraw()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌That account does not exist.", output)  #"Grigor"

    #check_balance
    @patch('builtins.input', return_value="Simeon")
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_balance_on_existing_account(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        skeleton.check_balance()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("1500.00$", output)

    #check_balnce
    @patch('builtins.input', return_value="Grigor")
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_balance_on_not_existing_account(self, mock_stdout, mock_input):
        skeleton.check_balance()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌This account does not exist in the system.", output)  #"Grigor"

    #list_account
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_accounts(self, mock_stdout):
        skeleton.list_accounts()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("1. Account holder: Simeon, Balance: 1500.00$, Loans: 50.00$\n"
                         "2. Account holder: Ivan, Balance: 1000.00$, Loans: 100.00$", output)

    # list_account
    @patch('sys.stdout', new_callable=StringIO)
    def test_not_single_account_exists(self, mock_stdout):
        skeleton.account_holders = []
        skeleton.list_accounts()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌There are no created accounts.", output)

    #transfer_funds
    @patch('builtins.input', side_effect=["Simeon", -120, 0, "abc", 2000, 500, "Ivan"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_transfer_funds_with_msg_for_incorrect_numbers(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        second_index = skeleton.account_holders.index("Ivan")
        skeleton.transfer_funds()
        output = mock_stdout.getvalue().strip()
        self.assertIn("🔄❌You cannot transfer less or equal on zero or you don't have enough balance. Please try again.",
                      output)  #-120
        self.assertIn("🔄❌You cannot transfer less or equal on zero or you don't have enough balance. Please try again.",
                      output)  #0
        self.assertIn("🔄❌Please enter a number.", output)  #"abc"
        self.assertIn("🔄❌You cannot transfer less or equal on zero or you don't have enough balance. Please try again.",
                      output)  #2000
        self.assertIn("✅You successfully transferred 500.00$ to Ivan", output)
        self.assertEqual(["Deposit 1500", "Transfer 500.00$ to Ivan"], skeleton.transaction_histories[index])
        self.assertEqual(1000, skeleton.balances[index])
        self.assertEqual(["Deposit 1000", "Received +500.00$ from Simeon"],
                         skeleton.transaction_histories[second_index])
        self.assertEqual(1500, skeleton.balances[second_index])

    #transfer_funds
    @patch('builtins.input', side_effect=["Grigor"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_transfer_funds_for_incorrect_first_name_only(self, mock_stdout, mock_input):
        skeleton.transfer_funds()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌This name is not in the system.", output)  #"Grigor"

    #transfer_funds
    @patch('builtins.input', side_effect=["Simeon", 500, "Atanas"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_transfer_finds_for_incorrect_second_name_only(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        skeleton.transfer_funds()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌This name is not in the system.", output)  #"Atanas"
        self.assertEqual(["Deposit 1500"], skeleton.transaction_histories[index])
        self.assertEqual(1500, skeleton.balances[index])

    #apply_for_loan
    @patch('builtins.input', side_effect=["Grigor"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_apply_for_loan_incorrect_name(self, mock_stdout, mock_input):
        skeleton.apply_for_loan()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌This account does not exist in the system.", output)  #"Grigor"

    #apply_for_loan
    @patch('builtins.input', side_effect=["Simeon", 1000, "n"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_apply_for_loan_cancelled_application(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        skeleton.apply_for_loan()
        output = mock_stdout.getvalue().strip()
        self.assertIn("⚠️⚠️If you take out a loan of 1000.00$ you will have to repay 1030.00$ with interest rate⚠️⚠️",
                      output)  #1000
        self.assertIn("❌Loan application cancelled.", output)  #"n"
        self.assertEqual(1500, skeleton.balances[index])
        self.assertEqual(["Deposit 1500"], skeleton.transaction_histories[index])
        self.assertEqual(50, skeleton.loans[index])

    #apply_for_loan
    @patch('builtins.input', side_effect=["Simeon", 9960, "y"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_apply_for_loan_exceed_the_maximum_loan_amount(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        skeleton.apply_for_loan()
        output = mock_stdout.getvalue().strip()
        self.assertIn("⚠️⚠️If you take out a loan of 9960.00$ you will have to repay 10258.80$ with interest rate⚠️⚠️",
                      output)  #9960
        self.assertIn("❌You will exceed the maximum loan amount.", output)  #9960 + 50 > 10000
        self.assertEqual(1500, skeleton.balances[index])
        self.assertEqual(["Deposit 1500"], skeleton.transaction_histories[index])
        self.assertEqual(50, skeleton.loans[index])

    #apply_for_loan
    @patch('builtins.input', side_effect=["Simeon", "abc", 10001, -12, 0, 100, "y"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_apply_for_loan_enter_incorrect_numbers(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        skeleton.apply_for_loan()
        output = mock_stdout.getvalue().strip()
        self.assertIn("🔄❌Please enter a valid number.", output)  #"abc" != integer
        self.assertIn("🔄❌Max amount for loan is 10000$. Please enter again.", output)  #10001 > 10000
        self.assertIn("🔄❌Please enter a positive amount.", output)  #-12 <= 0
        self.assertIn("🔄❌Please enter a positive amount.", output)  #0 <= 0
        self.assertIn("⚠️⚠️If you take out a loan of 100.00$ you will have to repay 103.00$ with interest rate⚠️⚠️",
                      output)  #100
        self.assertEqual(1600, skeleton.balances[index])
        self.assertEqual(["Deposit 1500", "Loan 100.00$"], skeleton.transaction_histories[index])
        self.assertEqual(150, skeleton.loans[index])

    #apply_for_loan
    @patch('builtins.input', side_effect=["Simeon", 5000, "y"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_apply_for_loan_approved(self, mock_stdout, mock_input):
        index = skeleton.account_holders.index("Simeon")
        skeleton.apply_for_loan()
        output = mock_stdout.getvalue().strip()
        self.assertIn("⚠️⚠️If you take out a loan of 5000.00$ you will have to repay 5150.00$ with interest rate⚠️⚠️",
                      output)  #5000
        self.assertIn("✅You are approved for a loan.", output)
        self.assertEqual(6500, skeleton.balances[index])
        self.assertEqual(["Deposit 1500", "Loan 5000.00$"], skeleton.transaction_histories[index])
        self.assertEqual(5050, skeleton.loans[index])

    #repay_loan
    @patch('builtins.input', side_effect=["Grigor"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repay_loan_not_exist_name(self, mock_stdout, mock_input):
        skeleton.repay_loan()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌This account does not exist in the system.", output)  #"Grigor"

    #repay_loan
    @patch('builtins.input', side_effect=["Simeon", "abc", 1600, 0, -10, 30])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repay_loan_remaining_amount_with_invalid_enter_numbers(self, mock_stdout, mock_input):
        skeleton.account_holders = ["Simeon"]
        skeleton.balances = [1500]
        skeleton.loans = [50]
        skeleton.transaction_histories = [["Deposit 1500"]]
        skeleton.INTEREST_RATE = 0.03
        initial_loan = skeleton.loans[0]
        expected_total_loan = initial_loan * (1 + skeleton.INTEREST_RATE)
        expected_remaining_loan = expected_total_loan - 30
        skeleton.repay_loan()
        output = mock_stdout.getvalue().strip()
        self.assertIn("🔄❌Please enter a valid number.", output)  #"abc" not integer
        self.assertIn("🔄❌Insufficient balance. Please try with less amount", output)  #1600 > balance
        self.assertIn("🔄❌Amount must be greater than zero.", output)  #0 <= 0
        self.assertIn("🔄❌Amount must be greater than zero.", output)  #-10 <= 0
        self.assertIn("️⚠️Remaining loan repayment amount 21.50$⚠️", output)  #30
        self.assertEqual(1470, skeleton.balances[0])
        self.assertEqual(["Deposit 1500", "Loan 30.00$"], skeleton.transaction_histories[0])
        self.assertAlmostEquals(expected_remaining_loan, skeleton.loans[0])

    #repay_loan
    @patch('builtins.input', side_effect=["Simeon", 51.50])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repay_loan_successfully_repay(self, mock_stdout, mock_input):
        skeleton.account_holders = ["Simeon"]
        skeleton.balances = [1500]
        skeleton.loans = [50]
        skeleton.transaction_histories = [["Deposit 1500"]]
        skeleton.INTEREST_RATE = 0.03
        initial_loan = skeleton.loans[0]
        expected_total_loan = initial_loan * (1 + skeleton.INTEREST_RATE)
        skeleton.repay_loan()
        output = mock_stdout.getvalue().strip()
        self.assertIn("⚠️You have a 51.50$ loan⚠️", output)  #51.50
        self.assertIn("🎉You have successfully repaid your loan.", output)  #51.50 - 51.50
        self.assertEqual(0, skeleton.loans[0])

    #identify_card_type
    @patch('builtins.input', return_value="4321")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_VISA(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("💳Card typs: VISA", output)  #start with 4 "4321"

    #identify_card_type
    @patch('builtins.input', return_value="5142")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_MasterCard(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("💳Card typs: MasterCard", output)  #the first two numbers must be [51, 52, 53, 54, 55] "51"

    #identify_card_type
    @patch('builtins.input', return_value="5242")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_MasterCard(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("💳Card typs: MasterCard", output)  #the first two numbers must be [51, 52, 53, 54, 55] "52"

    #identify_card_type
    @patch('builtins.input', return_value="5342")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_MasterCard(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("💳Card typs: MasterCard", output)  #the first two numbers must be [51, 52, 53, 54, 55] "53"

    #identify_card_type
    @patch('builtins.input', return_value="5442")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_MasterCard(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("💳Card typs: MasterCard", output)  #the first two numbers must be [51, 52, 53, 54, 55] "54"

    #identify_card_type
    @patch('builtins.input', return_value="5542")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_MasterCard(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("💳Card typs: MasterCard", output)  #the first two numbers must be [51, 52, 53, 54, 55] "55"

    #identify_card_type
    @patch('builtins.input', return_value="3458")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_AmericanExpress(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("💳Card typs: American Express", output)  #the first two numbers must be 34 or 37 "34"

    #identify_card_type
    @patch('builtins.input', return_value="3758")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_AmericanExpress(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("💳Card typs: American Express", output)  # the first two numbers must be 34 or 37 "37"

    #identify_card_type
    @patch('builtins.input', return_value="3258")
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_no_match_type(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertEqual("❌No match card type", output) #"32"

    #identify_card_type
    @patch('builtins.input', side_effect=["abc", "abcd"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_identify_card_number_no_match_type(self, mock_stdout, mock_input):
        skeleton.identify_card_type()
        output = mock_stdout.getvalue().strip()
        self.assertIn("🔄Your card number is less than 4. Please enter again.", output) #"abc"
        self.assertIn("❌No match card type", output)
