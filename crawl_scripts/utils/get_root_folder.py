import os

def get_project_root():
    """Returns the root folder of the current script file."""
    return '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-2])