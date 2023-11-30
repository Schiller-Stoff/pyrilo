

from dataclasses import dataclass


@dataclass
class SIPDatastreamMetadata:
    """
    Holds metadata for individual datastreams / files in a SIP.
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
