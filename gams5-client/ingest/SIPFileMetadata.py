

from dataclasses import dataclass


@dataclass
class SIPFileMetadata:
    """
    Represents metadata for individual datastreams / files in a SIP folder.
    """
    
    size: str
    bagpath: str
    dsid: str
    mimetype: str
    title: str
    description: str
    creator: str
    rights: str
    publisher: str
