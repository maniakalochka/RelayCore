import uuid

import factory

from app.auth import User
from app.auth.enums import UserRole


class UserFactory(factory.Factory):
    class Meta:
        model = User

    class Params:
        admin = factory.Trait(
            role=UserRole.ADMIN,
        )

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    hashed_password = "test"
    is_active = True
    is_verified = True
    role = UserRole.USER
    first_name = "John"
    last_name = "Doe"
