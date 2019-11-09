def chunk(filename, chunksize):
    file_number = 1
    with open(filename, "rb") as f:
        chunk = f.read(chunksize)
        while chunk:
            with open("chunks/" + filename + str(file_number)) as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(chunksize)


chunk()
