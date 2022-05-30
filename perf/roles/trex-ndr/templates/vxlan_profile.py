from trex_stl_lib.api import *


class Profile:
    def get_streams(self, direction=0, tunables=(), **kwargs):
        inner_left_mac = "{{trex_config[0].port_info[0].src_mac}}"
        inner_left_ip = "16.0.0.1"
        inner_left_port = 32000
        inner_right_mac = "de:ed:de:ed:00:01"
        inner_right_ip = "48.0.0.1"
        inner_right_port = 42000
        outer_left_mac = "{{outer_left_mac}}"
        outer_left_ip = "172.16.0.1"
        outer_right_mac = "{{trex_config[0].port_info[1].src_mac}}"
        outer_right_ip = "172.16.0.2"

        if direction == 0:
            # outer
            pkt = Ether(src=inner_left_mac, dst=inner_right_mac)
            pkt /= IP(src=inner_left_ip, dst=inner_right_ip)
            pkt /= UDP(sport=inner_left_port, dport=inner_right_port)
            pkt /= b"x" * 20

        else:
            # outer
            pkt = Ether(src=outer_right_mac, dst=outer_left_mac)
            pkt /= IP(src=outer_right_ip, dst=outer_left_ip)
            pkt /= UDP(dport=4789)
            pkt /= VXLAN(vni=1337, flags=0x08)
            # inner
            pkt /= Ether(src=inner_right_mac, dst=inner_left_mac)
            pkt /= IP(src=inner_right_ip, dst=inner_left_ip)
            pkt /= UDP(sport=inner_right_port, dport=inner_left_port)
            pkt /= b"y" * 20

        return [STLStream(packet=STLPktBuilder(pkt), mode=STLTXCont())]


def register():
    return Profile()
