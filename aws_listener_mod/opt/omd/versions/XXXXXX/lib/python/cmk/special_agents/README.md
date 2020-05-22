####### In the file /opt/omd/versions/XXXXXXXX/lib/python/cmk/special_agents/agent_aws.py you have to change the following funcions:

########create_session

def create_session(access_key_id, secret_access_key, region, role):
    if role == "None":
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



########Main

def main(sys_argv=None):
    if sys_argv is None:
        cmk.utils.password_store.replace_passwords()
        sys_argv = sys.argv[1:]
    args = parse_arguments(sys_argv)
    setup_logging(args.debug, args.verbose)
    hostname = args.hostname

    aws_config = AWSConfig(hostname, sys_argv, (args.overall_tag_key, args.overall_tag_values))
    for service_key, service_names, service_tags, service_limits in [
        ("ec2", args.ec2_names, (args.ec2_tag_key, args.ec2_tag_values), args.ec2_limits),
        ("ebs", args.ebs_names, (args.ebs_tag_key, args.ebs_tag_values), args.ebs_limits),
        ("s3", args.s3_names, (args.s3_tag_key, args.s3_tag_values), args.s3_limits),
        ("elb", args.elb_names, (args.elb_tag_key, args.elb_tag_values), args.elb_limits),
        ("elbv2", args.elbv2_names, (args.elbv2_tag_key, args.elbv2_tag_values), args.elbv2_limits),
        ("rds", args.rds_names, (args.rds_tag_key, args.rds_tag_values), args.rds_limits),
    ]:
        aws_config.add_single_service_config("%s_names" % service_key, service_names)
        aws_config.add_service_tags("%s_tags" % service_key, service_tags)
        aws_config.add_single_service_config("%s_limits" % service_key, service_limits)

    aws_config.add_single_service_config("s3_requests", args.s3_requests)
    aws_config.add_single_service_config("cloudwatch_alarms", args.cloudwatch_alarms)

    use_cache = aws_config.is_up_to_date() and not args.no_cache

    has_exceptions = False
    for aws_services, aws_regions, aws_sections in [
        (args.global_services, ["us-east-1"], AWSSectionsUSEast),
        (args.services, args.regions, AWSSectionsGeneric),
    ]:
        if not aws_services or not aws_regions:
            continue
        for region in aws_regions:
            try:
                if not args.role_arn:
                    session = create_session(args.access_key_id, args.secret_access_key, region, "None")
                else:
                    session = create_session(args.access_key_id, args.secret_access_key, region, args.role_arn)
                sections = aws_sections(hostname, session, debug=args.debug)
                sections.init_sections(aws_services, region, aws_config)
                sections.run(use_cache=use_cache)
            except AssertionError:
                if args.debug:
                    return 1
            except Exception as e:
                logging.info(e)
                has_exceptions = True
                if args.debug:
                    return 1
    if has_exceptions:
        return 1
    return 0


######### Here (in Main) the key is the following part, where we get the args and if no role is specifyed, we create sessión without:
            try:
                if not args.role_arn:
                    session = create_session(args.access_key_id, args.secret_access_key, region, "None")
                else:
                    session = create_session(args.access_key_id, args.secret_access_key, region, args.role_arn)

