# Copyright (c) 2021 Nicolas Riquet (MIT license)

"""
This module contains the unit tests for the "utilities" module. 
"""

import pytest, utilities
from config import config_params
from typing import Callable, Dict

@pytest.fixture
def utilities_SATD_fixture() -> Dict[str, str]:
    """
    This test fixture sets variables for SATD detection unit tests.
    """
    
    return {
        "SATD_keywords": config_params["SATD_keywords"],
        "modified_lines_with_SATD": [
            {"added": [(1, "if (method.nloc >= max_method_CCN): #TODO : fix nloc bug")]},
            {"added": [(2, "if (method.nloc >= max_method_CCN): //TO DO : fix nloc bug")]},
            {"added": [(3, "if (method.nloc >= max_method_CCN): #fix me : fix nloc bug")]},
            {"added": [(4, "if (method.nloc >= max_method_CCN)://fixme : fix nloc bug")]},
            {"added": [(5, "if (method.nloc >= max_method_CCN)://to fix tofix : fix nloc bug")]},
            {"added": [(6, "if (method.nloc >= max_method_CCN):#    fixme : fix nloc bug")]}],
        "modified_lines_without_SATD": [
            {"added": [(1, "if (method.nloc >= max_method_CCN)")]},
            {"added": [(2, "if (method.nloc >= max_method_CCN)")]},
            {"added": [(3, "if (method.nloc >= max_method_CCN)")]},
            {"added": [(4, "if (method.nloc >= max_method_CCN)// test")]},
            {"added": [(5, "if (method.nloc >= max_method_CCN)")]},
            {"added": [(6, "if (method.nloc >= max_method_CCN):#     : fix nloc bug")]}]
    }


@pytest.fixture
def utilities_bugfix_fixture() -> Dict[str, str]:
    """
    This test fixture sets variables for bugfix detection unit tests.
    """
    
    return {
        "bugfix_keywords": config_params["bugfix_keywords"],
        "messages_with_bugfix": [
            "Solved bug 332",
            "Fixed problem",
            "Defect 778 corrected"],
        "messages_without_bugfix": [
            "Hello world"
            "implemented feature 654",
            "Changed error message",
            "Added documentation"]
    }


def test_utilities_is_SATD_Yes(utilities_SATD_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that GitDelver detects SATD when one of the SATD keywords is used.
    """
    
    for dict_of_modified_lines in utilities_SATD_fixture["modified_lines_with_SATD"]:
        contains_SATD, SATDLine = utilities.is_SATD(utilities_SATD_fixture["SATD_keywords"], dict_of_modified_lines)
        
        assert contains_SATD is True
        assert SATDLine == dict_of_modified_lines["added"][0][1]


def test_utilities_is_SATD_No(utilities_SATD_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that GitDelver does not detect SATD when none of the SATD keywords are used.
    """
    
    for dict_of_modified_lines in utilities_SATD_fixture["modified_lines_without_SATD"]:
        contains_SATD, SATDLine = utilities.is_SATD(utilities_SATD_fixture["SATD_keywords"], dict_of_modified_lines)
        
        assert contains_SATD is False
        assert SATDLine == ""


def test_utilities_is_bugfix_Yes(utilities_bugfix_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that GitDelver detects bug fixes when one of the bugfix keywords is used.
    """
    
    for message in utilities_bugfix_fixture["messages_with_bugfix"]:
        is_bugfix = utilities.is_bugfix(utilities_bugfix_fixture["bugfix_keywords"], message)
        
        assert is_bugfix is True


def test_utilities_is_bugfix_No(utilities_bugfix_fixture: Callable[[None], Dict[str, str]]):
    """
    This unit test checks that GitDelver does not detect bug fixes when none of the bug fix keywords are present.
    """

    for message in utilities_bugfix_fixture["messages_without_bugfix"]:
        is_bugfix = utilities.is_bugfix(utilities_bugfix_fixture["bugfix_keywords"], message)
        
        assert is_bugfix is False


def test_utilities_change_type_as_string():
    """
    This unit test checks that GitDelver correctly returns PyDriller's ModificationType enum values as strings.
    """

    change_types = ["ModificationType.ADD",
                    "ModificationType.COPY",
                    "ModificationType.RENAME",
                    "ModificationType.DELETE",
                    "ModificationType.MODIFY",
                    "ModificationType.UNKNOWN"]
    
    results = []
    
    for change in change_types:
        results.append(utilities.change_type_as_string(change))
    
    assert results[0] == "ADD"
    assert results[1] == "COPY"
    assert results[2] == "RENAME"
    assert results[3] == "DELETE"
    assert results[4] == "MODIFY"
    assert results[5] == "UNKNOWN"


def test_utilities_get_file_type_Production():
    """
    This unit test checks that GitDelver returns "Production" when the file name does not contain "test".
    """

    file_name = "Employee.java"
    
    assert utilities.get_file_type(file_name) == "Production"


def test_utilities_get_file_type_Test1():
    """
    This unit test checks that GitDelver returns "Test" when the file name contains "test".
    """

    file_name = "EmployeeTest.java"
    
    assert utilities.get_file_type(file_name) == "Test"


def test_utilities_get_file_type_Test2():
    """
    This unit test checks that GitDelver returns "Test" when the file name contains "test".
    """

    file_name = "EmployeeTestOfTheMonth.java"
    
    assert utilities.get_file_type(file_name) == "Test"


def test_utilities_keyword_match_found_Yes():
    """
    This unit test checks that GitDelver returns True when "string" contains one of the words
    in keywords_list.
    """

    keywords_list = ["java"]
    
    string = "toto.java"
    
    assert utilities.keyword_match_found(keywords_list, string) is True


def test_utilities_keyword_match_found_No():
    """
    This unit test checks that GitDelver returns False when "string" does not contain one of
    the words in keywords_list.
    """

    keywords_list = ["java"]
    
    string = "toto.cs"
    
    assert utilities.keyword_match_found(keywords_list, string) is False

