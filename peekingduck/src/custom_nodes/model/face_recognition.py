"""
Node template for creating custom nodes.
"""

import numpy as np
import numpy.typing as npt
import requests
import glob
import cv2
from os import path
from typing import Any, Dict, List, Tuple
from peekingduck.pipeline.nodes.node import AbstractNode
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials



def get_faces(bbox: List[float], image: npt.NDArray[np.float64], image_size: Tuple[int, int]) -> List[str]:
    faces = []
    for index, box in enumerate(bbox):
        img_path = path.join(path.realpath(__file__), "..", "..", "..", "..", "temp", "images", f"face_{index}.jpg")
        print(f"img_path: {img_path}")
        x1, y1, x2, y2 = box
        x1 *= image_size[0]
        x2 *= image_size[0]
        y1 *= image_size[1]
        y2 *= image_size[1]
        face = image[int(y1):int(y2), int(x1):int(x2)]
        cv2.imwrite(img_path, face)
        faces.append(img_path)
    return faces

class Node(AbstractNode):
    """
    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        

    def run(self, inputs: Dict[str, Any]) -> Dict[str, List[str]]:  # type: ignore
        """This node gets the names of the people found in the input.

        Args:
            inputs (dict): Dictionary with keys "str", "Any".

        Returns:
            outputs (dict): Dictionary with keys "names".
        """

        person_group_id = "autoattend"
        endpoint = "https://autoattend.cognitiveservices.azure.com/"
        key = "32cd204c1b7f4bbe98a67cd7dae08cc7"
        face_client = FaceClient(endpoint, CognitiveServicesCredentials(key))
        #TODO
        # - write image with cv2 to path
        # - use path to read image using glob

        img = inputs["img"]
        bboxes = inputs["bboxes"]
        faces_path = get_faces(bboxes, img, (img.shape[1], img.shape[0]))
        names = []
        for face_path in faces_path:
            image = open(glob.glob(face_path)[0], 'r+b')
            faces = face_client.face.detect_with_stream(image, detection_model='detection_03')
            face_ids = [face.face_id for face in faces]

            results = face_client.face.identify(face_ids, person_group_id)
            for person in results:
                if len(person.candidates) > 0:
                    response = requests.get(f"{endpoint}face/v1.0/persongroups/{person_group_id}/persons/{person.candidates[0].person_id}", headers={"Ocp-Apim-Subscription-Key": key})
                    response = response.json()
                    names.append(response["name"])

        outputs = {"names": names}
        return outputs
