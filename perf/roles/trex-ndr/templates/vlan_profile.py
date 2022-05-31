import argparse

from trex_stl_lib.api import *


class Profile:
    def get_streams(self, direction=0, tunables=(), **kwargs):
        ip_left = "16.0.0.1"
        port_left = 1025
        ip_right = "48.0.0.1"
        port_right = 12
        pkt = Ether()
        if direction == 0:
            pkt /= IP(src=ip_left, dst=ip_right)
            pkt /= UDP(sport=port_left, dport=port_right)

        else:
            pkt /= Dot1Q(vlan=int("{{vlan}}"))
            pkt /= IP(src=ip_right, dst=ip_left)
            pkt /= UDP(sport=port_right, dport=port_left)
        pkt /= b"x" * 20
        return [STLStream(packet=STLPktBuilder(pkt), mode=STLTXCont())]


def register():
    return Profile()
