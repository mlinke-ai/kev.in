#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Kev.in - a coding learning platform
# Copyright (C) 2022  Max Linke
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import flask_unittest
from flask_jwt_extended import decode_token, get_jti
from flask_unittest import ClientTestCase
from flask_unittest.case import FlaskClient

from backend import create_app


class BaseTest(ClientTestCase):
    app = create_app()

    def setUp(self, client: FlaskClient) -> None:
        raise NotImplementedError

    def tearDown(self, client: FlaskClient) -> None:
        raise NotImplementedError


class UserTest(BaseTest):
    user_id = None
    user_name = "Willie Baldomero"
    user_mail = "willie.baldomero@example.com"
    user_pass = "eiZach2shoh4yo6kieBieFei"
    user_role = None

    def setUp(self, client: FlaskClient) -> None:
        # create user (it is already logged in)
        # TODO: check if user exists and simply log him in
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))
        r = client.post(
            "/user",
            json={
                "user_name": UserTest.user_name,
                "user_mail": UserTest.user_mail,
                "user_pass": UserTest.user_pass,
            },
            headers={"Content-Type": "application/json"},
        )
        self.assertTrue(r.is_json)
        self.assertEqual(r.status_code, 200)
        UserTest.user_id = r.json.get("user_id", None)
        self.assertTrue(UserTest.user_id is not None)
        self.assertTrue(isinstance(UserTest.user_id, int))
        UserTest.user_role = r.json.get("user_role_value", None)
        self.assertTrue(UserTest.user_role is not None)
        self.assertTrue(isinstance(UserTest.user_role, int))

    def tearDown(self, client: FlaskClient) -> None:
        # logout and delete user
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))
        token = None
        for cookie in client.cookie_jar:
            token = cookie.value if cookie.name == "csrf_access_token" else None
        r = client.delete("/user", json={"user_id": UserTest.user_id}, headers={"X-CSRF-TOKEN": token})
        self.assertTrue(r.is_json)
        self.assertEqual(r.status_code, 200)

    # --- GET ---

    def test_get_existing_by_id(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_id={UserTest.user_id}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(UserTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_name(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_name={UserTest.user_name}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(UserTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_mail(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_mail={UserTest.user_mail}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(UserTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_existing_by_role(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_role={UserTest.user_role}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertIn(UserTest.user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_non_existing_by_id(self, client: FlaskClient) -> None:
        user_id = -1
        r = client.get(f"/user?user_id={user_id}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertNotIn(user_id, [d["user_id"] for d in r.json["data"]])

    def test_get_non_existing_by_name(self, client: FlaskClient) -> None:
        user_name = "Does Not Exist"
        r = client.get(f"/user?user_name={user_name}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertNotIn(user_name, [d["user_name"] for d in r.json["data"]])

    def test_get_non_existing_by_mail(self, client: FlaskClient) -> None:
        user_mail = "does.not.exist@example.com"
        r = client.get(f"/user?user_mail={user_mail}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json)
        self.assertNotIn(user_mail, [d["user_mail"] for d in r.json["data"]])

    def test_get_non_existing_by_role(self, client: FlaskClient) -> None:
        user_role = -1
        r = client.get(f"/user?user_role={user_role}")
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], {"user_role": f"{user_role} is not a valid UserRole"})

    def test_get_restrict_page_size(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        user_limit = 1
        r = client.get(f"/user?user_role={UserTest.user_role}&user_limit={user_limit}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(user_limit, r.json["meta"]["page_size"])

    def test_get_page_index_zero(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        user_page = 0
        r = client.get(f"/user?user_id={UserTest.user_id}&user_page={user_page}")
        self.assertEqual(r.status_code, 404)
        self.assertTrue(r.is_json)
        self.assertEqual(
            r.json["message"],
            "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
        )

    def test_get_user_pass(self, client: FlaskClient) -> None:
        self.assertTrue(UserTest.user_id is not None)
        r = client.get(f"/user?user_id={UserTest.user_id}")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertNotIn("user_pass", r.json["data"][0].keys())

    # --- POST ---

    def test_post_user(self, client: FlaskClient) -> None:
        pass

    def test_post_user_without_token(self, client: FlaskClient) -> None:
        pass

    def test_post_duplicate_user(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_empty_name(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_empty_mail(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_empty_password(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_long_name(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_strange_name(self, client: FlaskClient) -> None:
        pass

    # --- PUT ---

    def test_put_mail_to_existing(self, client: FlaskClient) -> None:
        pass

    def test_put_name_to_empty(self, client: FlaskClient) -> None:
        pass

    def test_put_mail_to_empty(self, client: FlaskClient) -> None:
        pass

    def test_put_password_to_empty(self, client: FlaskClient) -> None:
        pass

    def test_put_admin_elevation_as_user(self, client: FlaskClient) -> None:
        pass

    def test_put_sadmin_elevation_as_user(self, client: FlaskClient) -> None:
        pass

    def test_put_demotion_as_user(self, client: FlaskClient) -> None:
        pass

    # --- DELETE ---

    def test_delete_existing(self, client: FlaskClient) -> None:
        pass

    def test_delete_non_existing(self, client: FlaskClient) -> None:
        pass

    def test_delete_self_as_user(self, client: FlaskClient) -> None:
        pass

    def test_delete_other_as_user(self, client: FlaskClient) -> None:
        pass


class AdminTest(BaseTest):
    def setUp(self, client: FlaskClient) -> None:
        # create user (it is already logged in) and promote it to admin
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))

    def tearDown(self, client: FlaskClient) -> None:
        # logout and delete admin
        self.assertTrue(client is not None)
        self.assertTrue(isinstance(client, FlaskClient))

    # --- GET ---

    def test_get_existing_by_id(self, client: FlaskClient) -> None:
        r = client.get("/user", json={"user_id": 1})
        self.assertEqual(r.status_code, 200)

    def test_get_existing_by_name(self, client: FlaskClient) -> None:
        pass

    def test_get_existing_by_mail(self, client: FlaskClient) -> None:
        pass

    def test_get_existing_by_role(self, client: FlaskClient) -> None:
        pass

    def test_get_non_existing_by_id(self, client: FlaskClient) -> None:
        pass

    def test_get_non_existing_by_name(self, client: FlaskClient) -> None:
        pass

    def test_get_non_existing_by_mail(self, client: FlaskClient) -> None:
        pass

    def test_get_non_existing_by_role(self, client: FlaskClient) -> None:
        pass

    def test_get_restrict_page_size(self, client: FlaskClient) -> None:
        pass

    # --- POST ---

    def test_post_admin(self, client: FlaskClient) -> None:
        pass

    def test_put_demotion_as_admin(self, client: FlaskClient) -> None:
        pass

    # --- PUT ---

    def test_put_admin_elevation_as_admin(self, client: FlaskClient) -> None:
        pass

    def test_put_sadmin_elevation_as_admin(self, client: FlaskClient) -> None:
        pass

    # --- DELETE ---

    def test_delete_self_as_admin(self, client: FlaskClient) -> None:
        pass

    def test_delete_other_as_admin(self, client: FlaskClient) -> None:
        pass


if __name__ == "__main__":
    flask_unittest.main()
