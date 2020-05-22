###### In the file /opt/omd/versions/XXXXXX/share/check_mk/checks/agent_aws you have to edit the function agent_aws_arguments, adding the param "role_arn" like following


def agent_aws_arguments(params, hostname, ipaddress):
    args = [
        "--access-key-id",
        params["access_key_id"],
        "--role-arn",
        params["role_arn"],
        "--secret-access-key",
        passwordstore_get_cmdline("%s", params["secret_access_key"]),
    ]
    regions = params.get("regions")