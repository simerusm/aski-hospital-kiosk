from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    all_users = User.query.all()
    print("\nAll users in the database:")
    for user in all_users:
        print(f"Name: {user.name}, Phone: {user.phone}")


    # Create the database and the database table
    db.create_all()

    # Add a new user
    new_user = User(name='John Doe', phone='1234567890')
    db.session.add(new_user)
    db.session.commit()

    # Query the user back
    user = User.query.filter_by(name='John Doe').first()

    existing_user = User.query.filter_by(name='John Doe').first()

    # Check if the user was added successfully
    if not existing_user:
        print(f"User added: {user.name}, Phone: {user.phone}")
    else:
        print("User not found.")