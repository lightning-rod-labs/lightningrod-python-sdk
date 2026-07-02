import os
import sys
import getpass
from pathlib import Path


class LightningrodAuthError(RuntimeError):
    """Raised when required configuration (API key, etc.) is missing and cannot be prompted for."""


def _is_colab_notebook() -> bool:
    """Check if we're running inside a Google Colab notebook."""
    try:
        import google.colab.userdata
    except ImportError:
        return False
    else:
        return True


_DOTENV_LOADED = False


def _load_dotenv_once():
    """Best-effort loader for a project-local .env file.

    Walks up from the current working directory looking for a `.env` file and
    populates `os.environ` with any `KEY=VALUE` lines that aren't already set.
    Runs once per process. Disable with `LIGHTNINGROD_DISABLE_DOTENV=1`.
    """
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return
    _DOTENV_LOADED = True

    if os.environ.get("LIGHTNINGROD_DISABLE_DOTENV"):
        return

    cwd = Path.cwd().resolve()
    for directory in [cwd, *cwd.parents]:
        env_path = directory / ".env"
        if not env_path.is_file():
            continue
        try:
            with env_path.open("r", encoding="utf-8") as fh:
                for raw in fh:
                    line = raw.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
        except OSError:
            pass
        return


def get_config_value(key, default=None, optional=False):
    """
    Portable function to get a value from the environment variables or Google Colab userdata.
    """
    _load_dotenv_once()

    if key in os.environ:
        return os.environ[key]

    if _is_colab_notebook():
        from google.colab import userdata
        from google.colab.userdata import SecretNotFoundError
        try:
            return userdata.get(key)
        except SecretNotFoundError:
            return default

    if default is not None:
        return default

    if optional:
        return None

    # Non-interactive context (agent harness, CI, piped shell): fail fast with a
    # clear error instead of blocking on a getpass prompt that nothing can answer.
    if not sys.stdin.isatty():
        raise LightningrodAuthError(
            f"{key} is not set. Export it in your environment or add it to a "
            f"project-local .env file. Interactive prompts are disabled in "
            f"non-TTY contexts (set LIGHTNINGROD_DISABLE_DOTENV=1 to skip .env autoload)."
        )

    return getpass.getpass(f"Enter the value for {key}: ")