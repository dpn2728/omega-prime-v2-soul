# utils.py (The Royal Archives v3.0 - Final)
import json
import logging
import os
import gzip
import aiofiles
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path

# --- Custom Exception Hierarchy ---
class UtilsError(Exception): pass
class FileIOError(UtilsError): pass
class JSONProcessingError(UtilsError): pass

def _get_logger():
    return logging.getLogger("RoyalArchives_v3")

def save_to_json(data: Dict[str, Any], file_path: str, compress: bool = False) -> bool:
    """
    Atomically saves a dictionary to a JSON file, with optional gzip compression.
    Includes versioning and timestamp metadata.
    """
    logger = _get_logger()
    path = Path(file_path)
    
    try:
        # Directory Auto-Creation
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        full_data = {
            "metadata": {
                "version": "1.0",
                "saved_at_utc": datetime.now(timezone.utc).isoformat()
            },
            "data": data
        }

        temp_path = path.with_suffix(f"{path.suffix}.tmp")
        
        # Atomic Write
        if compress:
            with gzip.open(temp_path, 'wt', encoding='utf-8') as f:
                json.dump(full_data, f, ensure_ascii=False, indent=4)
        else:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(full_data, f, ensure_ascii=False, indent=4)
        
        os.replace(temp_path, path)
        logger.debug(f"Successfully saved data to {path}")
        return True
    except (IOError, TypeError) as e:
        logger.critical(f"CRITICAL I/O ERROR saving to {path}: {e}")
        raise FileIOError(e)
    except Exception as e:
        logger.error(f"An unexpected error occurred during save: {e}")
        return False

def load_from_json(file_path: str, compressed: bool = False) -> Optional[Dict[str, Any]]:
    """

    Loads data from a JSON file, with optional gzip decompression.
    Returns the content of the 'data' key.
    """
    logger = _get_logger()
    path = Path(file_path)
    try:
        if compressed:
            with gzip.open(path, 'rt', encoding='utf-8') as f:
                full_data = json.load(f)
        else:
            with open(path, 'r', encoding='utf-8') as f:
                full_data = json.load(f)
        return full_data.get("data")
    except FileNotFoundError:
        logger.warning(f"File not found: '{path}'. Returning None.")
        return None
    except (json.JSONDecodeError, gzip.BadGzipFile):
        logger.error(f"Could not decode file: '{path}'. It may be corrupt. Returning None.")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during load: {e}")
        return None

# --- Async Versions for non-blocking I/O ---
async def save_to_json_async(data: Dict[str, Any], file_path: str):
    logger = _get_logger()
    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        full_data = {"metadata": {"version":"1.0"}, "data": data} # Simplified for async
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(full_data, ensure_ascii=False, indent=4))
    except Exception as e:
        logger.error(f"Async save failed for {path}: {e}")

async def load_from_json_async(file_path: str) -> Optional[Dict[str, Any]]:
    logger = _get_logger()
    path = Path(file_path)
    try:
        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content).get("data")
    except FileNotFoundError:
        return None
    except Exception:
        return None
