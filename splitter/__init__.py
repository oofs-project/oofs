import io

from diskcollections.iterables import FileList


def chunk(filename, chunksize):
    chunks = FileList()
    file_number = 1
    with open(filename, "rb") as f:
        chunk = f.read(chunksize)
        while chunk:
            chunks.append(io.BytesIO(chunk))
            file_number += 1
            chunk = f.read(chunksize)
    return chunks


def chunkBytes(bytes, chunksize):
    chunks = FileList()
    file_number = 1
    f = io.BytesIO(bytes)
    chunk = f.read(chunksize)
    while chunk:
        chunks.append(io.BytesIO(chunk))
        file_number += 1
        chunk = f.read(chunksize)
    return chunks
