def create_session(access_key_id, secret_access_key, region, role):
    if role == "":
        return boto3.session.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name=region)
    else:
        session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        boto_assume_role = session.client('sts')
        assume_role_resp_policy = boto_assume_role.assume_role(RoleArn=role, RoleSessionName='newsession')
        newsession_id = assume_role_resp_policy["Credentials"]["AccessKeyId"]
        newsession_key = assume_role_resp_policy["Credentials"]["SecretAccessKey"]
        newsession_token = assume_role_resp_policy["Credentials"]["SessionToken"]
        sessEdu = boto3.session.Session(aws_access_key_id=newsession_id, aws_secret_access_key=newsession_key, region_name=region, aws_session_token=newsession_token)
        return sessEdu
    #return boto3.session.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name=region)




   parser.add_argument("--role-arn",
                        required=False,
                        help="The role ARN of the AWS remote account.")
