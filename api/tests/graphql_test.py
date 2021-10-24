import json

from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token

from api.models import User, TransactionKind


class GraphqlTestCase(GraphQLTestCase):
    fixtures = ['dump-1400-08-01.json', ]
    GRAPHQL_URL = '/api/graphql'

    @classmethod
    def setUpTestData(cls):
        u: User = User(username='superadmin')
        # u.username = 'myadmin'
        # u.set_password(raw_password='admin123')
        # u.is_superuser=True
        # u.save()
        cls.token = get_token(u)
        tk = TransactionKind.objects.create(title="sarmaye")
        tk.save()

    def test_login(self):
        response = self.query(
            '''
                mutation {
                  login(username: "superadmin", password: "Admin123") {
                    token
                    user{
                      id
                      username
                    }
                  }
                }

            '''
            # '''
            #     mutation login($username: String!, $password: String!) {
            #       login(username: $username, password: $password) {
            #         token
            #         user{
            #           id
            #           username
            #         }
            #       }
            #     }
            #
            # ''',
            # input_data={'username': 'admin', 'password': 'admin123'}
        )
        content = json.loads(response.content)
        self.token = content['data']['login']['token']
        self.assertIsNotNone(self.token)
        self.assertResponseNoErrors(response)

    def test_me(self):
        response = self.query(
            '''
            {
              me {
                id
                username
              }
            }
            ''',
            headers=
            {
                "HTTP_AUTHORIZATION": "jwt " + self.token
                # "http_authorization": "jwt " + token
                # "AUTHORIZATION": "jwt " + token
            }
        )

        content = json.loads(response.content)
        id = content['data']['me']['id']
        username = content['data']['me']['username']
        print(content)
        # self.assertEqual(id, '1')
        self.assertEqual(username, 'superadmin')

    def test_transactionKinds(self):
        response = self.query(
            '''
            {
              transactionKinds {
                id
                title
              }
            }
            '''
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_create_profile_mutation_with_presenterId(self):
        response = self.query(
            '''
            mutation {
              createProfile(input: {firstName: "testuser_first", lastName: "testuser_last", codeMeli: "1754432573",presenterId:2, user: {username: "testusre_username2", password: "testuser_password"}}) {
                profile{
                  id
                  firstName
                  lastName
                  codeMeli
                  moaref
                }
              }
            }
        ''',
            headers=
            {
                "HTTP_AUTHORIZATION": "jwt " + self.token
            }
        )
        content = json.loads(response.content)
        print(content)
        firstName = content['data']['createProfile']['profile']['firstName']
        self.assertEqual(firstName, 'testuser_first')

    def test_create_profile_mutation_no_presenterId(self):
        response = self.query(
            '''
            mutation {
              createProfile(input: {firstName: "testuser_first", lastName: "testuser_last", codeMeli: "1754432573", user: {username: "testusre_username2", password: "testuser_password"}}) {
                profile{
                  id
                  firstName
                  lastName
                  codeMeli
                  moaref
                }
              }
            }
        ''',
            headers=
            {
                "HTTP_AUTHORIZATION": "jwt " + self.token
            }
        )
        content = json.loads(response.content)
        print(content)
        firstName = content['data']['createProfile']['profile']['firstName']
        self.assertEqual(firstName, 'testuser_first')
