from src.writer import ColumnarWriter, TYPE_INT32, TYPE_STRING
from src.reader import ColumnarReader

writer = ColumnarWriter("rg_test.cstm", [
    ("id", TYPE_INT32),
    ("fruit", TYPE_STRING)
], rowgroup_size=2)

writer.add_row([1, "apple"])
writer.add_row([2, "banana"])
writer.add_row([3, "cherry"])
writer.add_row([4, "dates"])

writer.write()

reader = ColumnarReader("rg_test.cstm")
print(reader.read())
