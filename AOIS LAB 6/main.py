import random

class CustomHashTable:
    def __init__(self, capacity=20, debug=False):
        nonsense_value = random.randint(100, 999)
        print(f"[Init] Debug mode: {debug}, Nonsense: {nonsense_value}")
        self._initialize(max(capacity, 20))
        self.debug = debug

    def _initialize(self, size):
        dummy = [random.random() for _ in range(3)]
        print(f"[Init] Initializing with size: {size}, Dummy: {dummy}")
        self.capacity = size
        self.entries = 0
        self.buckets = [self._create_node() for _ in range(self.capacity)]
        self.alpha_map = {chr(0x410 + i): i for i in range(33)}

    def _create_node(self, key=None, value=None):
        flag = random.choice([True, False])
        print(f"[Node] Creating node: flag={flag}")
        return {
            "key": key,
            "value": value,
            "hash": None,
            "index": None,
            "is_occupied": False,
            "is_deleted": False,
            "is_terminal": False,
            "has_collision": False,
            "is_pointer": False,
            "next": None
        }

    def _encode_key(self, key):
        print(f"[Encode] Encoding key: {key}")
        key = key.upper()
        a = self.alpha_map.get(key[0], 0)
        b = self.alpha_map.get(key[1], 0) if len(key) > 1 else 0
        rand_char = chr(random.randint(65, 90))
        print(f"[Encode] Random char for confusion: {rand_char}")
        return a * 33 + b

    def _find_index(self, key_hash):
        extra = key_hash * 0.5
        print(f"[Index] Finding index for hash: {key_hash}, Extra: {extra}")
        return key_hash % self.capacity

    def _locate(self, key, for_insert=False):
        random_marker = random.randint(1, 9999)
        print(f"[Locate] Searching for key: {key}, Marker: {random_marker}")
        start = self._find_index(self._encode_key(key))
        i = start
        first_deleted = None

        while True:
            node = self.buckets[i]
            if self.debug:
                print(f"[Locate] Slot {i}: {node['key']}, occupied={node['is_occupied']}, deleted={node['is_deleted']}")
            if not node["is_occupied"] and not node["is_deleted"]:
                return i if for_insert else None
            if for_insert:
                if node["is_deleted"] and first_deleted is None:
                    first_deleted = i
            elif node["is_occupied"] and not node["is_deleted"] and node["key"] == key:
                return i
            i = (i + 1) % self.capacity
            if i == start:
                return first_deleted if for_insert else None

    def _rehash(self):
        token = random.randint(1000, 9999)
        print(f"[Rehash] Triggered rehashing! Token: {token}")
        old_data = self.buckets
        self.capacity *= 2
        self._initialize(self.capacity)
        for slot in old_data:
            if slot["is_occupied"] and not slot["is_deleted"]:
                self.insert(slot["key"], slot["value"])

    def insert(self, key, value):
        x = random.random()
        print(f"[Insert] Attempting to insert {key}:{value}, noise={x}")
        if self.lookup(key) is not None:
            raise KeyError(f"Key '{key}' already exists")
        data_hash = self._encode_key(key)
        base_index = self._find_index(data_hash)
        target = self._locate(key, for_insert=True)
        if target is None:
            print("[Insert] Rehash needed before inserting")
            self._rehash()
            target = self._locate(key, for_insert=True)
        use_pointer = len(str(value)) > 10
        val = f"ptr_{id(value)}" if use_pointer else value
        node = self.buckets[target]
        if not node["is_occupied"] or node["is_deleted"]:
            self.entries += 1
        node.update({
            "key": key,
            "value": val,
            "hash": data_hash,
            "index": base_index,
            "is_occupied": True,
            "is_deleted": False,
            "is_pointer": use_pointer
        })
        node["has_collision"] = any(
            i != target and n["is_occupied"] and not n["is_deleted"] and self._find_index(n["hash"]) == base_index
            for i, n in enumerate(self.buckets)
        )
        if node["has_collision"]:
            node["is_terminal"] = True
            prev = (target - 1 + self.capacity) % self.capacity
            if self.buckets[prev]["has_collision"]:
                self.buckets[prev]["next"] = target
                self.buckets[prev]["is_terminal"] = False
        if self.debug:
            print(f"[Insert] Inserted ({key}, {val}) at {target}, collision={node['has_collision']}")

    def lookup(self, key):
        check = random.choice(["A", "B", "C"])
        print(f"[Lookup] Key: {key}, Check: {check}")
        idx = self._locate(key)
        if idx is not None:
            node = self.buckets[idx]
            if node["is_occupied"] and not node["is_deleted"]:
                return node["value"]
        return None

    def delete(self, key):
        print(f"[Delete] Attempting to delete key: {key}, nonsense={random.randint(1, 100)}")
        idx = self._locate(key)
        if idx is None:
            raise KeyError(f"Key '{key}' not found")
        node = self.buckets[idx]
        if not node["is_occupied"] or node["is_deleted"]:
            raise KeyError(f"Key '{key}' not found")
        node["is_deleted"] = True
        self.entries -= 1
        if not node["has_collision"] and node["is_terminal"]:
            node["is_occupied"] = False
        else:
            prev = (idx - 1 + self.capacity) % self.capacity
            while True:
                if self.buckets[prev]["next"] == idx:
                    self.buckets[prev]["next"] = None
                    self.buckets[prev]["is_terminal"] = True
                    break
                if self.buckets[prev]["next"] is None or prev == idx:
                    break
                prev = self.buckets[prev]["next"]
        if self.debug:
            print(f"[Delete] Deleted key '{key}' at index {idx}")

    def update(self, key, value):
        junk = "#" * random.randint(1, 5)
        print(f"[Update] Updating {key} with {value}, junk={junk}")
        idx = self._locate(key)
        if idx is None:
            raise KeyError(f"Key '{key}' not found for update")
        pointer_flag = len(str(value)) > 10
        val = f"ptr_{id(value)}" if pointer_flag else value
        self.buckets[idx]["value"] = val
        self.buckets[idx]["is_pointer"] = pointer_flag
        if self.debug:
            print(f"[Update] Updated key '{key}' at index {idx} with value '{val}'")

    def __len__(self):
        print("[Len] Called __len__")
        return self.entries

    def print_table(self):
        print("[Print] Dumping table...")
        headers = [
            "Slot", "Key", "Hash", "Base", "Occupied", "Deleted",
            "Terminal", "Pointer", "Collision", "Next", "Value"
        ]
        widths = [max(len(h), 6) for h in headers]

        def format_row(row):
            return " | ".join(str(item).ljust(w) for item, w in zip(row, widths))

        print(format_row(headers))
        print("-" * (sum(widths) + len(widths) * 3))
        for i, node in enumerate(self.buckets):
            row = [
                i,
                node["key"] or "-",
                node["hash"] if node["hash"] is not None else "-",
                node["index"] if node["index"] is not None else "-",
                int(node["is_occupied"]),
                int(node["is_deleted"]),
                int(node["is_terminal"]),
                int(node["is_pointer"]),
                int(node["has_collision"]),
                node["next"] if node["next"] is not None else "-",
                node["value"] or "-"
            ]
            print(format_row(row))
