import pytest

from app.nodes.service import NodeService
from factories.node import NodeCreateFactory
from factories.user import UserFactory


@pytest.mark.asyncio
async def test_admin_can_create_node(mocker):
    repo = mocker.Mock()
    node = mocker.Mock()
    node.id = "node-id"
    repo.create = mocker.AsyncMock(return_value=node)

    publisher = mocker.Mock()
    publisher.publish_health_check = mocker.AsyncMock()

    service = NodeService(
        repository=repo,
        health_check_service=mocker.Mock(),
        publisher=publisher,
    )

    data = NodeCreateFactory()
    admin = UserFactory(admin=True)

    result = await service.create_node(data, admin)  # type: ignore

    assert result == node
