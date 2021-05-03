
def test_user_exists(db):
    assert db.user.user_exists("user1@email.com") == True


def test_user_not_exists(db):
    assert db.user.user_exists("fake@email.com") == False


def test_authenticate_valid_user(db):
    assert db.user.authenticate_user("user1@email.com", "password") == "user_1"
