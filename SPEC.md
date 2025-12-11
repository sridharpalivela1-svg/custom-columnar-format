# Custom Columnar Storage Format – SPEC

## 1. File Structure

The file consists of:
1. Number of columns (uint32)
2. Schema:
   - Column name length (uint32)
   - Column name (utf-8 bytes)
   - Column type (uint32)
3. Number of row groups (uint32)
4. For each row group:
   - Row count (uint32)
   - Compression flag (uint32) (0 = none)
   - Block size (uint32)
   - Block data (raw or compressed)

## 2. Supported Types
- TYPE_INT32 = 1 → 4-byte integers
- TYPE_STRING = 2 → UTF-8 strings prefixed with length (uint32)

## 3. Writer Logic
- Write schema
- Encode rows column-wise
- Combine into one block
- Optionally compress
- Write block to file

## 4. Reader Logic
- Read schema
- Read row group metadata
- Decompress if needed
- Parse block and reconstruct columns

## 5. Example
Input:
id = [1,2,3]
value = ["apple","banana","cherry"]

Output structure reconstructed by reader.
