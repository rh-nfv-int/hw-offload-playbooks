# Performance Test Playbooks

This is a collection of Ansible playbooks to test OpenvSwitch performance.

All the playbooks use combinations of Ansible roles that can be found in the
`roles` directory. These roles use one or more of the `install`, `setup` and
`test` ansible tags. By default, every task is executed. To only perform the
test part you can use the `--tags test` option. To explicitly skip the install
and/or setup phases, you can use the `--skip-tags install` and/or `--skip-tags
install,setup` arguments.

## Configuration

These playbooks have been made for a specific platform. In order to run them on
different platforms, the `host.yml` inventory file must be edited. Follow the
comments for guidance.

## Examples

### OVS conntrack with DPDK dataplane

```
ansible-playbook -e datapath=dpdk ovs-conntrack.yml
```

### OVS conntrack with hardware offload dataplane

```
ansible-playbook -e datapath=hwol ovs-conntrack.yml
```
