import uuid

import pytest

from app.auth import User
from app.auth.enums import UserRole
from app.nodes.schemas import NodeCreate
from app.nodes.service import NodeService


@pytest.mark.asyncio
async def test_admin_can_create_node(mocker):
    mock_repo = mocker.Mock()

    node = mocker.Mock()
    node.id = "node-id"

    mock_repo.create = mocker.AsyncMock(return_value=node)

    publisher = mocker.Mock()
    publisher.publish_health_check = mocker.AsyncMock()

    service = NodeService(
        repository=mock_repo,
        health_check_service=mocker.Mock(),
        publisher=publisher,
    )

    data = NodeCreate(
        name="Test Node",
        host="1.1.1.1",
        port=8080,
        country_code="US",
    )
    admin = User(
        id=uuid.uuid4(),
        email="johndoe@gmail.com",
        hashed_password="hashedpassword",  # S106
        is_active=True,
        is_verified=True,
        role=UserRole.ADMIN,
        first_name="John",
        last_name="Doe",
    )

    result = await service.create_node(data, admin)

    assert result == node

    mock_repo.create.assert_awaited_once_with(data)
    publisher.publish_health_check.assert_awaited_once_with(node.id)


@pytest.mark.asyncio
async def test_common_user_cannot_create_node(mocker):
    mock_repo = mocker.Mock()

    node = mocker.Mock()
    node.id = "node-id"

    mock_repo.create = mocker.AsyncMock(return_value=node)

    publisher = mocker.Mock()
    publisher.publish_health_check = mocker.AsyncMock()

    service = NodeService(
        repository=mock_repo,
        health_check_service=mocker.Mock(),
        publisher=publisher,
    )

    data = NodeCreate(
        name="Test Node",
        host="1.1.1.1",
        port=8080,
        country_code="US",
    )
    admin = User(
        id=uuid.uuid4(),
        email="johndoe@gmail.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
        role=UserRole.USER,
        first_name="John",
        last_name="Doe",
    )
    with pytest.raises(PermissionError):
        await service.create_node(data, admin)
