from trex_stl_lib.api import *
import argparse


class STLS1:

    def get_streams (self, direction=0, tunables=(), **kwargs):
        parser = argparse.ArgumentParser()
        parser.add_argument("--numflows", type=int, default=1000)
        parser.add_argument("--size", type=int, default=60)
        args = parser.parse_args(tunables)

        p = Ether()
        p /= IP(src="48.0.0.1", dst="16.0.0.1")
        p /= UDP(sport=12, dport=1025, chksum=0)
        pad = max(0, args.size - len(p)) * b'x'
        p /= pad

        flow_vars = [
            STLVmTupleGen(
                name="gen",
                ip_min="16.0.0.1",
                ip_max="16.0.0.254",
                port_min=1025,
                port_max=65535,
                limit_flows=args.numflows,
            ),
            # force variable IP destination
            STLVmWrFlowVar(fv_name="gen.ip", pkt_offset= "IP.dst"),
            # force recalculate IP checksum
            STLVmFixIpv4(offset="IP"),
            # force variable UDP dest port
            STLVmWrFlowVar(fv_name="gen.port", pkt_offset="UDP.dport"),
            # no need to fix UDP checksum, it is left to 0
        ]

        return [
            STLStream(
                packet=STLPktBuilder(pkt=p, vm=STLScVmRaw(flow_vars)),
                mode=STLTXCont(),
            )
        ]


# dynamic load - used for trex console or simulator
def register():
    return STLS1()
