# import os
# import responses


# @responses.activate
# def test_get(client):
#     responses.add(
#         responses.GET,
#         f'http://localhost:{os.environ["FLASK_RUN_PORT"]}/problems',
#         json={
#             "id": 4,
#             "title": "reprehenderit",
#             "content": "Elit deserunt tempor cillum eu. Laborum aute tempor sunt incididunt anim reprehenderit elit ut nisi cillum sint aliquip dolor. Adipisicing est incididunt aute. Occaecat excepteur eiusmod sit ullamco voluptate dolore reprehenderit qui id quis. Ipsum eiusmod sint do voluptate et incididunt voluptate aute qui occaecat ullamco consectetur cupidatat. Pariatur commodo sunt id. Cillum elit proident esse. Sint adipisicing ut pariatur excepteur anim non veniam nostrud elit.",
#             "rank": [{"id": 4, "name": "Platinum", "min_xp": 750, "max_xp": 1000}],
#         },
#         status=200,
#     )
#     # register_response = client.post(
#     #     "/users/register", data={"username": "d", "password": "jkl"}
#     # )
#     # print(register_response)
#     # assert register_response == 201
#     response = client.get("/problems")
#     assert response.status_code == 200
