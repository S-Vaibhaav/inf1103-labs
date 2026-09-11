inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity or type quit: ").strip()

    if stock.lower() == "quit":
        break

    elif stock.startswith("-") and stock[1:].isdigit():
        print("Error: Negative numbers are not allowed.")
        failed_entries += 1
        continue

    elif not stock.isdigit():
        print("Error: Invalid input. Please enter an integer.")
        failed_entries += 1
        continue

    else:
        stock = int(stock)
        inventory += stock

        if inventory > 500:
            print("Overstock Alert!")
            break

print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)