from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from decimal import Decimal, ROUND_HALF_UP
import json


# =========================
# MY FINTECH APP
# =========================

APP_NAME = "My Fintech App"

wallet = Decimal("100000.00")
TRANSFER_FEE = Decimal("500.00")

transactions = []


# =========================
# MONEY FORMAT
# =========================

def money(amount):
    amount = Decimal(amount)
    return amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


# =========================
# LIVE EXCHANGE RATE
# =========================

def get_live_rate(base, quote):

    base = base.upper()
    quote = quote.upper()

    if base == quote:
        return Decimal("1"), "same currency"

    url = f"https://api.frankfurter.dev/v2/rate/{base.lower()}/{quote.lower()}"

    request = Request(
        url,
        headers={"User-Agent": "MyFintechApp/1.0"}
    )

    try:
        with urlopen(request, timeout=10) as response:

            data = json.loads(
                response.read().decode("utf-8"),
                parse_float=Decimal
            )

            rate = data["rate"]
            date = data["date"]

            return rate, date

    except HTTPError as error:

        if error.code == 404 or error.code == 422:
            raise ValueError(
                "Currency not supported or currency code is invalid."
            )

        raise ValueError("Exchange-rate server error.")

    except URLError:

        raise ValueError(
            "No internet connection. Please check your internet."
        )

    except Exception:

        raise ValueError(
            "Could not get the exchange rate."
        )


# =========================
# CURRENCY CONVERTER
# =========================

def convert_currency():

    print("\n========== CURRENCY CONVERTER ==========")

    base = input(
        "Enter the currency you have (example NGN): "
    ).strip().upper()

    quote = input(
        "Enter the currency you want (example USD): "
    ).strip().upper()

    amount_text = input(
        f"Enter amount in {base}: "
    ).strip()

    try:

        amount = Decimal(amount_text)

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        print("\nGetting latest exchange rate...")

        rate, date = get_live_rate(base, quote)

        result = amount * rate

        print("\n---------- RESULT ----------")

        print(
            f"{money(amount)} {base} = "
            f"{money(result)} {quote}"
        )

        print(
            f"1 {base} = {rate} {quote}"
        )

        print(
            f"Rate date: {date}"
        )

        print("----------------------------")

    except ValueError as error:

        print(f"\nError: {error}")

    except Exception:

        print("\nPlease enter a valid amount.")


# =========================
# TRANSFER MONEY
# =========================

def transfer_money():

    global wallet

    print("\n========== MONEY TRANSFER ==========")

    name = input("Receiver name: ").strip()

    account = input("Receiver account/phone: ").strip()

    amount_text = input("Amount to send (NGN): ").strip()

    try:

        amount = Decimal(amount_text)

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        total = amount + TRANSFER_FEE

        if total > wallet:

            print("\nInsufficient wallet balance.")

            print(
                f"Your balance: ₦{money(wallet)}"
            )

            print(
                f"Required: ₦{money(total)}"
            )

            return

        wallet -= total

        transactions.append({
            "type": "Transfer",
            "receiver": name,
            "account": account,
            "amount": amount,
            "fee": TRANSFER_FEE
        })

        print("\n========== TRANSFER SUCCESS ==========")

        print(f"Receiver: {name}")

        print(f"Amount: ₦{money(amount)}")

        print(f"Fee: ₦{money(TRANSFER_FEE)}")

        print(f"Total: ₦{money(total)}")

        print(
            f"New balance: ₦{money(wallet)}"
        )

    except:

        print("Please enter a valid amount.")


# =========================
# WALLET
# =========================

def show_wallet():

    print("\n========== WALLET ==========")

    print(
        f"Balance: ₦{money(wallet)}"
    )


# =========================
# TRANSACTION HISTORY
# =========================

def show_transactions():

    print("\n====== TRANSACTION HISTORY ======")

    if not transactions:

        print("No transactions yet.")

        return

    for number, transaction in enumerate(
        transactions,
        start=1
    ):

        print(f"\nTransaction {number}")

        print(
            f"Type: {transaction['type']}"
        )

        print(
            f"Receiver: {transaction['receiver']}"
        )

        print(
            f"Amount: ₦{money(transaction['amount'])}"
        )

        print(
            f"Fee: ₦{money(transaction['fee'])}"
        )


# =========================
# MAIN MENU
# =========================

def main():

    while True:

        print("\n")
        print("================================")
        print("       MY FINTECH APP")
        print("================================")

        print("1. Wallet")

        print("2. Live Currency Converter")

        print("3. Transfer Money")

        print("4. Transaction History")

        print("5. Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":

            show_wallet()

        elif choice == "2":

            convert_currency()

        elif choice == "3":

            transfer_money()

        elif choice == "4":

            show_transactions()

        elif choice == "5":

            print("\nThank you for using My Fintech App.")

            break

        else:

            print("\nInvalid option.")


# =========================
# START APP
# =========================

main()
