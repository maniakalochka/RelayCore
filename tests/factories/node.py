import factory

from app.nodes.schemas import NodeCreate


class NodeCreateFactory(factory.Factory):
    class Meta:
        model = NodeCreate

    name = factory.Sequence(lambda n: f"Node {n}")
    host = "1.1.1.1"
    port = 8080
    country_code = "US"
