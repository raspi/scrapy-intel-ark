# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from intelark.items import *


class IntelarkPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CPUSpecsItem):
            fpath = os.path.abspath(os.path.join("..", "items", "cpuspecs", item["socket"]))

            Path(fpath).mkdir(parents=True, exist_ok=True)
            fname = item["id"] + ".json"

            fullpath = os.path.join(fpath, fname)

            with open(fullpath, "w", encoding="utf8") as f:
                json.dump(item, f)
                spider.logger.info(f"saved {f.name}")

            return

        spider.logger.error("Skipped item {0}".format(type(item)))
