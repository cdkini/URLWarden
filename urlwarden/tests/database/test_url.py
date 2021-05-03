import pytest

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
    a: str = db.url._sanitize("www.google.com")
    assert a == "google.com"


def test_sanitize_http(db):
    b: str = db.url._sanitize("http://google.com")
    assert b == "google.com"


def test_sanitize_https(db):
    c: str = db.url._sanitize("https://google.com")
    assert c == "google.com"


def test_sanitize_https_and_www(db):
    d: str = db.url._sanitize("https://www.google.com")
    assert d == "google.com"


def test_encode_hash(db):
    a: str = db.url._encode("abcd1234", "www.github.com", 8)
    assert a == "LNdf10VL"


def test_encode_consistency(db):
    b: str = db.url._encode("abcd1234", "www.github.com", 8)
    c: str = db.url._encode("abcd1234", "www.github.com", 8)
    assert b == c


def test_encode_same_url(db):
    d: str = db.url._encode("abcd1234", "www.github.com", 8)
    e: str = db.url._encode("efgh5678", "www.github.com", 8)
    assert d != e


def test_encode_same_user(db):
    f: str = db.url._encode("abcd1234", "www.github.com", 8)
    g: str = db.url._encode("abcd1234", "www.facebook.com", 8)
    assert f != g
