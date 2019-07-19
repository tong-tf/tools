#!/usr/bin/env python
# -*- coding: utf8 -*-

"""LCM fps adjust

Usage:
  lcm_fps.py (-h | --help)
  lcm_fps.py DTS FPS
  lcm_fps.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import sys
import re
import os
from docopt import docopt

brace_number = re.compile(r'<(\d+)>')

dts_folder = r'X:\code\O13399_git\alps\kernel\arch\arm64\boot\dts\rockchip'
lcm = os.path.join(dts_folder, "lcd-OTA7290B-boe101-wuxga.dtsi")

def lcm_fps_modify(inf, fps, outf=None):
    timing = {
        "hactive": 0,
        "vactive": 0,
        "hsync-len": 0,
        "hback-porch": 0,
        "hfront-porch": 0,
        "vsync-len":0,
        "vback-porch": 0,
        "vfront-porch": 0,
        "clock-frequency": 0
    }
    lines = []
    clk_index = 0
    fps = int(fps)
    with open(inf) as fp:
        lines = fp.readlines()
    for i, line in enumerate(lines):
        for k in timing:
            if k in line:
                timing[k] = int(brace_number.findall(line)[0])
                if k == "clock-frequency":
                    clk_index = i
    timing['clock-frequency'] =(fps * (timing['hactive']  + timing['hsync-len'] + timing['hback-porch'] + timing['hfront-porch'])
                                    *( timing["vactive"] + timing['vsync-len'] + timing["vback-porch"] + timing["vfront-porch"]))
    lines[clk_index] = brace_number.sub("<{}>".format(timing['clock-frequency']), lines[clk_index])
    outf = outf or os.path.join(dts_folder, "out.dtsi")
    with open(outf, "w") as fp:
        fp.writelines(lines)

#lcm_fps_modify(lcm, 55)

def main():
    args = docopt(__doc__)
    lcm_fps_modify(args['DTS'], args['FPS'], args['DTS'])

if __name__ == "__main__":
    main()