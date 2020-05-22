######### ABout line 1838 of the /opt/omd/versions/XXXXXXXX/lib/python/cmk/gui/plugins/wato/datasource_programs.py file, you can find something like:

def _valuespec_special_agents_aws():
    return Dictionary(
        title=_('Amazon Web Services (AWS)'),
        elements=[
            ("access_key_id",
             TextAscii(
                 title=_("The access key ID for your AWS account"),
                 allow_empty=False,
                 size=50,
             )),
            ("secret_access_key",
             IndividualOrStoredPassword(
                 title=_("The secret access key for your AWS account"),
                 allow_empty=False,
             )),
            ("role_arn",
             IndividualOrStoredPassword(
                 title=_("The role ARN of the AWS account you want to query"),
                 allow_empty=True,
             )),
            ("global_services",
             Dictionary(
                 title=_("Global services to monitor"),
                 elements=[
                     ("ce",
                      FixedValue(None,
                                 totext=_("Monitor costs and usage"),
                                 title=_("Costs and usage (CE)"))),
                 ],
             )),

######## Notice that i added the following in IndividualOrStoredPassword mode because often the remote role must be hidden because of security but you can set as TextAscii if you feel conftable


            ("role_arn",
             IndividualOrStoredPassword(
                 title=_("The role ARN of the AWS account you want to query"),
                 allow_empty=True,
             )),
