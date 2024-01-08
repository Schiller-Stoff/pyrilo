from typing import Final

class GAMSXMLNamespaces:
    """
    Defines namespaces for GAMS source documents.
    """

    GML_NAMESPACES: Final = {
        "xml": "http://www.w3.org/XML/1998/namespace",
        "gml": "http://www.opengis.net/gml", 
        "gdas": "http://cm4f.org/gdas/",
        "derla": "https://gams.uni-graz.at/o:derla.ontology#"
    }

    TEI_NAMESPACES: Final = {
        "xml": "http://www.w3.org/XML/1998/namespace",
        "": "http://www.tei-c.org/ns/1.0",
        "t": "http://www.tei-c.org/ns/1.0",
        "tei": "http://www.tei-c.org/ns/1.0",
    }

    SKOS_NAMESPACES: Final = {
        "xml": "http://www.w3.org/XML/1998/namespace",
        "skos":"http://www.w3.org/2004/02/skos/core#",
        "dc11": "http://purl.org/dc/elements/1.1/",
        "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
    }