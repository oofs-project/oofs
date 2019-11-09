import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


__all__ = ("FileID", "session")

engine = create_engine('sqlite:///data.db')

Base = declarative_base()

Session = sessionmaker()

class FileID(Base):
    __tablename__ = "ids"

    id = Column(Integer(), primary_key=True)
    filename = Column(String())
    messageid = Column(String())

Base.metadata.create_all(engine)

Session.configure(bind=engine)

session = Session()


def getFileById(messageid):
    filename = session.query(FileID).filter_by(messageid=messageid).first()
    return 

def getIdByFile():
    pass

def addFileToDB(filepath, messageid):
    fileToAdd = FileID(filename=str(filepath), messageid=str(messageid))
    session.add(fileToAdd)
    try:
        session.commit()
    except:
        return False
    return True

def removeFileFromDBById(fileid):
    pass

def removeFileFromDBByFileName(filename):
    pass


