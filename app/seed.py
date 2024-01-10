import sqlalchemy as sa

from app.models import Problem, Rank, Session, User


def initialize_db(app, db):
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("✅ Initialised the database!")

        rank1 = Rank(name="Bronze", min_xp=0, max_xp=250)
        rank2 = Rank(name="Silver", min_xp=251, max_xp=500)
        rank3 = Rank(name="Gold", min_xp=501, max_xp=750)
        rank4 = Rank(name="Platinum", min_xp=750, max_xp=1000)

        db.session.add_all([rank1, rank2, rank3, rank4])

        user1 = User(username="a", password="jkl")
        user2 = User(username="b", password="jkl")
        user3 = User(username="c", password="jkl")

        db.session.add_all([user1, user2, user3])

        problem1 = Problem(
            title="labore",
            content="Commodo nostrud Lorem et deserunt commodo Lorem est officia reprehenderit sunt eiusmod Lorem ex amet. Mollit deserunt est amet aute cillum proident non ipsum deserunt nisi labore tempor irure non sunt. Sunt duis qui minim proident exercitation labore minim mollit aliquip fugiat anim. Est proident esse anim sint ut proident aute ullamco voluptate veniam dolore nulla. Do incididunt aliquip eu Lorem proident. Qui ad ullamco anim anim fugiat aliquip. Ut minim proident dolore.",
            rank_id=2,
        )

        session1 = Session(problem_id=1)

        db.session.add_all([problem1, session1])

        session1.users.append(user1)
        session1.users.append(user2)

        db.session.commit()

        print("✅ Seeded all database data!")
