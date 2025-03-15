from emaillib import Email, MailAdminClient

import pytest

X = 1

@pytest.fixture
def mail_admin():
    return MailAdminClient()


@pytest.fixture
def sending_user(mail_admin):
    user = mail_admin.create_user()
    print(X)
    yield user
    mail_admin.delete_user(user)


@pytest.fixture
def receiving_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    user.clear_mailbox()
    mail_admin.delete_user(user)

def test_email_received(sending_user, receiving_user):
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(email, receiving_user)
    assert email in receiving_user.inbox

@pytest.fixture
def receiving_user1(mail_admin, request):
    user = mail_admin.create_user()

    def delete_user():
        mail_admin.delete_user(user)

    request.addfinalizer(delete_user)
    return user

@pytest.fixture
def email(sending_user, receiving_user1, request):
    _email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(_email, receiving_user1)

    def empty_mailbox():
        receiving_user1.clear_mailbox()

    request.addfinalizer(empty_mailbox)
    return _email

@pytest.mark.new
def test_email_received1(receiving_user1, email):
    assert email in receiving_user1.inbox