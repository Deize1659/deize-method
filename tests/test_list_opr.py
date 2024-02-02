from src.my_method.list_opr import ListOpr


def test_element_same_all() -> None:
    assert ListOpr.element_same_all([1, 1, 1]) == True
    assert ListOpr.element_same_all([1, 1, 2]) == False
    assert ListOpr.element_same_all([1, 2, 2]) == False
    assert ListOpr.element_same_all([1, 2, 3]) == False
