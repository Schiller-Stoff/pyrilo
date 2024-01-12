
import xml.etree.ElementTree as ET


def clean_xml_string(xml: str) -> str:
    """
    Replaces double whitespace, \n \t and whitespace before and after "<" or "/>"
    :param xml: xml as string
    :return: cleaned xml.
    """
    # xml = xml.replace("  ", "")
    xml = xml.replace("\n", " ")
    xml = xml.replace("\t", " ")
    xml = xml.replace("  ", " ")
    xml = xml.replace("   ", " ")
    xml = xml.replace(" <", "<")
    xml = xml.replace("< ", "<")
    xml = xml.replace(" />", "/>")
    xml = xml.replace("> ", ">")
    return xml


def parse_xml(xml: str, default_namespaces: {} = None) -> ET.Element:
    """
    Parses given string as xml. Needs namespace declarations. For the default namespace
    just ommit an empty string as key.
    :param xml: xml as string.
    :param default_namespaces: Dictionary of namespaces. Key is the 'shorctut' and value the full resource-link.
    :return:
    """
    # Register default tei namespace first.
    if default_namespaces:
        for key in default_namespaces:
            ET.register_namespace(key, default_namespaces[key])

    tei_string: str = clean_xml_string(xml)
    root: ET.Element = ET.fromstring(tei_string)
    return root

