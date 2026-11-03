import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# ---------- Starter example tests ----------
def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_no_bonus():
    assert no_claim_bonus(0) == 0


# ---------- annual_premium: error handling ----------
def test_unknown_car_type_raises():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 0, False)


def test_driver_too_young_raises():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)


# ---------- annual_premium: age loadings ----------
def test_young_driver_surcharge():
    # hatchback 8000 + 4000 = 12000 ; no claims -> -2400 = 9600
    assert annual_premium("hatchback", 22, 0, False) == 9600


def test_senior_driver_surcharge():
    # suv 15000 + 2000 = 17000 ; no claims -> -3400 = 13600
    assert annual_premium("suv", 65, 0, False) == 13600


# ---------- annual_premium: claims and anti-theft ----------
def test_many_claims_doubles_premium():
    # sedan 12000 ; 3 claims -> 24000
    assert annual_premium("sedan", 30, 3, False) == 24000


def test_anti_theft_discount():
    # hatchback 8000 ; no claims -> 6400 ; anti-theft -> 5900
    assert annual_premium("hatchback", 30, 0, True) == 5900


# ---------- no_claim_bonus ----------
def test_bonus_negative_years_raises():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


def test_bonus_five_years():
    assert no_claim_bonus(5) == 50


def test_bonus_three_years():
    assert no_claim_bonus(3) == 35


def test_bonus_one_year():
    assert no_claim_bonus(1) == 20


# ---------- claim_payout ----------
def test_payout_negative_damage_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-100, 500000, 5000, False)


def test_payout_total_loss():
    assert claim_payout(10000, 500000, 5000, True) == 500000


def test_payout_below_deductible():
    assert claim_payout(3000, 500000, 5000, False) == 0


def test_payout_normal():
    assert claim_payout(20000, 500000, 5000, False) == 15000


def test_payout_capped_at_insured_value():
    assert claim_payout(600000, 500000, 5000, False) == 500000


# ================= EXTRA TESTS FOR BRANCH COVERAGE =================

# ---------- annual_premium: age boundaries (neither surcharge branch) ----------
def test_middle_age_no_surcharge():
    # hatchback 8000 ; age 25 -> no surcharge ; 1 claim -> unchanged
    assert annual_premium("hatchback", 25, 1, False) == 8000


def test_age_exactly_18_is_young_surcharge():
    # sedan 12000 + 4000 = 16000 ; 1 claim -> unchanged
    assert annual_premium("sedan", 18, 1, False) == 16000


def test_age_24_is_young_surcharge():
    assert annual_premium("sedan", 24, 1, False) == 16000


def test_age_59_no_senior_surcharge():
    assert annual_premium("sedan", 59, 1, False) == 12000


def test_age_exactly_60_is_senior_surcharge():
    # sedan 12000 + 2000 = 14000 ; 1 claim -> unchanged
    assert annual_premium("sedan", 60, 1, False) == 14000


# ---------- annual_premium: claims boundaries (neither claims branch) ----------
def test_one_claim_no_change():
    assert annual_premium("suv", 30, 1, False) == 15000


def test_two_claims_no_change():
    assert annual_premium("suv", 30, 2, False) == 15000


def test_three_claims_with_anti_theft():
    # suv 15000 -> x2 = 30000 -> -500 = 29500
    assert annual_premium("suv", 30, 3, True) == 29500


# ---------- no_claim_bonus: boundaries ----------
def test_bonus_zero_boundary_zero_years():
    assert no_claim_bonus(0) == 0


def test_bonus_four_years():
    assert no_claim_bonus(4) == 35


def test_bonus_two_years():
    assert no_claim_bonus(2) == 20


def test_bonus_many_years():
    assert no_claim_bonus(10) == 50


# ---------- claim_payout: remaining branches ----------
def test_payout_negative_deductible_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(1000, 500000, -1, False)


def test_payout_damage_equals_deductible():
    assert claim_payout(5000, 500000, 5000, False) == 0


def test_payout_exactly_insured_value():
    # payout == insured_value -> not capped, returned as is
    assert claim_payout(505000, 500000, 5000, False) == 500000


def test_payout_total_loss_ignores_deductible():
    assert claim_payout(0, 300000, 5000, True) == 300000