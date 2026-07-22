from datetime import date


VALID_HOUSE_STATUS = [
    "Available",
    "Occupied",
    "Under Maintenance"
]

VALID_PAYMENT_STATUS = [
    "Pending",
    "Paid",
    "Overdue"
]


def valid_house_status(status):

    return status in VALID_HOUSE_STATUS


def valid_payment_status(status):

    return status in VALID_PAYMENT_STATUS


def valid_agreement_dates(
    move_in_date,
    agreement_end_date
):

    return agreement_end_date > move_in_date


def rent_amount_valid(amount):

    return amount > 0


def house_available(status):

    return status == "Available"
