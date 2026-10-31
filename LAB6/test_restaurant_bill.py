import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# Test suite demonstrating Line Coverage (Code Coverage >= 90%)
# Notice that while every statement is executed (100% line coverage),
# several decision branches remain untested (e.g. false branches for happy hour, party size, even splits).

def test_unknown_section():
    # Covers line 6: raise ValueError("unknown section")
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("patio", 1000, 2, False)


def test_invalid_order_negative_food():
    # Covers line 8: raise ValueError("invalid order")
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -10, 2, False)


def test_happy_hour_and_large_party():
    # Covers line 10: happy hour discount and line 13: guests >= 8 surcharge
    # food_total: 1000 * 80 // 100 = 800
    # rooftop service (15%): 800 * 15 // 100 = 120 + 200 = 320
    # total: 1120 + 1120 * 5 // 100 = 1176
    assert bill_total("rooftop", 1000, 8, True) == 1176


def test_split_invalid_people():
    # Covers line 20: raise ValueError("invalid people count")
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


def test_split_invalid_tip():
    # Covers line 22: raise ValueError("invalid tip")
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 2, -1)


def test_split_with_remainder():
    # Covers line 26: share += 1 when remainder exists
    assert split_bill(100, 3, 0) == 34


def test_table_wait_call_ahead():
    # Covers line 32: party_size > 12 -> "call ahead"
    assert table_wait(13, 2, False) == "call ahead"


def test_table_wait_reservation():
    # Covers line 34: has_reservation -> "seat now"
    assert table_wait(4, 0, True) == "seat now"


def test_table_wait_no_tables():
    # Covers line 36: free_tables == 0 -> "waitlist"
    assert table_wait(4, 0, False) == "waitlist"


def test_table_wait_large_party_few_tables():
    # Covers line 38: party_size > 6 and free_tables < 2 -> "waitlist"
    assert table_wait(8, 1, False) == "waitlist"


def test_table_wait_seat_now():
    # Covers line 39: fallback -> "seat now"
    assert table_wait(4, 2, False) == "seat now"
