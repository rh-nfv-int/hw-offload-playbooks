# hwoffloadplaybooks

Have ansible playbooks to automate and validate different ovs-hw-offload scenarios/use cases
As a first step we are testing the Stateful NAT usecase (for TCP and UDP).

# What to do before running the test ? 

*Note: These steps needs to be done only first time for a setup to make it ready*

Few steps are needed to be done as below before we can trigger the run

1. Fill the inventory file. (inventory file is provided. Please edit it and same file can be passed in command line while executing the test)

2. Since the playbook tries to access or log in to the compute1 and compute2 which we filled in the inventory file above,
   We need to copy the ssh public keys using the commands below and login and see that it doesnt expect password to be entered each time.

   ssh-copy-id -i ~/.ssh/id_rsa.pub root@dest_machine

   When you execute the command it asks for the password. After the copy from next time if you try ssh to root@dest_machine it shouldnt ask for password and login directly from thereon

3. The playbook doesn't install OVN and OVS.
   User shall use or test with the version he wants to. 
   So the user has to install OVN and OVS on compute1(DUT) and provide the path of the same in the config file as explained in next step.

4. Please configure required details in the files "ovn_ovs_vars" and "rhel_vars"
   which sets the variables to appropriate values which will be used in the test run.

5. Execute the test by using the command like below
   ansible-playbook -v -i inventory testNAToffload.yml

6. Logs to look for. It generates 2 log files which are timestamped and it will remain on your compute1 where we have taken the dump of flows and Conn Track table.
   Files are named dump_flows_<timestamp>.txt and dump_ct_table_<timestamp>.txt

7. We have taken care to see that the test cleans up all things which it created (expect the above logs). In case the test bails out inbetween and resources are not cleared out.
   Please run the cleanup script in the utilities folder.
   ansible-playbook -v -i inventory utilities/cleanupNATconfigs.yml

Known Issues and Workarounds:

Sometimes --> "subscription-manager register --force" throws up an error and it does not create the VM itself --> Such cases just re-run the playbook and usually the next run it works all good. Investigation in progress for this . But this shouldn't be a blocker. 
