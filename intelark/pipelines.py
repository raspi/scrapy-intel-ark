# -*- coding: utf-8 -*-
import os
import json
from tempfile import NamedTemporaryFile
from pathlib import Path
from shutil import move
from intelark.items import *


class IntelarkPipeline(object):
    """
    Save CPU specifications
    """

    def process_item(self, item, spider):
        if isinstance(item, CPUSpecsItem):
            # Save to temporary file
            tmpf = NamedTemporaryFile("w", prefix="cpu-specs-", suffix=".json", encoding="utf8", delete=False)
            with tmpf as f:
                json.dump(item, f)
                f.flush()
                spider.logger.info(f"saved as {f.name}")

            # path for saving
            fpath = os.path.abspath(os.path.join("..", "items", "cpuspecs", item["socket"]))
            Path(fpath).mkdir(parents=True, exist_ok=True)
            fname = item["id"] + ".json"
            fullpath = os.path.join(fpath, fname)

            # Rename and move the temporary file to actual file
            newpath = move(tmpf.name, fullpath)
            spider.logger.info(f"renamed {tmpf.name} to {newpath}")
            return

        spider.logger.error("Skipped item {0}".format(type(item)))
