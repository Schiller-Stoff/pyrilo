from dataclasses import dataclass
from typing import List

@dataclass
class DigitalObject:
    """
    Represents a digital object returned by the gams-api.
    """

    id: str
    """
    Id of a digital object e.g. demo1 or o:demo.1 
    """

    project: str
    """
    Project abbreviation = id of a GAMS project e.g. 'demo'
    """

    datastreams: List[str]
    """
    List of datastreams contained by the digital object, e.g. TEI_SOURCE and IMG.1.
    """

    # child_objects: List[str]


