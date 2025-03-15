import smtplib

import pytest


# @pytest.fixture(scope="module")
# def smtp_connection(request):
#     server = getattr(request.module, "smtpserver", "smtp.gmail.com")
#     smtp_connection = smtplib.SMTP(server, 587, timeout=5)
#     yield smtp_connection
#     print(f"finalizing {smtp_connection} ({server})")
#     smtp_connection.close()

def pytest_addoption(parser):
    parser.addoption(
        "--stringinput",
        action="append",
        default=[],
        help="list of stringinputs to pass to test functions",
    )


def pytest_generate_tests(metafunc):
    if "stringinput" in metafunc.fixturenames:
        metafunc.parametrize("stringinput", metafunc.config.getoption("stringinput"))

def idfn(fixture_value):
    if fixture_value == "smtp.gmail.com":
        return "GMAIL"
    else:
        return "PYTHON"

@pytest.fixture(scope="module", params=["smtp.gmail.com", pytest.param("mail.python.org", marks=pytest.mark.skip)], ids=idfn )
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print(f"finalizing {smtp_connection}")
    smtp_connection.close()