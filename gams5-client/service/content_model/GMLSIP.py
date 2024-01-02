from service.content_model.SIP import SIP
from service.content_model.SIPMetadata import SIPMetadata
from service.content_model.SIPFileMetadata import SIPFileMetadata
from service.content_model.GAMSXMLNamespaces import GAMSXMLNamespaces
from service.content_model.ContentModels import ContentModels

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

        # add SOURCE.xml as content file
        object_metadata.contentFiles.append(
            SIPFileMetadata(
                # TODO think about actual data assignment
                title="SOURCE", 
                dsid="SOURCE", 
                bagpath="data/content/SOURCE.xml", 
                mimetype="text/xml",
                # TODO add actual size 
                size=9999999,
                # TODO add processing of missing statements! 
                creator=publisher_creator, 
                description="Source GML datastreams", 
                rights="CC BY-SA 4.0", 
                publisher=publisher_creator, 
            )
        )

        return object_metadata

