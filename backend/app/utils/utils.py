from typing import Dict, List
from app.models import User, Doctor
import re
from flask import jsonify
from http import HTTPStatus

def query_builder(data: Dict[str, str], query_type: str, queried_param: str) -> List[User]:
    """
    Constructs and executes a database query on the User model based on the specified query type and parameter.

    Parameters:
    - data (Dict[str, str]): A dictionary containing the data to be queried, typically including user attributes like 'ssn'.
    - query_type (str): The type of query to perform. It can be 'all', 'one', or 'first', determining the method of retrieval.
    - queried_param (str): The key in the data dictionary that specifies which attribute to filter by, e.g., 'ssn'.

    Returns:
    - List[User]: A list of User objects that match the query criteria. The list may contain one or more users, or be empty.
    
    The function supports three query types:
    - 'all': Retrieves all User records matching the specified parameter.
    - 'one': Retrieves exactly one User record matching the specified parameter, raising an error if none or more than one is found.
    - 'first': Retrieves the first User record matching the specified parameter, or None if no match is found.
    """

    if query_type == "all":
        query = User.query.filter_by(ssn=data[queried_param]).all()
    elif query_type == "one":
        query = User.query.filter_by(ssn=data[queried_param]).one()
    elif query_type == "first":
        query = User.query.filter_by(ssn=data[queried_param]).first()
    
    return query

    
def parse_phone_number(phone: str) -> str:
    """
    Parses a phone number string by removing non-numeric characters and validating its length.
    
    The function supports two formats:
    - 10-digit numbers, which are returned as-is.
    - 12-digit numbers starting with '91', which are considered valid and returned without the '91' prefix.
    
    Parameters:
    - phone (str): The phone number string to be parsed.

    Returns:
    - str: A cleaned and validated phone number string, or None if the number is invalid.
    """

    # Remove all non-numeric characters
    cleaned_phone = re.sub(r'\D', '', phone)

    # Check if the cleaned phone number has a valid length (e.g., 10 digits for numbers without area code)
    if len(cleaned_phone) == 10:
        return cleaned_phone
    # Consider numbers with a leading '91' area code as valid
    elif len(cleaned_phone) == 12 and cleaned_phone[:2] == "91":
        return cleaned_phone[2:]
    else:
        return None
    

def create_error_response(message: str, status_code: int) -> tuple[Dict, int]:
    """Create standardized error response"""
    return jsonify({
        "status": "error",
        "response": message
    }), status_code


def create_success_response(message: str, status_code: int) -> tuple[Dict, int]:
    """Create standardized success response"""
    return jsonify({
        "status": "success",
        "response": message
    }), status_code


def fetch_all_doctors():
    """
    Logic to fetch/get all the doctors in the system.
    """
    try:
        doctors = Doctor.query.all()
        
        doctors_data = [{
            "id": doctor.id,
            "name": doctor.name,
            "specialties": doctor.specialties
        } for doctor in doctors]
        
        return create_success_response(
            doctors_data,
            HTTPStatus.OK
        )

    except Exception as e:
        return create_error_response(
            "Internal server error",
            HTTPStatus.INTERNAL_SERVER_ERROR
        )


def validate_phone_number(phone_number: str) -> str:
    """
    Validates and parses a phone number.

    Args:
        phone_number (str): The phone number to validate and parse.

    Returns:
        str: The parsed phone number.

    Raises:
        ValueError: If the phone number is invalid or cannot be parsed.
    """
    phone = parse_phone_number(phone_number)
    if phone is None:
        raise ValueError("Phone number cannot be null")
    return phone

