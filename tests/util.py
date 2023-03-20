import uuid

from lyrid import Address


def random_string() -> str:
    return uuid.uuid4().hex


def random_address() -> Address:
    return Address(f"$.tester.{random_string()}")
