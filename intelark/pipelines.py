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

    cpu_legend = CPULegendItem()

    def create_path(self, fpath):
        Path(fpath).mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        if isinstance(item, CPULegendItem):
            # Update legend information
            for i in item:
                if i in self.cpu_legend:
                    self.cpu_legend[i].update(item[i])
                else:
                    self.cpu_legend[i] = item[i]
            return

        if not (isinstance(item, CPUSpecsItem) or isinstance(item, CPUSpecsUnknownItem)):
            spider.logger.error("Skipped item {0}".format(type(item)))
            return

        # Save to temporary file
        tmpf = NamedTemporaryFile("w", prefix="cpu-specs-", suffix=".json", encoding="utf8", delete=False)
        with tmpf as f:
            json.dump(item, f)
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

    def close_spider(self, spider):
        if spider.name == "cpuspecs":
            # Save legend of different fields encountered in crawling

            # Save to temporary file
            tmpf = NamedTemporaryFile("w", prefix="cpu-legend-", suffix=".json", encoding="utf8", delete=False)
            with tmpf as f:
                json.dump(self.cpu_legend, f, indent=2)
                f.flush()
                spider.logger.info(f"saved as {f.name}")

            fullpath = os.path.abspath(os.path.join("..", "items", "cpuspecs", "_legend.json"))

            # Rename and move the temporary file to actual file
            newpath = move(tmpf.name, fullpath)
            spider.logger.info(f"renamed legend {tmpf.name} to {newpath}")
