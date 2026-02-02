import os
import getpass

try:
    from google.colab import userdata
    from google.colab.userdata import NotebookAccessError
except ImportError:
    is_colab_env = False
else:
    is_colab_env = True


def get_config_value(key, default=None):
    """
    Check in to env
    if not found check in to google colab userdata, if available
    else asks for that key, will be presented as ****
    """
    if key in os.environ:
        return os.environ[key]
    
    if is_colab_env:
        try:        
            return userdata.get(key)
        except NotebookAccessError as nae:
            raise nae
        except Exception:
            pass
    
    if default is not None:
        return default

    # Ask the user for the value if not found
    return getpass.getpass(f"Enter the value for {key}: ")