

from dataclasses import dataclass, field
import dataclasses
import json
from service.content_model.SIPFileMetadata import SIPFileMetadata
from typing import List


@dataclass
class SIPMetadata:
    """
    Contains data needed to construct a sip.json describin a digital object.
    """

    id: str
    title: str
    description: str
    creator: str
    rights: str
    publisher: str
    object_type: str = "TEI"
    files: List[SIPFileMetadata] = field(default_factory=list)


    def serialize_to_json(self):
        """
        Serializes this object to json. Corresponds to CERNS sip.json format.
        """
        sip_object_dict = dataclasses.asdict(self)
        return json.dumps(sip_object_dict)
        
        