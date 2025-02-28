from lab_bank import create_app, db
from lab_bank.models import User

def promote_to_admin(username):
    # Create the Flask app
    app = create_app()

    # Push the app context
    with app.app_context():
        # Query the user
        user = User.query.filter_by(username=username).first()

        if user:
            # Promote the user to admin
            user.is_admin = True
            db.session.commit()
            print(f"{user.username} is now an admin.")
        else:
            print(f"User '{username}' not found.")

if __name__ == "__main__":
    import sys

    # Check if a username was provided
    if len(sys.argv) != 2:
        print("Usage: python add_admin.py <username>")
        sys.exit(1)

    # Get the username from the command line
    username = sys.argv[1]

    # Promote the user to admin
    promote_to_admin(username)
