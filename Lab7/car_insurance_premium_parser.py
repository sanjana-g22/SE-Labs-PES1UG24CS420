from datetime import date


def normalize_registration(plate):
    """
    Removes spaces, dashes and dots from a registration number and upper-cases it.
    Returns an empty string if plate is not a string (e.g. None).
    """
    if not isinstance(plate, str):
        return ""
    plate = plate.strip().upper()
    for ch in [' ', '-', '.']:
        plate = plate.replace(ch, '')
    return plate


def total_claim_amount(text):
    """
    Adds up claim amounts separated by semicolons.
    Empty, non-numeric, negative or malformed amounts are ignored.
    Returns 0 if text is not a string (e.g. None).
    """
    if not isinstance(text, str):
        return 0
    total = 0
    for amount in text.split(';'):
        amount = amount.strip()
        # accept only plain ASCII digits (rejects "abc", "12.5", "-5", "", "1_000")
        if not (amount.isascii() and amount.isdigit()):
            continue
        try:
            total += int(amount)
        except ValueError:
            # e.g. absurdly long digit strings exceeding Python's int limit
            continue
    return total


def driver_age(dob, current_year=2026):
    """
    Works out the driver's age from a DD/MM/YYYY date of birth.
    Returns None if dob is not a string, is not in DD/MM/YYYY format,
    is not a real calendar date, or is in the future.
    """
    if not isinstance(dob, str):
        return None
    parts = dob.strip().split('/')
    if len(parts) != 3:
        return None
    for p in parts:
        p = p.strip()
        if not (p.isascii() and p.isdigit()):
            return None
    try:
        day, month, year = (int(p.strip()) for p in parts)
        date(year, month, day)  # raises ValueError for impossible dates
    except ValueError:
        return None
    if year > current_year:
        return None
    return current_year - year


def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    print("Normalized registration:", normalize_registration(value))

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    print("Total claimed:", total_claim_amount(value))

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    age = driver_age(value)
    if age is None:
        print("Invalid date of birth. Please use DD/MM/YYYY.")
    else:
        print("Driver age in 2026:", age)

if __name__ == "__main__":
    main()