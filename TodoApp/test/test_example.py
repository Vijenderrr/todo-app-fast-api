
import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3!= 1


def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)


def test_boolean():
    validate =True
    assert validate is True
    assert ('hello' == 'world') is False


def test_type():
    assert type(10) == int
    assert type('hello') == str


def test_greater_or_less_than():
    assert 5 > 3
    assert 2 < 4

def test_list():
    num_list = [1,2,3,4,5]
    any_list = [1, 'hello', 3.14, True]
    assert 1 in num_list
    assert 'hello' in any_list
    assert 10 not in num_list



class Student:
    def __init__(self, first_name:str, last_name: str, major: str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('john', 'Doe', 'Computer Science', 3)


#this is how we do without fixtures.

# def test_person_initialization():
#     p = Student('john', 'Doe', 'Computer Science', 3),
#     assert p.first_name == 'john', 'First name is John'
#     assert p.last_name == 'Doe', 'Last name is Doe'
#     assert p.major == 'Computer Science', 'Major is Computer Science'
#     assert p.years == 3, 'Years is 3'

def test_person_initialization_with_fixture(default_employee):
    assert default_employee.first_name == 'john', 'First name is John'
    assert default_employee.last_name == 'Doe', 'Last name is Doe'
    assert default_employee.major == 'Computer Science', 'Major is Computer Science'
    assert default_employee.years == 3, 'Years is 3'