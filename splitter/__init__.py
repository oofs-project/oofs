import encdec

def chunk(filename, chunksize):
    file_number = 1
    with open(filename, "rb") as f:
        chunk = f.read(chunksize)
        while chunk:
            with open("chunks/" + filename[:-4] + str(file_number), "ab") as chunk_file:
                # encodedfile = encdec.encodeBits(chunk)
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(chunksize)
        return True

