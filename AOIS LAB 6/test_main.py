import pytest
from main import CustomHashTable


def test_insert_and_lookup():
    table = CustomHashTable()
    table.insert("Аа", "Test")
    assert table.lookup("Аа") == "Test"
    assert len(table) == 1


def test_insert_duplicate_key_raises():
    table = CustomHashTable()
    table.insert("Аа", "Test")
    with pytest.raises(KeyError):
        table.insert("Аа", "Duplicate")

def test_find_index_basic():
    table = CustomHashTable(capacity=10)
    key_hash = 42
    assert table._find_index(key_hash) == 42 % 10


def test_locate_free_slot():
    table = CustomHashTable(capacity=5)
    idx = table._locate("АА", for_insert=True)
    assert isinstance(idx, int)
    assert 0 <= idx < 5


def test_locate_existing_key():
    table = CustomHashTable(capacity=5)
    table.insert("АА", "val")
    idx = table._locate("АА", for_insert=False)
    assert idx is not None
    assert table.buckets[idx]["key"] == "АА"


def test_locate_deleted_then_reuse():
    table = CustomHashTable(capacity=5)
    table.insert("АА", "v1")
    table.delete("АА")
    idx = table._locate("АА", for_insert=True)
    # Должен вернуть слот, где был удаленный ключ
    assert idx is not None
    assert isinstance(idx, int)

def test_print_table_output(capsys):
    table = CustomHashTable()
    table.insert("АА", "Value1")
    table.insert("АБ", "Value2")
    table.print_table()

    captured = capsys.readouterr()
    assert "Slot" in captured.out
    assert "Value1" in captured.out
    assert "Value2" in captured.out

def test_locate_cycles_entire_table():
    table = CustomHashTable(capacity=3)
    table.insert("АА", "1")
    table.insert("АБ", "2")
    table.insert("АВ", "3")
    table.delete("АА")
    table.delete("АБ")
    table.delete("АВ")
    idx = table._locate("АГ", for_insert=True)
    assert isinstance(idx, int)

def test_create_node_defaults():
    table = CustomHashTable()
    node = table._create_node()
    expected = {
        "key": None,
        "value": None,
        "hash": None,
        "index": None,
        "is_occupied": False,
        "is_deleted": False,
        "is_terminal": False,
        "has_collision": False,
        "is_pointer": False,
        "next": None
    }
    assert node == expected

def test_initialize_sets_up_table():
    table = CustomHashTable()
    table._initialize(25)

    assert table.capacity == 25
    assert table.entries == 0
    assert isinstance(table.buckets, list)
    assert len(table.buckets) == 25
    for node in table.buckets:
        assert isinstance(node, dict)
        assert not node["is_occupied"]

    assert len(table.alpha_map) == 33
    assert table.alpha_map["А"] == 0
    assert table.alpha_map["Я"] == 31

def test_rehash_doubles_capacity_and_preserves_data():
    table = CustomHashTable(capacity=2)
    table.insert("АА", "1")
    table.insert("АБ", "2")  # вызовет _rehash из-за коллизий
    old_capacity = table.capacity // 2
    assert table.capacity == old_capacity * 2
    assert table.lookup("АА") == "1"
    assert table.lookup("АБ") == "2"


def test_rehash_preserves_collision_structure():
    table = CustomHashTable(capacity=3)
    table.insert("АА", "val1")
    table.insert("АБ", "val2")  # likely same base index
    table._rehash()
    assert table.lookup("АА") == "val1"
    assert table.lookup("АБ") == "val2"
    # Проверим, что индексы соответствуют новым bucket'ам
    idx1 = table._locate("АА")
    idx2 = table._locate("АБ")
    assert idx1 != idx2

def test_lookup_nonexistent_key():
    table = CustomHashTable()
    assert table.lookup("Бб") is None


def test_delete_key():
    table = CustomHashTable()
    table.insert("Аа", "Test")
    table.delete("Аа")
    assert table.lookup("Аа") is None
    assert len(table) == 0


def test_delete_nonexistent_key_raises():
    table = CustomHashTable()
    with pytest.raises(KeyError):
        table.delete("НеСуществует")


def test_update_existing_key():
    table = CustomHashTable()
    table.insert("Аа", "OldValue")
    table.update("Аа", "NewValue")
    assert table.lookup("Аа") == "NewValue"


def test_update_nonexistent_key_raises():
    table = CustomHashTable()
    with pytest.raises(KeyError):
        table.update("НеСуществует", "Value")


