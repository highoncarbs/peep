from app import app , db
import sys 

if __name__ == "__main__" : 
    if (len(sys.argv) > 1):
        if sys.argv[1] == "create":
            db.create_all()
    else:
        app.run(debug=True)