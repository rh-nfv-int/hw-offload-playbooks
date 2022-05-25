import argparse

from trex_stl_lib.api import *


class Profile:
    def get_streams(self, direction=0, tunables=(), **kwargs):
        parser = argparse.ArgumentParser()
        parser.add_argument("--vlan", type=int, default=int("{{vlan}}"))
        args = parser.parse_args(tunables)

        pkt = Ether()

        if direction == 0:
            pkt /= IP(src="16.0.0.1", dst="48.0.0.1")
            pkt /= UDP(dport=12, sport=1025)

        else:
            pkt /= Dot1Q(prio=1, vlan=args.vlan)
            pkt /= IP(src="48.0.0.1", dst="16.0.0.1")
            pkt /= UDP(dport=1025, sport=12)

        pkt /= b"x" * 20

        return [STLStream(packet=STLPktBuilder(pkt), mode=STLTXCont())]


def register():
    return Profile()
