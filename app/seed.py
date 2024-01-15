import sqlalchemy as sa

from app.models import Example, Problem, Rank, Session, User


def initialize_db(app, db):
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("✅ Initialised the database!")

        rank1 = Rank(name="Bronze", min_xp=0, max_xp=250)
        rank2 = Rank(name="Silver", min_xp=251, max_xp=500)
        rank3 = Rank(name="Gold", min_xp=501, max_xp=750)
        rank4 = Rank(name="Platinum", min_xp=751, max_xp=1000)

        db.session.add_all([rank1, rank2, rank3, rank4])

        user1 = User(username="a", password="jkl")
        user2 = User(username="b", password="jkl")
        user3 = User(username="c", password="jkl")

        db.session.add_all([user1, user2, user3])

        problem1 = Problem(
            title="labore",
            description="Commodo nostrud Lorem et deserunt commodo Lorem est officia reprehenderit sunt eiusmod Lorem ex amet. Mollit deserunt est amet aute cillum proident non ipsum deserunt nisi labore tempor irure non sunt. Sunt duis qui minim proident exercitation labore minim mollit aliquip fugiat anim. Est proident esse anim sint ut proident aute ullamco voluptate veniam dolore nulla. Do incididunt aliquip eu Lorem proident. Qui ad ullamco anim anim fugiat aliquip. Ut minim proident dolore.",
            rank_id=2,
        )

        problem2 = Problem(
            title="sit",
            description="Elit magna ad anim sunt consectetur commodo laborum non id consectetur aliquip voluptate pariatur velit ea. Officia sunt magna esse incididunt. Ex cupidatat in commodo amet voluptate Lorem do veniam excepteur ut aliqua ullamco ad. Aliquip nostrud consequat ad duis quis est cupidatat cupidatat cupidatat cillum. Incididunt ut aliquip ut eiusmod officia ullamco consequat in ea. Ad consequat occaecat est duis incididunt.",
            rank_id=1,
        )

        problem3 = Problem(
            title="voluptate",
            description="Aliqua do laborum occaecat cillum. Dolore pariatur veniam minim. Laboris quis cillum id elit. Ex irure ipsum sit tempor sint ea enim laboris cupidatat mollit occaecat dolore do culpa nulla. Est deserunt laboris ullamco cillum enim mollit consectetur. Incididunt exercitation quis officia tempor ea nulla ipsum exercitation exercitation. Occaecat labore sint quis ullamco adipisicing deserunt esse adipisicing non duis Lorem ea.",
            rank_id=3,
        )

        problem4 = Problem(
            title="reprehenderit",
            description="Elit deserunt tempor cillum eu. Laborum aute tempor sunt incididunt anim reprehenderit elit ut nisi cillum sint aliquip dolor. Adipisicing est incididunt aute. Occaecat excepteur eiusmod sit ullamco voluptate dolore reprehenderit qui id quis. Ipsum eiusmod sint do voluptate et incididunt voluptate aute qui occaecat ullamco consectetur cupidatat. Pariatur commodo sunt id. Cillum elit proident esse. Sint adipisicing ut pariatur excepteur anim non veniam nostrud elit.",
            rank_id=4,
        )

        example1 = Example(
            problem_id=1,
            input="cillum",
            output="adipisicing occaecat",
            explanation="Commodo exercitation in nulla aliqua reprehenderit magna reprehenderit adipisicing. Do pariatur consequat eu ad ut eu tempor elit. Eiusmod esse Lorem aliquip pariatur ea. Fugiat consectetur do est et magna labore sunt tempor quis.",
        )

        example2 = Example(
            problem_id=2,
            input="non",
            output="Lorem occaecat",
            explanation="Dolor enim nostrud pariatur do eu exercitation deserunt. Enim ad amet nisi adipisicing officia mollit ullamco. Velit proident deserunt voluptate magna reprehenderit aliqua occaecat labore ex sit fugiat. Et qui ex laborum esse nostrud minim voluptate. Minim ut Lorem est labore sunt tempor aliquip amet. Qui veniam magna commodo nostrud elit eu fugiat do cupidatat nulla laboris pariatur nostrud sunt. Qui ex sit quis sint duis commodo. Ea aliquip ex eiusmod commodo excepteur officia incididunt ut minim elit.",
        )

        example3 = Example(
            problem_id=3,
            input="cillum",
            output="adipisicing aliquip",
            explanation="Proident pariatur laborum sint nulla nulla non est in adipisicing. Cillum magna nostrud et nostrud laboris. Ea eu elit cillum. Pariatur fugiat esse cupidatat ad esse commodo anim sit.",
        )

        example4 = Example(
            problem_id=4,
            input="cillum",
            output="sint elit",
            explanation="Culpa proident enim culpa labore irure exercitation veniam. Ad aliqua proident laborum. Qui est culpa tempor ut qui excepteur proident irure non incididunt in. Labore commodo cupidatat ex ipsum in. Lorem ipsum culpa esse fugiat ullamco nostrud do. Cupidatat pariatur mollit minim id nisi amet ullamco anim laboris commodo eu. Cupidatat elit cillum labore deserunt non ullamco.",
        )

        session1 = Session(problem_id=1, winner_id=3)

        db.session.add_all(
            [
                problem1,
                problem2,
                problem3,
                problem4,
                example1,
                example2,
                example3,
                example4,
                session1,
            ]
        )

        session1.users.append(user1)
        session1.users.append(user2)

        db.session.commit()

        print("✅ Seeded all database data!")
