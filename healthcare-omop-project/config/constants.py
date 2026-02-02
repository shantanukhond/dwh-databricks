""" Global constants and lookup values """

AUTHOR = "SHANTANU KHOND"
VERSION = "1.0.0"

# Date formats
DATE_FORMATS = {
    "standard": "%Y-%m-%d",
    "timestamp": "%Y-%m-%d %H:%M:%S",
    "iso": "%Y-%m-%dT%H:%M:%S.%fZ"
}

# Regex patterns
VALIDATION_PATTERNS = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "phone": r"^\+?1?\d{9,15}$",
    "zip_code": r"^\d{5}(-\d{4})?$"
}