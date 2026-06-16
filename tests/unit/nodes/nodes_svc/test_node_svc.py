import pytest

from app.nodes.service import NodeService


@pytest.mark.asyncio
async def test_list_available_nodes_returns_active_nodes(mocker):
    mock_repository = mocker.Mock()
    nodes = [mocker.Mock(), mocker.Mock()]
    mock_repository.list_active = mocker.AsyncMock(return_value=nodes)

    service = NodeService(repository=mock_repository)

    result = await service.list_available_nodes()

    assert result == nodes
    mock_repository.list_active.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_list_all_nodes_returns_all_nodes(mocker):
    mock_repository = mocker.Mock()
    nodes = [mocker.Mock(), mocker.Mock()]
    mock_repository.list_all_nodes = mocker.AsyncMock(return_value=nodes)

    service = NodeService(repository=mock_repository)

    result = await service.list_all_nodes()

    assert result == nodes
    mock_repository.list_all_nodes.assert_awaited_once_with()
