import uuid

from lyrid import Address


def random_string() -> str:
    return uuid.uuid4().hex


def random_address() -> Address:
    return Address(f"$.tester.{random_string()}")


def random_url() -> str:
    return f"https://example.com/{random_string()}"


def random_html_content() -> str:
    return f"<html>{random_string()}</html>"
