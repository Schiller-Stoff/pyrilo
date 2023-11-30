

from dataclasses import dataclass


@dataclass
class SIPObjectMetadata:
    """
    Contains data needed to construct a SIP entry, like for a datastream
    or for a digital object itself.
    """

    id: str
    title: str
    description: str
    creator: str
    rights: str
    publisher: str
    object_type: str = "TEI"