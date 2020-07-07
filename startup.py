from werkzeug.security import generate_password_hash, check_password_hash

from num_converter import db, create_app
from num_converter.models import User

#main script to init the database tables and create static user
#be sure to change the admin user password
def main():
    #creating database tables
    #passing app to get config
    app = create_app() #just to get config out of it
    with app.app_context():
        db.create_all()

        if User.query.all():
                print ('A user already exists. Default user will not be created')
        else:
            admin_user = User(username=app.config['DEFAULT_USER'], password=generate_password_hash(app.config['DEFAULT_PASSWORD']), typee=1)

            db.session.add(admin_user)
            db.session.commit()

if __name__ == '__main__':
    main()
