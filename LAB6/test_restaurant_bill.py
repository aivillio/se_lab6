import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# ==============================================================================
# Comprehensive Branch Coverage Test Suite
# Tests every decision branch, boundary condition, and edge case to achieve
# 100% Branch Coverage on restaurant_bill.py.
# ==============================================================================


# ------------------------------------------------------------------------------
# 1. Tests for bill_total(section, food_total, guests, is_happy_hour)
# ------------------------------------------------------------------------------

def test_bill_unknown_section():
    """Branch: section not in SERVICE_CHARGE -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("drive_thru", 1000, 2, False)


def test_bill_invalid_order_negative_food():
    """Branch: food_total < 0 or guests < 1 -> first condition True (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -50, 2, False)


def test_bill_invalid_order_zero_guests():
    """Branch: food_total < 0 or guests < 1 -> second condition True (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", 1000, 0, False)


def test_bill_dine_in_regular():
    """
    Branch tests:
    - section in SERVICE_CHARGE: True ("dine_in" -> 10% charge)
    - food_total < 0 or guests < 1: False
    - is_happy_hour and section != "takeaway": False (happy hour False)
    - guests >= 8: False
    Calculation:
      food_total = 1000
      service = 1000 * 10 // 100 = 100
      total = 1100
      grand_total = 1100 + 1100 * 5 // 100 = 1155
    """
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_bill_dine_in_happy_hour():
    """
    Branch tests:
    - is_happy_hour and section != "takeaway": True (20% discount applies)
    - guests >= 8: False
    Calculation:
      food_total = 1000 * 80 // 100 = 800
      service = 800 * 10 // 100 = 80
      total = 880
      grand_total = 880 + 880 * 5 // 100 = 924
    """
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_bill_takeaway_happy_hour_no_discount():
    """
    Branch tests:
    - is_happy_hour is True BUT section == "takeaway": False branch of condition
      (no discount for takeaway even during happy hour)
    - section takeaway service charge: 0%
    Calculation:
      food_total = 1000
      service = 1000 * 0 // 100 = 0
      total = 1000
      grand_total = 1000 + 1000 * 5 // 100 = 1050
    """
    assert bill_total("takeaway", 1000, 2, True) == 1050


def test_bill_rooftop_happy_hour_large_party():
    """
    Branch tests:
    - section rooftop service charge: 15%
    - is_happy_hour and section != "takeaway": True
    - guests >= 8: True (adds 200 service charge)
    Calculation:
      food_total = 1000 * 80 // 100 = 800
      service = 800 * 15 // 100 = 120 + 200 = 320
      total = 1120
      grand_total = 1120 + 1120 * 5 // 100 = 1176
    """
    assert bill_total("rooftop", 1000, 8, True) == 1176


# ------------------------------------------------------------------------------
# 2. Tests for split_bill(total, people, tip_percent)
# ------------------------------------------------------------------------------

def test_split_invalid_people():
    """Branch: people < 1 -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


def test_split_invalid_tip():
    """Branch: tip_percent < 0 -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 4, -5)


def test_split_even():
    """
    Branch tests:
    - people < 1: False
    - tip_percent < 0: False
    - grand_total % people != 0: False (even division, no remainder)
    Calculation:
      grand_total = 1000 + 1000 * 10 // 100 = 1100
      share = 1100 // 4 = 275 (1100 % 4 == 0)
    """
    assert split_bill(1000, 4, 10) == 275


def test_split_with_remainder():
    """
    Branch tests:
    - grand_total % people != 0: True (rounds up by adding 1)
    Calculation:
      grand_total = 100 + 100 * 0 // 100 = 100
      share = 100 // 3 = 33
      100 % 3 != 0 -> share = 34
    """
    assert split_bill(100, 3, 0) == 34


# ------------------------------------------------------------------------------
# 3. Tests for table_wait(party_size, free_tables, has_reservation)
# ------------------------------------------------------------------------------

def test_table_wait_party_too_large():
    """Branch: party_size > 12 -> True ("call ahead")."""
    assert table_wait(13, 5, False) == "call ahead"


def test_table_wait_has_reservation():
    """
    Branch tests:
    - party_size > 12: False
    - has_reservation: True -> "seat now"
    """
    assert table_wait(6, 0, True) == "seat now"


def test_table_wait_no_free_tables():
    """
    Branch tests:
    - party_size > 12: False
    - has_reservation: False
    - free_tables == 0: True -> "waitlist"
    """
    assert table_wait(4, 0, False) == "waitlist"


def test_table_wait_large_party_one_table():
    """
    Branch tests:
    - free_tables == 0: False
    - party_size > 6 and free_tables < 2: True (party_size=8, free_tables=1) -> "waitlist"
    """
    assert table_wait(8, 1, False) == "waitlist"


def test_table_wait_large_party_multiple_tables():
    """
    Branch tests:
    - party_size > 6: True BUT free_tables < 2: False (free_tables=2) -> falls through to "seat now"
    """
    assert table_wait(8, 2, False) == "seat now"


def test_table_wait_small_party_one_table():
    """
    Branch tests:
    - party_size > 6: False (party_size=4) -> falls through to "seat now"
    """
    assert table_wait(4, 1, False) == "seat now"
