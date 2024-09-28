import os
from typing import Optional

def is_running_in_colab() -> bool:
    """Check if the code is running in Google Colab."""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def save_to_storage(filename: str, content: str) -> Optional[str]:
    """
    Save content to a file, handling both Colab and local environments.
    
    Args:
        filename (str): The name of the file to save.
        content (str): The content to write to the file.
    
    Returns:
        Optional[str]: The path where the file was saved, or None if in Colab (where it's downloaded).
    """
    if is_running_in_colab():
        try:
            from google.colab import files
            with open(filename, 'w') as f:
                f.write(content)
            files.download(filename)
            print(f"File '{filename}' has been downloaded in Colab.")
            return None
        except Exception as e:
            print(f"Error saving file in Colab: {e}")
            return None
    else:
        try:
            # For non-Colab environments, save to the current working directory
            filepath = os.path.join(os.getcwd(), filename)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"File saved locally at: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving file locally: {e}")
            return None

def load_from_storage(filename: str) -> Optional[str]:
    """
    Load content from a file, handling both Colab and local environments.
    
    Args:
        filename (str): The name of the file to load.
    
    Returns:
        Optional[str]: The content of the file, or None if the file couldn't be loaded.
    """
    if is_running_in_colab():
        try:
            from google.colab import files
            uploaded = files.upload()
            if filename in uploaded:
                content = uploaded[filename].decode('utf-8')
                print(f"File '{filename}' has been uploaded and read in Colab.")
                return content
            else:
                print(f"File '{filename}' was not uploaded.")
                return None
        except Exception as e:
            print(f"Error loading file in Colab: {e}")
            return None
    else:
        try:
            filepath = os.path.join(os.getcwd(), filename)
            with open(filepath, 'r') as f:
                content = f.read()
            print(f"File loaded locally from: {filepath}")
            return content
        except Exception as e:
            print(f"Error loading file locally: {e}")
            return None