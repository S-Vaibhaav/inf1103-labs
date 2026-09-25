def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            total = int(lines[0].strip())

            if len(lines) > 1 and lines[1].strip():
                history = [int(x) for x in lines[1].strip().split(",")]
            else:
                history = []

            return total, history

    except FileNotFoundError:
        return 0, []

    except (ValueError, IndexError):
        return 0, []


def save_inventory(total, history):
    with open("inventory.txt", "w") as file:
        file.write(str(total) + "\n")
        file.write(",".join(str(x) for x in history))


def get_valid_input():
    stock = input("Enter stock quantity or type quit: ").strip()

    if stock.lower() == "quit":
        return "quit"

    elif stock.startswith("-") and stock[1:].isdigit():
        print("Error: Negative numbers are not allowed.")
        return None

    elif not stock.isdigit():
        print("Error: Invalid input. Please enter an integer.")
        return None

    else:
        return int(stock)


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts, deliveries_processed):
    print("\nFinal Report")
    print("Total Units Processed:", total_units)
    print("Total Deliveries Processed:", deliveries_processed)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory, transaction_history = load_inventory()

failed_entries = 0
deliveries_processed = 0


while True:
    stock = get_valid_input()

    if stock == "quit":
        break

    elif stock is None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)

    transaction_history.append(stock)

    tax = calculate_tax(stock)
    print("Tax for this delivery:", tax)

    deliveries_processed += 1

    if inventory > 500:
        print("Overstock Alert!")
        break


save_inventory(inventory, transaction_history)

generate_report(
    inventory,
    failed_entries,
    deliveries_processed
)