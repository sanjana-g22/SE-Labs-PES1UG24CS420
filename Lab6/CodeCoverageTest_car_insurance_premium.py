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