from datetime import datetime
import re
from extract.GAMSXMLNamespaces import GAMSXMLNamespaces
from extract.TEISIP import TEISIP
from extract.GMLSIP import GMLSIP
from extract.SubInfoPackService import SubInfoPackService
from PyriloStatics import PyriloStatics
from PIL import Image
from typing import List, Dict
import os
import logging
import json
import fasttext


class DerlaSIPRefiner:
    """
    Handles / controls the data refinement operations for the DERLA project.

    """

    PROJECT_ABBREVIATION = "demo"

    def __init__(self):
        subinfo_pack_service = SubInfoPackService(self.PROJECT_ABBREVIATION)
        subinfo_pack_service.walk_sip_folder(lambda_func=self.process_sip_folder)
        subinfo_pack_service.walk_sip_folder(lambda_func=self.process_perslist_sip, pattern="perslist", content_model="tei")
        subinfo_pack_service.walk_sip_folder(lambda_func=self.process_gml_sip, pattern="placelist", content_model="gml")


    def process_sip_folder(self, sip_folder_path, source_file_path, folder_pattern: str, folder_name: str, content_model: str):
        """
        Demo lambda function for processing a SIP folder. (for DERLA)
        """
        
        # creates thumbnails for the sips
        self.generate_thumbnail(sip_folder_path)    

        # creates search.json files for the sips
        self.generate_search_json(sip_folder_path)

        # project worker needs to decide which content model to use.
        # tei_service = TEIService(MY_PROJECT, source_file_path, sip_folder_path)

    
    def process_perslist_sip(self, sip_folder_path: str, source_file_path: str, folder_pattern: str, folder_name: str, content_model: str):
        """
        Processes a perslist SIP folder.
        """

        # reading in machine learning model (needed later for word embeddings)
        model_path = './models/cc.de.20.bin'
        model = fasttext.load_model(model_path)
        
        persons = []

        tei_sip = TEISIP(self.PROJECT_ABBREVIATION, sip_folder_path)
        object_id = tei_sip.resolve_pid()

        # get all person elements
        person_elems = tei_sip.XML_ROOT.findall(".//listPerson/person", GAMSXMLNamespaces.TEI_NAMESPACES)

        for person_elem in person_elems:
            # get the person id
            person_id = person_elem.get("{http://www.w3.org/XML/1998/namespace}id")

            # get the person name
            person_name_surname = person_elem.find("persName/surname", GAMSXMLNamespaces.TEI_NAMESPACES).text
            # get the person description
            person_name_forename = person_elem.find("persName/forename", GAMSXMLNamespaces.TEI_NAMESPACES).text

            # person types
            person_term_elems = person_elem.findall("listEvent//event/label/term", GAMSXMLNamespaces.TEI_NAMESPACES)
            person_types = ["person"]
            for person_term_elem in person_term_elems:
                person_types.append(person_term_elem.text)

            # add description
            desc_elem = person_elem.find("listEvent/head/desc", GAMSXMLNamespaces.TEI_NAMESPACES)
            if desc_elem is None:
                raise Exception(f"Person description element is missing in TEI SIP. {tei_sip.SIP_FOLDER_PATH}")

            person_desc = desc_elem.text

            # add birthdate
            birthdate_elem = person_elem.find("birth/date", GAMSXMLNamespaces.TEI_NAMESPACES)
            birthdate = self.transform_to_solr_date(birthdate_elem.text if birthdate_elem is not None else "01.01.2023"	 )


            # add deathdate
            deathdate_elem = person_elem.find("death/date", GAMSXMLNamespaces.TEI_NAMESPACES)
            deathdate = self.transform_to_solr_date(deathdate_elem.text if deathdate_elem is not None else "01.01.2023"	 )

            # word embeddings for person description
            word_embeddings = {}
            try:
                # word embeddings for person name
                word_embeddings = self.calculate_word_embeddings(person_desc, model)
            except ReferenceError:
                msg = f"Failed to calculate word embeddings for person {person_id}. {ReferenceError}"
                logging.info(msg)
                raise ReferenceError(msg)

            for word in word_embeddings:
                word_id = person_id + "_" + word

                word_dict = {}

                # word_dict["pid"] = digital_object_pid
                # word_dict["project_abbr"] = "admin"
                word_dict["id"] = word_id
                word_dict["pers_id_s"] = person_id
                word_dict["types"] = "word-vector"
                word_dict["word_s"] = word
                # numpy array needs to be converted to list for json serialization later on
                word_dict["vector"] = word_embeddings[word].tolist()

                persons.append(word_dict)



            # create a person dict
            person = {
                "id": f"{object_id}_{person_id}",
                "surname": person_name_surname,
                "firstname": person_name_forename,
                "types": person_types,
                "desc": person_desc,
                "birthdate": birthdate,
                "deathdate": deathdate
            }


            # add the person dict to the persons list
            persons.append(person)

        self.generate_search_index_json(persons, sip_folder_path)

        
    
    def generate_thumbnail(self, sip_folder_path: str):
        """
        Generates a thumbnail for a given sip folder if 
        """
        try:
            EXPECTED_IMAGE_FILE_PATH = os.path.join(sip_folder_path, PyriloStatics.THUMBNAIL_SIP_SOURCE_FILE_NAME)
            image = Image.open(EXPECTED_IMAGE_FILE_PATH)
            image.thumbnail((90,90))
            image.save(os.path.join(sip_folder_path, PyriloStatics.THUMBNAIL_FILE_NAME))
        except FileNotFoundError:
            logging.info(f"No image found in SIP folder at expected location for thumbnail generation: {EXPECTED_IMAGE_FILE_PATH}.")
            pass
        except IOError:
            logging.info(f"Failed to create thumbnail for SIP {sip_folder_path} {IOError}")
            pass


    def generate_search_json(self, sip_folder_path: str):
        """
        Generates a search.json file for a given SIP folder.
        """

        tei_sip = TEISIP(self.PROJECT_ABBREVIATION, sip_folder_path)
        # default operations provided by the TEISIP
        title = tei_sip.resolve_title()
        id = tei_sip.resolve_pid()
        desc = tei_sip.resolve_sip_description()
        types = tei_sip.resolve_terms()
        # DERLA specific operations
        location = self.extract_geo_location(tei_sip)
        creation_date = self.extract_creation_date(tei_sip)
        # extracting fulltext field
        fulltext = tei_sip.extract_full_text()

        # solr dict to be written to json file
        search_data = [{
            "title": title,
            "id": id,
            "desc": desc,
            "types": types,
            "location": location,
            "creation_date_dt": creation_date,
            "_fulltext": fulltext,
            # needs to be assigned if the index of an object is being overwritten
            "_type": PyriloStatics.INTEGRATION_API_OBJECT_TYPE
        }]

        self.generate_search_index_json(search_data, sip_folder_path)

    
    def extract_geo_location(self, tei_sip: TEISIP):
        """
        Extracts the geo location from a DERLA TEISIP object.
        """
        geo_elems = tei_sip.XML_ROOT.findall(".//geo", GAMSXMLNamespaces.TEI_NAMESPACES)

        if len(geo_elems) < 2:
            raise Exception(f"Not enough geo elements found in TEI SIP. {tei_sip.SIP_FOLDER_PATH}")
        
        if geo_elems[0].text is None or geo_elems[1].text is None:
            raise Exception(f"Geo elements in TEI SIP are empty. {tei_sip.SIP_FOLDER_PATH}")

        return f"{geo_elems[0].text},{geo_elems[1].text}" 


    def extract_creation_date(self, tei_sip: TEISIP):
        """
        Extracts the creation date from a DERLA TEISIP object.
        """

        creation_date_elem = tei_sip.XML_ROOT.find(".//date[@type='creation']", GAMSXMLNamespaces.TEI_NAMESPACES)

        creation_date = "01.01.2023"
        # check if tei element is not none and if the text is not none
        if creation_date_elem is not None:
            if creation_date_elem.text is not None:
                creation_date = creation_date_elem.text

        # if creation date is none, we set it to a default value
        if creation_date is None:
            creation_date = "01.01.2023"

        return self.transform_to_solr_date(creation_date)
    

    def generate_search_index_json(self, entries: List[Dict[str, str]], sip_folder_path: str):
        """
        Generates a search index json file for a given list of dicts at given sip_folder_path
        :param entries: list of dicts containing the search index entries
        :param sip_folder_path: path to the sip folder
        """
        # TODO validate the entries here?
        # TODO validate muts contain id / _id?

        search_json_path = os.path.join(sip_folder_path, PyriloStatics.SIP_SEARCH_JSON_FILE_NAME)
        with open(search_json_path, "w", encoding="utf-8") as search_file:
            # setting ensure ascii to false to allow umlauts
            json.dump(entries, search_file, indent=4, ensure_ascii=False)

        logging.info(f"Generated search.json file for SIP at {search_json_path}.")


    def transform_to_solr_date(self, date: str):
        """
        Transforms a date string to a solr date string.
        """

        # also assigns a default date if missing
        if date is None:
            date = "01.01.2023"

        # if the creation date is only a year, we add a default month and day
        if len(date) == 4:
            date = f"01.01.{date}"

        input_format = "%d.%m.%Y"
        output_format = "%Y-%m-%dT%H:%M:%SZ"

        # Convert input date string to a datetime object
        try:
            parsed_date = datetime.strptime(date, input_format)
        except ValueError:
            logging.error(f"Failed to parse date string {date} with format {input_format}. Appliying default value 01.01.2023.")
            parsed_date = datetime.strptime("01.01.2023", input_format)

        # Format the datetime object in the desired output format
        solr_date = parsed_date.strftime(output_format)

        return solr_date
    

    def calculate_word_embeddings(self, text: str, model):
        """
        Calculates word embeddings for given text.
        :param text: text to calculate word embeddings for.
        :param model: fasttext model to use for word embeddings.
        :return: dict containing the word embeddings for the given text.
        :raises ReferenceError: if text is None.
        """
        
        if text is None:
            msg = "Text is None. Cannot calculate word embeddings."
            logging.error(msg)
            raise ReferenceError(msg)

        words = self.tokenize_text(text)
        # logging.debug(f"Tokenized text: {words}")
        embeddings_dict = {}
        for word in words:
            # Get the fasttext embedding for the word
            embedding = model.get_word_vector(word)
            embeddings_dict[word] = embedding

        return embeddings_dict
    
    
    def tokenize_text(self, text: str):
        """
        Tokenizes given text.
        :param text: text to tokenize.
        :return:
        """
        pattern = r'\w+'
        tokens = re.findall(pattern, text.lower())  # Convert to lowercase to handle case-insensitivity
        return tokens


    def process_gml_sip(self, sip_folder_path, source_file_path, folder_pattern: str, folder_name: str, content_model: str):
        """

        """

        gml_sip = GMLSIP(self.PROJECT_ABBREVIATION, sip_folder_path)
        gml_metadata = gml_sip.extract_metadata()

        # get all placename elements
        place_elems = gml_sip.XML_ROOT.findall(".//derla:placeOfRemembrance", GAMSXMLNamespaces.GML_NAMESPACES)

        places: List[Dict[str, str]] = []


        # reading in machine learning model (needed later for word embeddings)
        model_path = './models/cc.de.20.bin'
        model = fasttext.load_model(model_path)

        for place_elem in place_elems:
            # get the placename id
            place_id = place_elem.find("gdas:ref", GAMSXMLNamespaces.GML_NAMESPACES).text

            place_title = place_elem.find("gdas:title", GAMSXMLNamespaces.GML_NAMESPACES).text

            description = place_elem.find("gdas:desc", GAMSXMLNamespaces.GML_NAMESPACES).text            

            # sentence embeddings for placename description
            description_vector = model.get_sentence_vector(description)


            # create a placename dict
            placename = {
                "id": f"{place_id}_gml",
                "source_id_s": place_id,
                "vector": description_vector.tolist(),
                "types": "description-vector",
                "title": place_title    
                # "name": placename_name,
                # "desc": placename_desc,
                # "type": placename_type,
                # "coordinates": placename_coordinates
            }

            # add the placename dict to the placenames list
            places.append(placename)

        self.generate_search_index_json(places, sip_folder_path)
