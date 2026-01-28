from dataclasses import dataclass


@dataclass
class Project:
    """
    Represents a GAMS project
    """

    projectAbbr: str
    """
    Project abbreviation = id of a GAMS project e.g. 'demo'
    """

    description: str
    """
    Description of a GAMS project
    """