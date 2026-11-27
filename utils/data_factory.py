import random
import uuid
from dataclasses import dataclass

from config import settings


@dataclass
class TestUser:
    name: str
    email: str
    password: str
    title: str
    birth_day: str
    birth_month: str
    birth_year: str
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: str
    country: str
    state: str
    city: str
    zipcode: str
    mobile_number: str

    def account_payload(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "title": self.title,
            "birth_date": self.birth_day,
            "birth_month": self.birth_month,
            "birth_year": self.birth_year,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "company": self.company,
            "address1": self.address1,
            "address2": self.address2,
            "country": self.country,
            "zipcode": self.zipcode,
            "state": self.state,
            "city": self.city,
            "mobile_number": self.mobile_number,
        }


def unique_email(prefix="qa.user"):
    token = uuid.uuid4().hex[:10]
    return f"{prefix}.{token}@{settings.TEST_EMAIL_DOMAIN}"


def build_user(**overrides):
    token = uuid.uuid4().hex[:6]
    first = random.choice(["Asha", "Ravi", "Maya", "Liam", "Noor"])
    last = random.choice(["Menon", "Patel", "Carter", "Singh", "Okafor"])
    data = dict(
        name=f"{first} {last} {token}",
        email=unique_email(),
        password=settings.TEST_PASSWORD,
        title="Mr",
        birth_day="10",
        birth_month="5",
        birth_year="1990",
        first_name=first,
        last_name=last,
        company="Northwind QA",
        address1="221B Test Street",
        address2="Suite 4",
        country="Canada",
        state="Ontario",
        city="Toronto",
        zipcode="M5V1A1",
        mobile_number="5551234567",
    )
    data.update(overrides)
    return TestUser(**data)
