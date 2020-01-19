# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path

from intelark.items import CPUSpecsItem


class IntelarkPipeline(object):
    def process_item(self, item, spider):

        if not isinstance(item, CPUSpecsItem):
            spider.logger.error(f"Skipped item")
            return

        fpath = os.path.abspath(os.path.join("..", "items", spider.name, item["socket"]))

        Path(fpath).mkdir(parents=True, exist_ok=True)
        fname = item["id"] + ".json"

        fullpath = os.path.join(fpath, fname)

        with open(fullpath, "w", encoding="utf8") as f:
            json.dump(item, f)
            spider.logger.info(f"saved {f.name}")
