from .common import os, re


def directory_listing(
    name: str = "",
    ext: str | tuple[str] = (""),
    exc_ext: str | tuple[str] = (""),
) -> list[str]:
    """
    カレントディレクトリのリスト化

    Parameters
    ----------
    name : str, optional
        正規表現を含めたファイル名, by default ""
    ext : tuple[str], optional
        拡張子, by default ("")
    exc_ext : tuple[str], optional
        除外拡張子, by default ("")

    Returns
    -------
    list[str]
        リスト化したディレクトリ一覧
    """
    path = "."
    if name == "":
        if ext != (""):
            files = [
                file
                for file in os.listdir(path)
                if os.path.isfile(os.path.join(path, file))
                and file.endswith(ext)
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
    else:
        files = [
            file
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))
        ]
        temp = []
        for file in files:
            if re.fullmatch(name, file):
                temp.append(file)
        files = temp
    return files
