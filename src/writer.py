import struct
import zlib

TYPE_INT32 = 1
TYPE_STRING = 2


class ColumnarWriter:
    def __init__(self, filename, schema, rowgroup_size=2, compression=True):
        self.filename = filename
        self.schema = schema
        self.rowgroup_size = rowgroup_size
        self.current_rows = []
        self.rowgroups = []
        self.compression = compression  # True = zlib, False = none

    def add_row(self, row):
        self.current_rows.append(row)
        if len(self.current_rows) >= self.rowgroup_size:
            self.finish_rowgroup()

    def finish_rowgroup(self):
        if self.current_rows:
            self.rowgroups.append(self.current_rows)
            self.current_rows = []

    def write(self):
        self.finish_rowgroup()

        with open(self.filename, "wb") as f:
            # Number of columns
            f.write(struct.pack("<I", len(self.schema)))

            # Schema metadata
            for name, col_type in self.schema:
                name_bytes = name.encode("utf-8")
                f.write(struct.pack("<I", len(name_bytes)))
                f.write(name_bytes)
                f.write(struct.pack("<I", col_type))

            # Number of row groups
            f.write(struct.pack("<I", len(self.rowgroups)))

            # Write each row group
            for group in self.rowgroups:
                f.write(struct.pack("<I", len(group)))  # rows in group

                # --- Build raw uncompressed block ---
                block = bytearray()

                for col_index, (_, col_type) in enumerate(self.schema):
                    values = [row[col_index] for row in group]

                    if col_type == TYPE_INT32:
                        for v in values:
                            block += struct.pack("<i", v)

                    elif col_type == TYPE_STRING:
                        for v in values:
                            b = v.encode("utf-8")
                            block += struct.pack("<I", len(b))
                            block += b

                # --- Compress if enabled ---
                if self.compression:
                    compressed = zlib.compress(block)
                    f.write(struct.pack("<I", 1))  # compression flag
                    f.write(struct.pack("<I", len(compressed)))
                    f.write(compressed)
                else:
                    f.write(struct.pack("<I", 0))  # no compression
                    f.write(struct.pack("<I", len(block)))
                    f.write(block)
