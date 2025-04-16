import os

def get_media_folder() -> str:
    full =  os.path.dirname(os.path.abspath(__file__))
    folders = full.split(os.sep)
    folders.remove('utils')
    folders.append('media')
    path = f"{os.sep}".join(folders)
    return path
