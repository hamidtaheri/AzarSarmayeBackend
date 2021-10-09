import json

from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token

from api.models import User, TransactionKind


class GraphqlTestCase(GraphQLTestCase):
    GRAPHQL_URL = '/api/graphql'

    @classmethod
    def setUpTestData(cls):
        u = User()
        u.username = 'myadmin'
        u.set_password(raw_password='admin123')
        u.save()
        cls.token = get_token(u)
        tk = TransactionKind.objects.create(title="sarmaye")
        tk.save()

    def test_login(self):
        response = self.query(
            '''
                mutation {
                  login(username: "myadmin", password: "admin123") {
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
        self.assertEqual(id, '1')
        self.assertEqual(username, 'myadmin')

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
