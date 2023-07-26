def input_int(print_str: str) -> int:
    """
    int入力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    int
        入力数字
    """
    while True:
        try:
            num = int(input(print_str + "入力:"))
            if input(print_str + f":{num}[Yn]:").lower() == "y":
                break
        except ValueError:
            pass
    return num


def input_float(print_str: str) -> float:
    """
    float入力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    float
        入力数字
    """
    while True:
        try:
            num = float(input(print_str + "入力:"))
            if input(print_str + f":{num}[Yn]:").lower() == "y":
                break
        except ValueError:
            pass
    return num


def input_str(print_str: str) -> str:
    """
    文字列出力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    str
        入力文字列
    """
    while True:
        try:
            sec = input(print_str + "入力:")
            if input(print_str + f":{sec}[Yn]:").lower() == "y":
                break
        except ValueError:
            pass
    return sec
