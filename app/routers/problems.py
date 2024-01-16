import os, json
from http import HTTPStatus
from flask_restx import Namespace, Resource
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import func
from openai import OpenAI

from app.extensions import db
from app.models import Problem, Example
from app.api_models import problem_model


authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
problemRouter = Namespace(
    "problems", description="`/problems` routes", authorizations=authorizations
)


@problemRouter.route("/random")
class RandomProblem(Resource):
    method_decorators = [jwt_required()]

    @problemRouter.doc(security="jsonWebToken")
    @problemRouter.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired")
    @problemRouter.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error"
    )
    @problemRouter.marshal_with(problem_model)
    def get(self):
        """Get a random problem with the same rank as the currently logged-in user"""
        problem = (
            Problem.query.filter_by(rank_id=current_user.rank_id)
            .order_by(func.random())
            .first()
        )
        return problem, HTTPStatus.OK


@problemRouter.route("/generate")
class GenerateProblem(Resource):
    method_decorators = [jwt_required()]

    @problemRouter.doc(security="jsonWebToken")
    @problemRouter.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired")
    @problemRouter.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error"
    )
    @problemRouter.marshal_with(problem_model)
    def post(self):
        """Generate a problem with the same rank as the currently logged-in user using AI"""

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        rank_name = current_user.rank.name

        problems = Problem.query.all()

        output_format = {
            "problem": {
                "title": "Fill in question title",
                "description": "Fill in question description",
                "examples": [
                    {
                        "input": "Fill in input values",
                        "output": "Fill in output values",
                        "explanation": "Provide explanation as to how the inputs were used to reach the desired output",
                        "test_case": "Provide a test case in the form of a function call using the input e.g. function_name(input)",
                    }
                ],
            }
        }

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {
                    "role": "assistant",
                    "content": f"""You are coding challenge generator for programmers, where your task is to generate a coding challenge in a similar vein to CodeWars based on the provided rank of the user, where the resultant difficulty to be used will be shown below:

                    - Bronze rank = ~8-7 kyu Codewars challenge
                    - Silver rank = ~6-5 kyu Codewars challenge
                    - Gold rank = ~4-3 kyu Codewars challenge
                    - Platinum rank = ~2-1 kyu Codewars challenge

                    Try to be creative with the challenges you create, where you should shy away from creating generic challenges. You should also try not to generate already existing challenges, with the list of recorded challenges provided below:

                    {problems}
                    
                    You should create a valid JSON object containing the the title of the coding challenge, a description and examples with expected inputs, outputs and a test case where you define a function call, using the inputs:

                    {output_format}

                    You should only return the JSON object with no backticks or special formatting.

                    The provided rank of the user is: {rank_name}""",
                }
            ],
        )

        resp = json.loads(completion.choices[0].message.content)
        resp_problem = resp["problem"]

        problem = Problem(
            title=resp_problem["title"],
            description=resp_problem["description"],
            rank_id=current_user.rank.id,
        )

        db.session.add(problem)
        db.session.commit()

        examples = [
            Example(
                problem_id=problem.id,
                input=e["input"],
                output=e["output"],
                explanation=e["explanation"],
                test_case=e["test_case"],
            )
            for e in resp_problem["examples"]
        ]

        db.session.add_all(examples)
        db.session.commit()

        return problem, HTTPStatus.CREATED
