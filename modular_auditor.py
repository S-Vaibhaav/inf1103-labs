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


inventory = 0
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

    tax = calculate_tax(stock)
    print("Tax for this delivery:", tax)

    deliveries_processed += 1

    if inventory > 500:
        print("Overstock Alert!")
        break


generate_report(
    inventory,
    failed_entries,
    deliveries_processed
)