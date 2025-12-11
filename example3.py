from src.writer import ColumnarWriter, TYPE_INT32, TYPE_STRING
from src.reader import ColumnarReader

writer = ColumnarWriter("compressed.cstm", [
    ("id", TYPE_INT32),
    ("name", TYPE_STRING)
], rowgroup_size=2, compression=True)

writer.add_row([1, "apple"])
writer.add_row([2, "banana"])
writer.add_row([3, "cherry"])
writer.add_row([4, "dragonfruit"])
writer.write()

reader = ColumnarReader("compressed.cstm")
print(reader.read())
