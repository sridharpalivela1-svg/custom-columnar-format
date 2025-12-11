import struct
import zlib

TYPE_INT32 = 1
TYPE_STRING = 2


class ColumnarReader:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, "rb") as f:

            num_cols = struct.unpack("<I", f.read(4))[0]

            schema = []
            for _ in range(num_cols):
                name_len = struct.unpack("<I", f.read(4))[0]
                name = f.read(name_len).decode("utf-8")
                col_type = struct.unpack("<I", f.read(4))[0]
                schema.append((name, col_type))

            num_groups = struct.unpack("<I", f.read(4))[0]

            result = {name: [] for name, _ in schema}

            for _ in range(num_groups):
                rows = struct.unpack("<I", f.read(4))[0]
                compression_flag = struct.unpack("<I", f.read(4))[0]
                block_size = struct.unpack("<I", f.read(4))[0]
                block = f.read(block_size)

                if compression_flag == 1:
                    block = zlib.decompress(block)

                offset = 0
                for name, col_type in schema:
                    if col_type == TYPE_INT32:
                        for _ in range(rows):
                            v = struct.unpack("<i", block[offset:offset+4])[0]
                            result[name].append(v)
                            offset += 4

                    else:
                        for _ in range(rows):
                            strlen = struct.unpack("<I", block[offset:offset+4])[0]
                            offset += 4
                            s = block[offset:offset+strlen].decode("utf-8")
                            offset += strlen
                            result[name].append(s)

        return result
