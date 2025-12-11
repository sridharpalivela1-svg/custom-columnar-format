from src.columnar_writer import ColumnarWriter, TYPE_INT32, TYPE_STRING
from src.columnar_reader import ColumnarReader

writer = ColumnarWriter("output.ccf")
writer.add_column("id", TYPE_INT32, [1, 2, 3])
writer.add_column("value", TYPE_STRING, ["apple", "banana", "cherry"])
writer.write()

print("File written: output.ccf")

reader = ColumnarReader("output.ccf")
print(reader.read())
