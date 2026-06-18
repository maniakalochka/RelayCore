import pytest

from app.nodes.schemas import NodeCreate
from app.nodes.service import NodeService


@pytest.mark.asyncio
async def test_can_create_node(mocker):
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

    result = await service.create_node(data)

    assert result == node

    mock_repo.create.assert_awaited_once_with(data)
    publisher.publish_health_check.assert_awaited_once_with(node.id)
