import encdec
import io

def chunk(filename, chunksize):
    chunks = []
    file_number = 1
    with open(filename, "rb") as f:
        chunk = f.read(chunksize)
        while chunk:
            with open("chunks/" + filename[:-4] + str(file_number), "wb") as chunk_file:
                # encodedfile = encdec.encodeBits(chunk)
                chunk_file.write(chunk)
                chunks.append(io.BytesIO(chunk))
            file_number += 1
            chunk = f.read(chunksize)
        return chunks

def unchunk(chunks):
    pass
