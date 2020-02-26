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
    cpu_prices = CPUPriceItem()

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
            # self.cpu_legend.update(item)
            return

        if isinstance(item, CPUPriceItem):
            self.cpu_prices.update(item)
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

        fname = item["number"] + ".json" if "number" in item else item["name"] + ".json"

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
            self.saveToFile(spider, self.cpu_legend, "_legend")
            # Save legend of different fields encountered in crawling
            self.saveToFile(spider, self.cpu_prices, "cpuprices")

    def saveToFile(self, spider, data, name):
        # Save to temporary file
        tmpf = NamedTemporaryFile("w", prefix=f"cpuspecs-{name}-", suffix=".json", encoding="utf8", delete=False)
        with tmpf as f:
            json.dump(data, f, indent=2)
            f.flush()
            spider.logger.info(f"saved as {f.name}")
        # Rename and move the temporary file to actual file
        fullpath = os.path.abspath(os.path.join("..", "items", "cpuspecs", f"{name}.json"))
        newpath = move(tmpf.name, fullpath)
        spider.logger.info(f"renamed legend {tmpf.name} to {newpath}")
