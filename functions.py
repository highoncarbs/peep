from app import Base , db

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