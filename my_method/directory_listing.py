from .common import os


def directory_listing(
    ext: tuple[str] = (""), exc_ext: tuple[str] = ("")
) -> list[str]:
    """
    カレントディレクトリのリスト化

    Parameters
    ----------
    ext : tuple[str], optional
        拡張子, by default ""
    exc_ext : tuple[str], optional
        除外拡張子, by default ""

    Returns
    -------
    list[str]
        リスト化したディレクトリ一覧
    """
    path = "."
    if ext != (""):
        files = [
            file
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file)) and file.endswith(ext)
        ]
    elif exc_ext != (""):
        files = [
            file
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))
            and not file.endswith(exc_ext)
        ]
    else:
        files = [
            file
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))
        ]
    return files
