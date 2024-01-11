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

        problem2 = Problem(
            title="sit",
            content="Elit magna ad anim sunt consectetur commodo laborum non id consectetur aliquip voluptate pariatur velit ea. Officia sunt magna esse incididunt. Ex cupidatat in commodo amet voluptate Lorem do veniam excepteur ut aliqua ullamco ad. Aliquip nostrud consequat ad duis quis est cupidatat cupidatat cupidatat cillum. Incididunt ut aliquip ut eiusmod officia ullamco consequat in ea. Ad consequat occaecat est duis incididunt.",
            rank_id=1,
        )

        problem3 = Problem(
            title="voluptate",
            content="Aliqua do laborum occaecat cillum. Dolore pariatur veniam minim. Laboris quis cillum id elit. Ex irure ipsum sit tempor sint ea enim laboris cupidatat mollit occaecat dolore do culpa nulla. Est deserunt laboris ullamco cillum enim mollit consectetur. Incididunt exercitation quis officia tempor ea nulla ipsum exercitation exercitation. Occaecat labore sint quis ullamco adipisicing deserunt esse adipisicing non duis Lorem ea.",
            rank_id=3,
        )

        problem4 = Problem(
            title="reprehenderit",
            content="Elit deserunt tempor cillum eu. Laborum aute tempor sunt incididunt anim reprehenderit elit ut nisi cillum sint aliquip dolor. Adipisicing est incididunt aute. Occaecat excepteur eiusmod sit ullamco voluptate dolore reprehenderit qui id quis. Ipsum eiusmod sint do voluptate et incididunt voluptate aute qui occaecat ullamco consectetur cupidatat. Pariatur commodo sunt id. Cillum elit proident esse. Sint adipisicing ut pariatur excepteur anim non veniam nostrud elit.",
            rank_id=4,
        )

        session1 = Session(problem_id=1)

        db.session.add_all([problem1, problem2, problem3, problem4, session1])

        session1.users.append(user1)
        session1.users.append(user2)

        db.session.commit()

        print("✅ Seeded all database data!")
