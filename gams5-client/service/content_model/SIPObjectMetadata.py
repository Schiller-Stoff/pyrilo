

from dataclasses import dataclass, field
from service.content_model.SIPDatastreamMetadata import SIPDatastreamMetadata
from typing import List


@dataclass
class SIPObjectMetadata:
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
    files: List[SIPDatastreamMetadata] = field(default_factory=list)