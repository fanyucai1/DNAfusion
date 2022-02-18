import argparse
import os
import sys
import re

args=argparse.ArgumentParser("Find DNA fusion use genefuse and factera.")
args.add_argument("-p1","--pe1",required=True)
args.add_argument("-p2","--pe2",required=True)

