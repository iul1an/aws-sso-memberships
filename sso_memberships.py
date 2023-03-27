# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import json
import boto3

class SSOMemberships:

    def __init__(self, aws_client, identity_store_id):
        self.aws_client = aws_client
        self.identity_store_id = identity_store_id

    def get_users(self):
        paginator = self.aws_client.get_paginator('list_users')
        users = {}
        for page in paginator.paginate(IdentityStoreId = self.identity_store_id):
            u_page = page['Users']
            for user in u_page:
                user_id = user['UserId']
                user_name = user['UserName']
                users[user_id] = user_name
        return users

    def get_groups(self):
        paginator = self.aws_client.get_paginator('list_groups')
        groups = {}
        for page in paginator.paginate(IdentityStoreId = self.identity_store_id):
            g_page = page['Groups']
            for group in g_page:
                group_id = group['GroupId']
                group_name = group['DisplayName']
                groups[group_id] = group_name
        return groups

    def get_memberships(self):
        users = self.get_users()
        groups = self.get_groups()
        paginator = self.aws_client.get_paginator('list_group_memberships')
        memberships = {}
        for group_id, group_name in groups.items():
            for page in paginator.paginate(IdentityStoreId = self.identity_store_id,
                                           GroupId = group_id):
                m_users = []
                m_page = page['GroupMemberships']
                for membership in m_page:
                    m_user_id = membership['MemberId']['UserId']
                    m_user_name = users[m_user_id]
                    m_users.append(m_user_name)
                if len(m_users) > 0:
                    memberships[group_name] = sorted(m_users)
        return dict(sorted(memberships.items()))

def main():
    aws_client = boto3.client('sso-admin')
    sso_instances = aws_client.list_instances()
    aws_client = boto3.client('identitystore')
    for sso_instance in sso_instances['Instances']:
        identity_store_id = sso_instance['IdentityStoreId']
        obj = SSOMemberships(aws_client, identity_store_id)
        memberships = obj.get_memberships()
        print(json.dumps(memberships, indent = 4))

if __name__ == "__main__":
    main()
