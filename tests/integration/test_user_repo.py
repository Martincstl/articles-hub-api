from app.models.user import User
from app.repositories import UserRepository


def test_user_repository_lookup_and_exists(db_session) -> None:
    repo = UserRepository(db_session)

    user = User(
        email="demo@example.com",
        username="demo_user",
        password_hash="hashed_password",
    )
    repo.add(user)
    repo.flush()

    assert repo.exists_by_email("demo@example.com") is True
    assert repo.exists_by_username("demo_user") is True

    found = repo.get_by_email("demo@example.com")
    assert found is not None
    assert found.id == user.id