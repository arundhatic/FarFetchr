import pytest
from utils import haversine, clean_address

def test_haversine_known_points():
    # San Francisco (lat, lon) and Palo Alto (lat, lon)
    sf = (37.7897, -122.3941)
    pa = (37.4449, -122.1617)
    miles, km = haversine(sf[0], sf[1], pa[0], pa[1])
    assert abs(miles - 27.0) < 1
    assert abs(km - 43.5) < 1

def test_haversine_identical_points():
    miles, km = haversine(0, 0, 0, 0)
    assert miles == pytest.approx(0, abs=1e-5)
    assert km == pytest.approx(0, abs=1e-5)

def test_haversine_antipodal():
    miles, km = haversine(0, 0, 0, 180)
    assert abs(round(km) - 20015) < 10
    assert abs(round(miles) - 12436) < 10

def test_clean_address_suite_and_commas():
    assert clean_address('415 Mission St Suite 4800, San Francisco, CA 94105') == '415 Mission St'
    assert clean_address('123 Main St, Suite 2, City, State') == '123 Main St'

def test_clean_address_extra_commas():
    assert clean_address('123 Main St,,, City, State,') == '123 Main St, City, State'

def test_clean_address_no_cleaning():
    assert clean_address('456 Elm St, Springfield, IL') == '456 Elm St, Springfield, IL'

def test_clean_address_odd_punctuation():
    assert clean_address('789 Oak St... City, State') == '789 Oak St... City, State'
    assert clean_address('789 Oak St, , , City, State') == '789 Oak St, City, State'

def test_clean_address_trims_whitespace():
    assert clean_address('   123 Main St, City, State   ') == '123 Main St, City, State' 