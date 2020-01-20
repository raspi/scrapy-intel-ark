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

    def create_path(self, fpath):
        Path(fpath).mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        if not (isinstance(item, CPUSpecsItem) or isinstance(item, CPUSpecsUnknownItem)):
            spider.logger.error("Skipped item {0}".format(type(item)))
            return

        # Save to temporary file
        tmpf = NamedTemporaryFile("w", prefix="cpu-specs-", suffix=".json", encoding="utf8", delete=False)
        with tmpf as f:
            json.dump(item, f, indent=2)
            f.flush()
            spider.logger.info(f"saved as {f.name}")

        basepath = os.path.abspath(os.path.join("..", "items", "cpuspecs"))
        fullpath = os.path.abspath(os.path.join(basepath, "tmp"))

        if "id" in item:
            fname = item["id"] + ".json"
        else:
            fname = item["name"] + ".json"

        if isinstance(item, CPUSpecsItem):
            # path for saving
            fpath = os.path.abspath(os.path.join(basepath, item["socket"]))
            self.create_path(fpath)
            fullpath = os.path.join(fpath, fname)

        elif isinstance(item, CPUSpecsUnknownItem):
            # path for saving
            fpath = os.path.abspath(os.path.join(basepath, "_unknown", item["Essentials"]["MarketSegment"]))
            self.create_path(fpath)
            fullpath = os.path.join(fpath, fname)

        # Rename and move the temporary file to actual file
        newpath = move(tmpf.name, fullpath)
        spider.logger.info(f"renamed {tmpf.name} to {newpath}")
