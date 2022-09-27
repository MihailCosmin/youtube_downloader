from os.path import sep

def clean_path(path: str) -> str:
    """clean_path by replacing all backslashes with standard os path separator

    Args:
        path (str): path to clean

    Returns:
        str: cleaned path
    """
    return path.replace("\\\\", sep).replace("\\", sep).replace("/", sep)
