from ingest.content_model.SIP import SIP
from ingest.content_model.SIPMetadata import SIPMetadata
from ingest.content_model.SIPFileMetadata import SIPFileMetadata
from ingest.content_model.GAMSXMLNamespaces import GAMSXMLNamespaces
from ingest.content_model.ContentModels import ContentModels

class GMLSIP(SIP):
    """
    Operates on the transformation from SIP to bags. (and preprocessing)
    Handles all GML related operations, like extracting pid from a GML document.
    """

    def __init__(self, project_abbr: str, sip_folder_path: str, subtype: str = "") -> None:
        SIP.__init__(self, project_abbr, sip_folder_path, subtype)


    def extract_metadata(self) -> SIPMetadata:
        """
        Extracts metadata from a TEI document.

        """

        pid_xpath = ".//gdas:PID"
        id = self.XML_ROOT.find(pid_xpath, GAMSXMLNamespaces.GML_NAMESPACES).text

        title_xpath = ".//gml:name"
        title = self.XML_ROOT.find(title_xpath, GAMSXMLNamespaces.GML_NAMESPACES).text

        description = f"Places for {title}"

        publisher_creator = f"{self.PROJECT_ABBR} GAMS project"

        object_metadata = SIPMetadata(
            id=id, 
            title=title, 
            creator=publisher_creator, 
            description=description,
            object_type=ContentModels.GML, 
            publisher=publisher_creator, 
            rights="CC BY-SA 4.0",
            types=[self.SUBTYPE],
            contentFiles=[],
        )

        # resolve files as datastreams
        files_dict = self.resolve_datastream_files()
        for key in files_dict.keys():
            object_metadata.contentFiles.append(files_dict[key])

        return object_metadata

