import pytest

from app.nodes.service import NodeService


@pytest.mark.asyncio
async def test_list_available_nodes_returns_active_nodes(mocker):
    mock_repository = mocker.Mock()
    nodes = [mocker.Mock(), mocker.Mock()]
    mock_repository.list_available = mocker.AsyncMock(return_value=nodes)

    service = NodeService(repository=mock_repository)

    result = await service.list_available_nodes()

    assert result == nodes
    mock_repository.list_available.assert_awaited_once_with()
