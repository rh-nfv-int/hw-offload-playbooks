import ipaddress
import argparse

from trex_stl_lib.api import *

import rss

class STLS1:
    def queue_ratios(self, arg):
        ratios = tuple(float(r) for r in arg.split(":"))
        return tuple(r / sum(ratios) for r in ratios)

    def get_streams(self, direction=0, tunables=(), **kwargs):
        parser = argparse.ArgumentParser()
        parser.add_argument("--queue-ratios", type=self.queue_ratios, default=(1.0,))
        parser.add_argument("--size", type=int, default=64)
        args = parser.parse_args(tunables)
        args.size -= 4  # strip ethernet CRC (added by hardware on tx)

        algo = rss.RSSAlgo(
            queues_count=len(args.queue_ratios),
            key=rss.RSS_KEY_I40E,
            reta_size=512,
            use_l4_port=True,
        )
        template = rss.TrafficTemplate(
            ipaddress.ip_network("16.0.0.1/32"),
            ipaddress.ip_network("48.0.0.0/24"),
            (12,),
            (1025,),
        )

        streams = []
        for q, _, pkt in rss.balanced_traffic(algo, template):
            p = Ether()
            p /= IP(src=str(pkt.ip_src), dst=str(pkt.ip_dst))
            p /= UDP(sport=pkt.l4_sport, dport=pkt.l4_dport)
            p /= max(0, args.size - len(p)) * b"x"  # padding
            streams.append(
                STLStream(
                    packet=STLPktBuilder(pkt=p),
                    mode=STLTXCont(pps=args.queue_ratios[q]),
                )
            )

        return streams

# dynamic load - used for trex console or simulator
def register():
    return STLS1()

