from app import create_app
from app.models.user import User

app = create_app()

with app.app_context():

    users = User.query.all()

    print("Number of users:", len(users))

    if not users:
        print("No users found in database.")
    else:
        for user in users:
            print(
                user.id,
                user.name,
                user.email
            )
