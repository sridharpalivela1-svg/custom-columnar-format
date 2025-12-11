import struct
import zlib

TYPE_INT32 = 1
TYPE_STRING = 2


class ColumnarWriter:
    def __init__(self, filename):
        self.filename = filename
        self.columns = {}

    def add_column(self, name, col_type, values):
        self.columns[name] = (col_type, values)

    def write(self):
        with open(self.filename, "wb") as f:

            # Write number of columns
            f.write(struct.pack("<I", len(self.columns)))

            # Write schema
            for name, (col_type, _) in self.columns.items():
                name_bytes = name.encode("utf-8")
                f.write(struct.pack("<I", len(name_bytes)))
                f.write(name_bytes)
                f.write(struct.pack("<I", col_type))

            # Only 1 row group
            f.write(struct.pack("<I", 1))

            # Number of rows
            rows = len(next(iter(self.columns.values()))[1])
            f.write(struct.pack("<I", rows))

            # Use compression flag = 0 (no compression)
            f.write(struct.pack("<I", 0))

            # Build block
            block = b""
            for name, (col_type, values) in self.columns.items():
                if col_type == TYPE_INT32:
                    for v in values:
                        block += struct.pack("<i", v)
                else:
                    for s in values:
                        b = s.encode("utf-8")
                        block += struct.pack("<I", len(b))
                        block += b

            # Write block size and block
            f.write(struct.pack("<I", len(block)))
            f.write(block)
