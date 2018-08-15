from app import app , db
import sys 

if __name__ == "__main__" :
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        db.session.commit()
        db.reflect()
        db.drop_all()
    db.create_all()
    app.run(debug=True)