import pytest
from string_utils import StringUtils

# экземпляр класса для тестирования
string_utils = StringUtils()


# ==================== ТЕСТЫ ДЛЯ CAPITALIZE ====================

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("skypro", "Skypro"),
    ("hello world", "Hello world"),
    ("python", "Python"),
    ("test", "Test"),
])
def test_capitalize_positive(input_str, expected):
    """Позитивные тесты для capitalize."""
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("123abc", "123abc"),
    ("", ""),
    ("   ", "   "),
    ("Test", "Test"),  # Уже начинается с заглавной
])
def test_capitalize_negative(input_str, expected):
    """Негативные тесты для capitalize."""
    assert string_utils.capitalize(input_str) == expected


# ==================== ТЕСТЫ ДЛЯ TRIM ====================

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("   skypro", "skypro"),
    ("  hello", "hello"),
    ("   test string", "test string"),
    ("   ", ""),
])
def test_trim_positive(input_str, expected):
    """Позитивные тесты для trim."""
    assert string_utils.trim(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("skypro   ", "skypro   "),  # Пробелы в конце не удаляются
    ("", ""),
    ("skypro", "skypro"),  # Без пробелов в начале
    ("\ttext", "\ttext"),  # Табуляция не удаляется
])
def test_trim_negative(input_str, expected):
    """Негативные тесты для trim."""
    assert string_utils.trim(input_str) == expected


# ==================== ТЕСТЫ ДЛЯ CONTAINS ====================

@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "S", True),
    ("SkyPro", "k", True),
    ("SkyPro", "y", True),
    ("Hello World", " ", True),
])
def test_contains_positive(string, symbol, expected):
    """Позитивные тесты для contains."""
    assert string_utils.contains(string, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "U", False),
    ("", "a", False),
    ("test", "T", False),  # Регистрозависимость
    ("hello", "world", False),
])
def test_contains_negative(string, symbol, expected):
    """Негативные тесты для contains."""
    assert string_utils.contains(string, symbol) == expected


# ==================== ТЕСТЫ ДЛЯ DELETE_SYMBOL ====================

@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "k", "SyPro"),
    ("SkyPro", "Pro", "Sky"),
    ("hello world", " ", "helloworld"),
    ("aaaa", "a", ""),
])
def test_delete_symbol_positive(string, symbol, expected):
    """Позитивные тесты для delete_symbol."""
    assert string_utils.delete_symbol(string, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "X", "SkyPro"),  # Символа нет в строке
    ("test", "", "test"),  # Пустая подстрока
    ("", "a", ""),  # Пустая исходная строка
    ("Hello", "hello", "Hello"),  # Регистрозависимость
])
def test_delete_symbol_negative(string, symbol, expected):
    """Негативные тесты для delete_symbol."""
    assert string_utils.delete_symbol(string, symbol) == expected


# ==================== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ====================

class TestEdgeCases:
    """Тесты граничных случаев."""

    @pytest.fixture
    def utils(self):
        return StringUtils()

    def test_capitalize_edge_cases(self, utils):
        """Граничные случаи для capitalize."""
        # Строка с пробелом в начале
        assert utils.capitalize(" skypro") == " skypro"
        # Строка с цифрой в начале
        assert utils.capitalize("1test") == "1test"
        # Специальные символы
        assert utils.capitalize("@test") == "@test"

    def test_trim_edge_cases(self, utils):
        """Граничные случаи для trim."""
        # Один пробел
        assert utils.trim(" text") == "text"
        # Много пробелов
        assert utils.trim("      text") == "text"
        # Смешанные пробельные символы
        assert utils.trim("\n text") == "\n text"  # Перенос строки сохраняется

    def test_contains_edge_cases(self, utils):
        """Граничные случаи для contains."""
        # Пустая строка и пустой символ
        assert utils.contains("", "") == True
        # Непустая строка и пустой символ
        assert utils.contains("abc", "") == True
        # Длинная подстрока
        assert utils.contains("hello world", "hello world") == True

    def test_delete_symbol_edge_cases(self, utils):
        """Граничные случаи для delete_symbol."""
        # Удаление всех символов
        assert utils.delete_symbol("aaaaa", "a") == ""
        # Удаление с перекрытием
        assert utils.delete_symbol("aaa", "aa") == "a"
        # Специальные символы
        assert utils.delete_symbol("a@b#c", "@") == "ab#c"


# ==================== ТЕСТЫ ИСКЛЮЧЕНИЙ ====================

def test_contains_with_exception():
    """Тест, проверяющий обработку исключений в contains."""
    # contains должен корректно обрабатывать случай, когда symbol не найден
    # через try/except блок
    result = string_utils.contains("test", "x")
    assert result == False

    # Должен возвращать True, если символ найден
    result = string_utils.contains("test", "t")
    assert result == True


def test_delete_symbol_does_nothing_when_symbol_not_found():
    """Тест, проверяющий, что delete_symbol не меняет строку, если символ не найден."""
    original = "Hello World"
    result = string_utils.delete_symbol(original, "x")
    assert result == original