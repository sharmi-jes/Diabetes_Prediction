import os
import sys
import yaml
from Diabetetic.exception import DiabeteticException
from Diabetetic.logging import logging


# def read_yaml_file(file_path: str) -> dict:
#     """Reads a YAML file and returns its content as a dictionary."""
#     try:
#         with open(file_path, "rb") as yaml_file:
#             return yaml.safe_load(yaml_file)
#     except Exception as e:
#         raise DiabeteticException(e, sys) from e


# def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
#     """Writes a dictionary to a YAML file. Creates directories if necessary."""
#     try:
#         # Ensure the file_path is not a directory
#         if os.path.isdir(file_path):
#             raise DiabeteticException(f"Expected a file but found a directory: {file_path}", sys)

#         if replace:
#             if os.path.exists(file_path):
#                 os.remove(file_path)

#         # Ensure the parent directory exists
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)

#         # Write YAML content with UTF-8 encoding
#         with open(file_path, "w", encoding="utf-8") as file:
#             yaml.dump(content, file, default_flow_style=False)

#     except PermissionError:
#         raise DiabeteticException(f"Permission denied: Unable to write to {file_path}. Try running as administrator.", sys)
#     except Exception as e:
#         raise DiabeteticException(e, sys)


import os
import sys
# from networksecurity.exception import NetworkSecurityException
# from networksecurity.logging import logging
import yaml
import numpy as np
import pickle
# from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import r2_score


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise DiabeteticException(e, sys) from e
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise DiabeteticException(e, sys)