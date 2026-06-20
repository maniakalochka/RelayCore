from app.auth.enums.user_role import UserRole
from app.nodes.enums.node_visibility import NodeVisibility
from app.nodes.models.node import Node


class NodeAccessPolicy:
    @staticmethod
    def can_access_node(user_role: UserRole, node: Node) -> bool:
        if user_role == UserRole.ADMIN:
            return True

        if user_role == UserRole.USER:
            return node.visibility in {
                NodeVisibility.PUBLIC,
                NodeVisibility.USER,
            }

        return False
