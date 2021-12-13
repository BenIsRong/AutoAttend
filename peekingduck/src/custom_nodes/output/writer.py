"""
Node template for creating custom nodes.
"""
import json
from os import path
from typing import Any, Dict
from datetime import datetime

from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    """

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node writes the names to a json file for the API to return.

        Args:
            inputs (dict): Dictionary with keys "str", Any.

        Returns:
            outputs (dict): Empty dictionary.
        """
        with open(path.join(path.realpath(__file__), "..", "..", "..", "..", "temp", "result", f"result.json"), "w") as write_records:
            json.dump({"regs": inputs["names"]}, write_records)
    
        return {}
