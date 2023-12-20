

from dataclasses import dataclass, field
import dataclasses
import json
from service.content_model.SIPFileMetadata import SIPFileMetadata
from typing import List
import copy


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
    # content model of the object
    object_type: str
    # types like TEI, TEIPerslist, TEIManuscript, TEIManuscriptPage, TEIManuscriptPageImage
    types: List[str] = field(default_factory=list)

    # needs to be named in camelCase otherwise there will be a serialization error 
    contentFiles: List[SIPFileMetadata] = field(default_factory=list)


    def serialize_to_json(self):
        """
        Serializes this object to json. Corresponds to CERNS sip.json format.
        Changes the keys to correspond to the sip.json schema.
        """
        sip_object_dict = dataclasses.asdict(self)

        # add static fields
        sip_object_dict["$schema"] = "https://gitlab.cern.ch/digitalmemory/sip-spec/-/blob/master/sip-schema-d1.json"
        sip_object_dict["created_by"] = "Pyrilo"
        sip_object_dict["source"] = "local"
        sip_object_dict["recid"] = self.id
        sip_object_dict["objectType"] = self.object_type

        # rewrite keys to correspond to the sip.json schema 
        sip_object_dict.pop("id")
        # rewrite keys to correspond to the sip.json schema
        sip_object_dict.pop("object_type")

        return json.dumps(sip_object_dict)
        
        