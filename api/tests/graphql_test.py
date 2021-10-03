import json

from graphene_django.utils.testing import GraphQLTestCase

from api.models import User, TransactionKind


class GraphqlTestCase(GraphQLTestCase):
    GRAPHQL_URL = '/api/graphql'
    token = ''

    @classmethod
    def setUpTestData(cls):
        u = User()
        u.username = 'myadmin'
        u.set_password(raw_password='admin123')
        u.save()

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
        token = content['data']['login']['token']
        self.assertIsNotNone(self.token)
        self.assertResponseNoErrors(response)

        # response = self.query(
        #     '''
        #     {
        #       me {
        #         id
        #         username
        #       }
        #     }
        #     ''',
        #     headers=
        #     {
        #         "authorization": "jwt " + token
        #     }
        # )
        #
        # content = json.loads(response.content)
        # print(content)

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
