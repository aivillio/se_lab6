# Lab 6: Code and Branch Coverage Analysis Report

**Repository:** `L6_L7_58_restaurant_bill`  
**Application Under Test:** `restaurant_bill.py`  
**Date:** October 31, 2026  

---

## 1. Executive Summary

This report documents the coverage analysis, test design, and verification process conducted for **Lab 6: Code and Branch Coverage Analysis**. 

- **Initial State**: Starter test cases achieved only **52% code coverage** and **44% branch coverage**, missing critical error handling, happy hour discounts, large party fees, and table seating logic.
- **Code Coverage Milestone**: Created targeted test cases in [`CodeCoverageTest_restaurant_bill.py`](file:///C:/Users/aivil/Downloads/selab6/L6_L7_58_restaurant_bill/LAB6/CodeCoverageTest_restaurant_bill.py) executing all statements, achieving **100% Statement (Line) Coverage** (33/33 statements). When branch coverage was measured, 3 decision branches were revealed as unexercised (`9->11`, `12->14`, `25->27`), providing clear empirical proof of why line coverage alone is insufficient.
- **Branch Coverage Milestone**: Designed comprehensive branch test cases in [`BranchCoverageTest_restaurant_bill.py`](file:///C:/Users/aivil/Downloads/selab6/L6_L7_58_restaurant_bill/LAB6/BranchCoverageTest_restaurant_bill.py) covering all 22 decision outcomes and compound predicate truth assignments, achieving **100% Branch Coverage** and **100% Line Coverage** with 17 passed test cases and 0 missing branches.

---

## 2. Code Coverage vs. Branch Coverage

| Metric | Definition | Significance | Weakness |
| :--- | :--- | :--- | :--- |
| **Line / Statement Coverage** | Measures whether each statement/line of code has been executed at least once during testing. | Ensures that dead code is identified and every implemented feature is triggered. | Can report 100% coverage even when entire logical branches (e.g., `else` or implicit false conditions) are untested. |
| **Branch / Decision Coverage** | Measures whether each branch of every control structure (e.g. `if`, `elif`, compound conditions) evaluated to both `True` and `False`. | Verifies all logical outcomes and edge cases of decision points. | Requires more test cases to test both positive and negative decision evaluations. |

---

## 3. Coverage Analysis Progression

### 3.1 Initial State (Starter Tests)
- **Test File**: `test_restaurant_bill.py` (2 tests: `test_dine_in_bill`, `test_even_split`)
- **Statements**: 33 total, 16 missed (**52% Statement Coverage**)
- **Branches**: 22 total, 7 partial branches (**44% Branch Coverage**)
- **Untested Code**:
  - `bill_total`: Invalid section exceptions, invalid order validation, happy hour discount, large party fees (guests >= 8).
  - `split_bill`: Validation for `people < 1`, `tip_percent < 0`, and fractional split handling (`share += 1`).
  - `table_wait`: Completely uncalled (lines 31–39).

### 3.2 Phase 1: Code Coverage Test Suite (>90% Line Coverage)
- **Test File**: [`CodeCoverageTest_restaurant_bill.py`](file:///C:/Users/aivil/Downloads/selab6/L6_L7_58_restaurant_bill/LAB6/CodeCoverageTest_restaurant_bill.py) (11 tests)
- **Line Coverage Results**:
  ```text
  Name                                  Stmts   Miss  Cover   Missing
  -------------------------------------------------------------------
  CodeCoverageTest_restaurant_bill.py      28      0   100%
  restaurant_bill.py                       33      0   100%
  -------------------------------------------------------------------
  TOTAL                                    61      0   100%
  ```
- **Branch Coverage on Line Suite** (demonstrating the limitation of line coverage):
  ```text
  Name                                  Stmts   Miss Branch BrPart  Cover   Missing
  ---------------------------------------------------------------------------------
  CodeCoverageTest_restaurant_bill.py      28      0      0      0   100%
  restaurant_bill.py                       33      0     22      3    95%   9->11, 12->14, 25->27
  ---------------------------------------------------------------------------------
  TOTAL                                    61      0     22      3    96%
  ```
- **Untested Branches Identified**:
  - `9->11`: `if is_happy_hour and section != "takeaway"` — False evaluation skipped.
  - `12->14`: `if guests >= 8` — False evaluation skipped (bypassing the fee).
  - `25->27`: `if grand_total % people != 0` — False evaluation skipped (exact split).

### 3.3 Phase 2: Branch Coverage Test Suite (100% Branch Coverage)
- **Test File**: [`BranchCoverageTest_restaurant_bill.py`](file:///C:/Users/aivil/Downloads/selab6/L6_L7_58_restaurant_bill/LAB6/BranchCoverageTest_restaurant_bill.py) (17 tests)
- **Branch Coverage Results**:
  ```text
  Name                                    Stmts   Miss Branch BrPart  Cover   Missing
  -----------------------------------------------------------------------------------
  BranchCoverageTest_restaurant_bill.py      41      0      0      0   100%
  restaurant_bill.py                         33      0     22      0   100%
  -----------------------------------------------------------------------------------
  TOTAL                                      74      0     22      0   100%
  ```
- **Result**: **100% Branch Coverage (22/22 branches)** and **100% Line Coverage (33/33 statements)** with **0 missing lines or branches**.

---

## 4. Test Case Specification & Decision Branch Matrix

| Function | Test Case | Inputs | Branch Evaluated | Expected Output |
| :--- | :--- | :--- | :--- | :--- |
| `bill_total` | `test_bill_unknown_section` | `("drive_thru", 1000, 2, False)` | `section not in SERVICE_CHARGE` -> **True** | `ValueError("unknown section")` |
| `bill_total` | `test_bill_invalid_order_negative_food` | `("dine_in", -50, 2, False)` | `food_total < 0` -> **True** | `ValueError("invalid order")` |
| `bill_total` | `test_bill_invalid_order_zero_guests` | `("dine_in", 1000, 0, False)` | `guests < 1` -> **True** | `ValueError("invalid order")` |
| `bill_total` | `test_bill_dine_in_regular` | `("dine_in", 1000, 2, False)` | All checks **False**, `guests >= 8` -> **False** | `1155` |
| `bill_total` | `test_bill_dine_in_happy_hour` | `("dine_in", 1000, 2, True)` | Happy hour **True**, Section != takeaway **True** | `924` (20% discount applied) |
| `bill_total` | `test_bill_takeaway_happy_hour_no_discount` | `("takeaway", 1000, 2, True)` | Happy hour **True**, Section == takeaway -> **False** | `1050` (no discount) |
| `bill_total` | `test_bill_rooftop_happy_hour_large_party` | `("rooftop", 1000, 8, True)` | Happy hour **True**, `guests >= 8` -> **True** | `1176` (15% service + 200 fee) |
| `split_bill` | `test_split_invalid_people` | `(1000, 0, 10)` | `people < 1` -> **True** | `ValueError("invalid people count")` |
| `split_bill` | `test_split_invalid_tip` | `(1000, 4, -5)` | `tip_percent < 0` -> **True** | `ValueError("invalid tip")` |
| `split_bill` | `test_split_even` | `(1000, 4, 10)` | `grand_total % people != 0` -> **False** | `275` (exact split) |
| `split_bill` | `test_split_with_remainder` | `(100, 3, 0)` | `grand_total % people != 0` -> **True** | `34` (rounds up by 1) |
| `table_wait` | `test_table_wait_party_too_large` | `(13, 5, False)` | `party_size > 12` -> **True** | `"call ahead"` |
| `table_wait` | `test_table_wait_has_reservation` | `(6, 0, True)` | `has_reservation` -> **True** | `"seat now"` |
| `table_wait` | `test_table_wait_no_free_tables` | `(4, 0, False)` | `free_tables == 0` -> **True** | `"waitlist"` |
| `table_wait` | `test_table_wait_large_party_one_table` | `(8, 1, False)` | `party_size > 6 and free_tables < 2` -> **True** | `"waitlist"` |
| `table_wait` | `test_table_wait_large_party_multiple_tables` | `(8, 2, False)` | `party_size > 6` **True**, `free_tables < 2` **False** | `"seat now"` |
| `table_wait` | `test_table_wait_small_party_one_table` | `(4, 1, False)` | `party_size > 6` **False** -> default return | `"seat now"` |

---

## 5. Artifacts and Terminal Output Screenshots

The generated terminal screenshots verifying the test suite executions and coverage tables are committed in `LAB6/` and `LAB6/screenshots/`:

1. **Code Coverage Report Screenshot**:
   - Path: [`code_coverage_report.png`](file:///C:/Users/aivil/Downloads/selab6/L6_L7_58_restaurant_bill/LAB6/code_coverage_report.png)
   - Verifies 100% Statement Coverage.
2. **Branch Coverage Report Screenshot**:
   - Path: [`branch_coverage_report.png`](file:///C:/Users/aivil/Downloads/selab6/L6_L7_58_restaurant_bill/LAB6/branch_coverage_report.png)
   - Verifies 100% Branch Coverage across all 22 branches.

---

## 6. How to Re-Run the Tests and Generate Reports

From the `LAB6` directory:

```powershell
# 1. Run line coverage
coverage run -m pytest CodeCoverageTest_restaurant_bill.py
coverage report -m

# 2. Run branch coverage
coverage run --branch -m pytest BranchCoverageTest_restaurant_bill.py
coverage report -m
```
