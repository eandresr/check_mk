This mod tries to complete the functionality of the AWS connector for Check_MK as the current Well Arquitected Framework says that 
landing zones are the way of isolate resources ant the way to reduce the shock wave in case of attack. Landing Zones often require
the Login account and then, users must "jump" from that account to another account roles (Switch Role). Ok, the problem is that
 from 1.6.0 versions, Check_MK has the AWS conenctor ready to work, first against HTTP Rest API and after that, with the boto3 botocore
 python module. The problem here is that the module only accept acces_key_id and secret_access_key, that means that you have to create
one IAM user in every account you want to monitor (remember Landing Zone, this is not the way!).
 
The problem could be solved with this mod, using the "sts" service.

You can modify your files or you can just replace with mine... My advise is to replace (with previous backup)

FIles:
	- /opt/omd/versions/XXXXXXXX/lib/python/cmk/special_agents/agent_aws.py
	- /opt/omd/versions/XXXXXXXX/lib/python/cmk/gui/plugins/wato/datasource_programs.py
	- /opt/omd/versions/XXXXXXXX/share/check_mk/checks/agent_aws

After makins all the changes, you must restart your omd

	omd restart