from app import Base , db
from math import log10, floor

def GroupTableCreator(tablename):
    '''
        Group Table creator
    '''
    class GroupTable(Base):
        __tablename__ = tablename
        id = db.Column(db.Integer , primary_key = True)
        contact = db.Column(db.Integer)

        def __init__(self, contact=None):
            contact = db.Column(db.Integer)
            
    return GroupTable

def human_format(num, ends=["", "K", "M", "B", "T"]):
        # divides by 3 to separate into thousands (...000)
        if num is 0:
            return str('0')
        return str(num)[0:2] + str(ends[int(floor(log10(num))/3)])