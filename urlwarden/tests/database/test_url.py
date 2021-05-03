from datetime import datetime

import mongomock
import pytest
from passlib.hash import pbkdf2_sha256


def test_add_url_to_valid_user(db):
    assert db.url.add_url("user_2", "www.google.com") == None


def test_add_url_to_invalid_user(db):
    with pytest.raises(Exception):
        db.url.add_url("fake_user", "www.google.com")


def test_get_existant_url(db):
    assert db.url.get_url("abc123") == "www.google.com"


def test_get_nonexistant_url(db):
    with pytest.raises(Exception):
        db.url.get_url("fake_url")


def test_sanitize_www(db):
    """ Should remove a preceding 'www.' """
    a = db.url._sanitize("www.google.com")
    assert a == "google.com"


def test_sanitize_http(db):
    """ Should remove a preceding 'http://' """
    b = db.url._sanitize("http://google.com")
    assert b == "google.com"


def test_sanitize_https(db):
    """ Should remove a preceding 'https://' """
    c = db.url._sanitize("https://google.com")
    assert c == "google.com"


def test_sanitize_https_and_www(db):
    """ Should remove any preceding values """
    d = db.url._sanitize("https://www.google.com")
    assert d == "google.com"


def test_encode_hash(db):
    """ Should properly encode in base62 """
    a = db.url._encode("abcd1234", "www.github.com", 8)
    assert a == "LNdf10VL"


def test_encode_consistency(db):
    """ Should encode the same given the same input """
    b = db.url._encode("abcd1234", "www.github.com", 8)
    c = db.url._encode("abcd1234", "www.github.com", 8)
    assert b == c


def test_encode_same_url(db):
    """ Should encode same site differently with different users """
    d = db.url._encode("abcd1234", "www.github.com", 8)
    e = db.url._encode("efgh5678", "www.github.com", 8)
    assert d != e


def test_encode_same_user(db):
    """ Should encode same user differently with different sites """
    f = db.url._encode("abcd1234", "www.github.com", 8)
    g = db.url._encode("abcd1234", "www.facebook.com", 8)
    assert f != g
