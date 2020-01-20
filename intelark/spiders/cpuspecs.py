# -*- coding: utf-8 -*-
import scrapy

from intelark.items import *


def floatConv(value: str):
    fl, unit = value.split(" ")
    return {"value": float(fl), "unit": unit}


def sizeToBytes(value: str):
    num, unit = value.split(" ")
    num = int(num)

    units = ["B", "KB", "MB", "GB", "TB"]
    if unit not in units:
        raise ValueError(f"unit {unit} not in units")

    for idx, u in enumerate(units):
        if unit == u:
            break

        num *= 1024

    return num


def speedToHz(value: str):
    num, unit = value.split(" ")
    num = float(num)

    units = ["Hz", "kHz", "MHz", "GHz", "THz"]
    if unit not in units:
        raise ValueError(f"unit {unit} not in units")

    for idx, u in enumerate(units):
        if unit == u:
            break

        num *= 1000.0

    return num


convertTo = {
    "NumPCIExpressPorts": int,
    "MaxCPUs": int,
    "NumMemoryChannels": int,
    "CoreCount": int,
    "ThreadCount": int,
    "NumUSBPorts": int,
    "NumSATAPorts": int,
    "SATA6PortCount": int,
    "ClockSpeed": speedToHz,
    "GraphicsFreq": speedToHz,
    "GraphicsMaxFreq": speedToHz,
    "ClockSpeedMax": speedToHz,
    "TurboBoostMaxTechMaxFreq": speedToHz,
    "GraphicsMaxMem": sizeToBytes,
}


class BaseSpider(scrapy.Spider):
    """
    Base spider for common tasks
    """

    def parse(self, response):
        raise NotImplementedError

    def cleantxt(self, v: str) -> str:
        v = v.replace("Intel", "")
        v = v.replace("\u2122", " ")  # tm
        v = v.replace("\u00ae", " ")  # (c)
        v = v.replace("\u2021", " ")  #

        v = ' '.join(v.split())
        v = v.strip()
        return v

    def parse_specs(self, response):
        """
        Get specifications of one CPU
        """

        cpuname = response.xpath("//div/h1/text()").get()
        cpuname = self.cleantxt(cpuname)

        specs = {
            "URL": response.url,
            "name": cpuname,
        }

        for section in response.xpath("//div[@class='arkProductSpecifications']/div/section/div"):
            header = section.xpath("div/h2/text()").get()
            if header not in specs:
                # Add header
                specs[header] = {}

            for data in section.xpath("ul[@class='specs-list']/li"):
                # Find specifications under each header
                k = data.xpath("span[@class='value']/@data-key").get()

                if k == "null":
                    continue

                v = data.xpath("span[@class='value']//text()").get().strip()

                v = self.cleantxt(v)

                if v == 'Yes':
                    v = True
                elif v == 'No':
                    v = False
                elif v == '':
                    v = None
                elif k in convertTo:
                    # Try to convert value to machine parsable presentation
                    try:
                        v = convertTo[k](v)
                    except ValueError as e:
                        raise ValueError(f"FAILED: {k}: {v}")

                specs[header][k] = v

        # Specification object is now complete
        has_socket = True
        has_id = True

        if "SocketsSupported" not in specs["Package Specifications"]:
            has_socket = False

        if "ProcessorNumber" not in specs["Essentials"]:
            has_id = False

        if has_id:
            # CPU specs lists number such as Q6600
            specs["id"] = specs["Essentials"]["ProcessorNumber"]
            del specs["Essentials"]["ProcessorNumber"]

        if has_socket:
            # many sockets might be supported
            sockets = specs["Package Specifications"]["SocketsSupported"].split(", ")
            del specs["Package Specifications"]["SocketsSupported"]

            for socket in sockets:
                specs["socket"] = socket
                yield CPUSpecsItem(specs)
        else:
            yield CPUSpecsUnknownItem(specs)


class CpuSpecListSpider(BaseSpider):
    """
    Spider for getting list of CPUs
    """
    name = 'cpuspecs'
    allowed_domains = ['ark.intel.com']
    start_urls = ['https://ark.intel.com/content/www/us/en/ark.html']

    def parse(self, response):
        for panelId in response.xpath("//div[@data-parent-panel-key='Processors']/div/div/@data-panel-key"):
            # Series such as Core, Atom, Xeon, etc, ....
            for link in response.xpath(f"//div[@data-parent-panel-key='{panelId.root}']/div/div/span/a/@href"):
                yield scrapy.Request(response.urljoin(link.root), callback=self.parse_series)

    # Series-specific CPU list such as Atom CPUs
    def parse_series(self, response):
        for link in response.xpath("//tr/td/a/@href"):
            if link.root.find("/products/") == -1:
                self.logger.error("product not found from link, skipping")
                continue
            yield scrapy.Request(response.urljoin(link.root), callback=self.parse_specs)


class CpuSpecSpider(BaseSpider):
    """
    Spider for getting CPU specifications for one CPU
    """
    name = 'onecpuspec'
    allowed_domains = ['ark.intel.com']
    start_urls = ['https://ark.intel.com/content/www/us/en/ark/products/']

    def __init__(self, url: str):
        if url == "":
            url = None

        if url is None:
            raise ValueError("Invalid url given")

        self.start_urls = [url]

    def parse(self, response):
        yield self.parse_specs(response)
