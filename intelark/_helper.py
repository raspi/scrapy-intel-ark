# Helper for IDE
import sys
from scrapy import cmdline

cmds = ["scrapy"]
cmds.extend(sys.argv[1:])
cmdline.execute(cmds)
