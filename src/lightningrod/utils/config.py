import os
import getpass
from lightningrod._display import _is_notebook

def get_config_value(key, default=None):
    """
    Portable function to get a value from the environment variables or Google Colab userdata.
    """
    if key in os.environ:
        return os.environ[key]
    
    if _is_notebook():
        from google.colab import userdata
        return userdata.get(key)
    
    if default is not None:
        return default

    # Ask the user for the value if not found
    return getpass.getpass(f"Enter the value for {key}: ")