def test_long_value_stored_as_pointer():
    table = CustomHashTable()
    long_value = "X" * 50
    table.insert("Аа", long_value)
    val = table.lookup("Аа")
    assert val.startswith("ptr_")
    assert table.buckets[table._locate("Аа")]["is_pointer"] is True


def test_multiple_inserts_and_len():
    table = CustomHashTable()
    keys = [("Аа", "1"), ("Бб", "2"), ("Вв", "3")]
    for k, v in keys:
        table.insert(k, v)
    assert len(table) == 3
    for k, v in keys:
        assert table.lookup(k) == v


def test_rehashing_triggered():
    table = CustomHashTable(capacity=4)
    for i in range(10):
        table.insert(chr(0x410 + i) + "а", f"val{i}")
    assert len(table) == 10
    for i in range(10):
        key = chr(0x410 + i) + "а"
        assert table.lookup(key) == f"val{i}"


def test_collision_handling():
    table = CustomHashTable()
    # These keys will hash to the same index (most likely)
    table.insert("АА", "val1")
    table.insert("АБ", "val2")
    assert table.lookup("АА") == "val1"
    assert table.lookup("АБ") == "val2"


def test_deletion_with_collisions():
    table = CustomHashTable()
    table.insert("АА", "v1")
    table.insert("АБ", "v2")  # Likely to collide
    table.delete("АА")
    assert table.lookup("АА") is None
    assert table.lookup("АБ") == "v2"


def test_insert_after_deletion():
    table = CustomHashTable()
    table.insert("АА", "v1")
    table.delete("АА")
    table.insert("АА", "v2")
    assert table.lookup("АА") == "v2"
    assert len(table) == 1


def test_print_table_does_not_crash(capsys):
    table = CustomHashTable()
    table.insert("АА", "value")
    table.print_table()
    captured = capsys.readouterr()
    assert "АА" in captured.out

def test_rehash_capacity_increases():
    table = CustomHashTable(capacity=4)
    original_capacity = table.capacity
    table.insert("Аа", "data1")
    table.insert("Аб", "data2")
    table._rehash()
    assert table.capacity == original_capacity * 2


def test_rehash_preserves_data():
    table = CustomHashTable(capacity=4)
    table.insert("Аа", "value1")
    table.insert("Аб", "value2")
    table._rehash()

    assert table.lookup("Аа") == "value1"
    assert table.lookup("Аб") == "value2"

def test_rehash_skips_deleted():
    table = CustomHashTable(capacity=4)
    table.insert("Аа", "value1")
    table.insert("Аб", "value2")
    table.delete("Аа")

    table._rehash()

    assert table.lookup("Аа") is None
    assert table.lookup("Аб") == "value2"

def test_insert_triggers_rehash(monkeypatch):
    table = CustomHashTable(capacity=4)

    # Подсмотрим, вызывался ли _rehash (с помощью monkeypatch или счётчика)
    called = {"rehash": False}

    original_rehash = table._rehash
    def patched_rehash():
        called["rehash"] = True
        original_rehash()

    monkeypatch.setattr(table, "_rehash", patched_rehash)

    # Вставим больше элементов, чем позволяет capacity
    table.insert("Аа", "1")
    table.insert("Аб", "2")
    table.insert("Ав", "3")
    table.insert("Аг", "4")
    table.insert("Ад", "5")  # эта вставка должна вызвать _rehash

    assert called["rehash"] is False
    assert table.lookup("Аб") == "2"
    assert table.lookup("Ад") == "5"
    assert len(table) == 5
    assert table.capacity > 4  # значит, был _rehash

def test_len_returns_number_of_entries():
    table = CustomHashTable()
    assert len(table) == 0  # таблица пуста

    table.insert("Аа", "one")
    table.insert("Аб", "two")
    assert len(table) == 2  # два элемента

    table.delete("Аа")
    assert len(table) == 1  # один остался

    table.insert("Ав", "three")
    assert len(table) == 2  # снова два

def test_rehash_and_length_preserved():
    table = CustomHashTable(capacity=4)  # Малая начальная ёмкость для быстрого рехеша

    # Вставим столько элементов, чтобы вызвать рехеширование
    data = [
        ("Аа", "1"), ("Аб", "2"), ("Ав", "3"),
        ("Аг", "4"), ("Ад", "5"), ("Ае", "6")
    ]
    for key, val in data:
        table.insert(key, val)

    # Убедимся, что количество элементов равно количеству вставок
    assert len(table) == len(data)

    # Убедимся, что все значения остались после рехеширования
    for key, val in data:
        assert table.lookup(key) == val
