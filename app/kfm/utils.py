# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
from xml.etree import ElementTree as ET

import requests

from app import db
from app.models import User

# Links to files
active_file = 'http://kfm.gov.kz/blacklist/export/active/xml'
included_file = 'http://kfm.gov.kz/blacklist/export/included/xml'
excluded_file = 'http://kfm.gov.kz/blacklist/export/excluded/xml'

# Login and password
LOGIN = os.getenv('KFM_LOGIN', '000940001446')
PASSWORD = os.getenv('KFM_PASSWORD', 'fS2SuCrMFs')

# A link to the login form
ACCESS_URL = 'http://kfm.gov.kz/assets/components/office/action.php?action=auth%2FformLogin&username={}&password={}&pageId=795'
ACCESS_URL = ACCESS_URL.format(LOGIN, PASSWORD)


def get_XML_from_URL(link_to_file):
    """Return XML object from the link."""

    if link_to_file is None:
        raise ValueError('Link to file not found')
    try:
        if 'included' in link_to_file:
            # Use request with session
            with requests.Session() as s:
                headers = {'Cache-Control': 'no-cache'}
                p = s.post(ACCESS_URL, headers=headers)  # login to the web page
                r = s.get(link_to_file)
        else:
            # Use usual request
            r = requests.get(link_to_file)
    except (requests.exceptions.Timeout, requests.exceptions.HTTPError):
        return None
    return ET.fromstring(r.text)


def get_list_from_XML(xml_object, object_type):
    """Loop over XML (xml_object) and find all object_type.
    Return list of dictionaries containing persons or organizatons.
    """

    # Return empty list if xml object is not presented
    if xml_object is None:
        return []

    object_types = {
            'person': ('persons/person',),
            'org': ('organisations/org', 'organisationscis/org')
        }

    # List of 'Element' objects from XML
    list_of_elements = []

    for x in object_types[object_type]:
        list_of_elements.extend(xml_object.findall(x))

    result = []  # list of dictionaries containing persons or organizatons

    if object_type == 'person':
        for prsn in list_of_elements:
            result.append(create_person(prsn))
    elif object_type == 'org':
        for org in list_of_elements:
            result.append(create_org(org))

    return result


def create_person(a_list):
    """Create a dictionary for a person from the list of Elements object."""

    # Pattern for date matching in string.
    # It matches if string is '01.02.2002' or '01.02.02'
    date_pattern = re.compile(r'(\d{2}).(\d{2}).(\d{4}|\d{2})')

    # Create a result dict and set initial sub dict data to None
    result = {
        'lname': None,
        'fname': None,
        'mname': None,
        'iin': None,
        'birthdate': None,
        'included': None,
        'excluded': None
    }

    # Loop over list of Elements. Every Element has 'tag' attribute and 'text'
    for value in a_list:
        # For every string type of data look up for text
        # and add it to the 'result' dict

        if value.tag in ['lname', 'fname', 'mname', 'iin']:
            if value.text is not None:
                result[value.tag] = value.text.strip().upper()

        # If tag is 'birthdate'
        elif value.tag == 'birthdate':
            # then check if it has the text
            if value.text is not None and re.search(date_pattern, value.text):
                result[value.tag] = datetime.strptime(
                        value.text,
                        '%d.%m.%Y'
                    ).date()

        # If tag is 'note' then mazafaka comes :(
        elif value.tag == 'note' and value.text is not None:
            # A 'note' could be anything... let's try convert text to list
            note_list = value.text.split()
            # If the text converted to the list and it has more than 1 value
            if len(note_list) > 1:
                # If list's index 0 value starts with 'вкл' then
                # it means that there is a date of inclusion somewhere in list
                if note_list[0].startswith('вкл'):
                    for x in note_list:
                        # then find a date string using regex
                        if re.search(date_pattern, x):
                            d = datetime.strptime(x[0:10], '%d.%m.%Y').date()
                            result['included'] = d
                if note_list[0].startswith('иск'):
                    for x in note_list:
                        if re.search(date_pattern, x):
                            d = datetime.strptime(x[0:10], '%d.%m.%Y').date()
                            result['excluded'] = d
    return result


def create_org(list_of_elements):
    if list_of_elements is None:
        raise ValueError("List of elements not found.")

    date_pattern = re.compile(r'(\d{2}).(\d{2}).(\d{4}|\d{2})')

    result = {
        'org_name': None,
        'org_name_en': None,
        'included': None,
        'excluded': None
    }

    for val in list_of_elements:
        if val.text is not None:
            if val.tag in ['org_name', 'org_name_en']:
                result[val.tag] = val.text.strip().upper()

            # Grab included and excluded dates
            if val.tag == 'note':
                note_list = val.text.split()
                if len(note_list) > 1:
                    if note_list[0].startswith('вкл'):
                        for x in note_list:
                            if re.search(date_pattern, x):
                                d = datetime.strptime(x[0:10], '%d.%m.%Y').date()
                                result['included'] = d
                    elif note_list[0].startswith('иск'):
                        for x in note_list:
                            if re.search(date_pattern, x):
                                d = datetime.strptime(x[0:10], '%d.%m.%Y').date()
                                result['excluded'] = d
    return result


def request_active(a_type):
    """Create initial list of active"""

    if a_type not in ('person', 'org'):
        raise ValueError("a_type must be person or org")

    # Convert excluded link to XML object
    active_xml = get_XML_from_URL(active_file)

    # Create persons data
    list_of_active = get_list_from_XML(active_xml, a_type)

    return list_of_active


def request_excluded(a_type):

    if a_type not in ('person', 'org'):
        raise ValueError("a_type must be person or org")

    # Convert excluded link to XML object
    excluded_xml = get_XML_from_URL(excluded_file)
    # Create persons data
    list_of_excluded = get_list_from_XML(excluded_xml, a_type)

    return list_of_excluded


def request_included(a_type):

    if a_type not in ('person', 'org'):
        raise ValueError("a_type must be person or org")

    # Convert included link to XML object
    included_xml = get_XML_from_URL(included_file)
    # Create persons data
    list_of_included = get_list_from_XML(included_xml, a_type)

    return list_of_included
