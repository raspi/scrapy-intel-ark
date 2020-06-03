# -*- coding: utf-8 -*-
from urllib.parse import urlsplit

import scrapy
from scrapy.exceptions import CloseSpider

from intelark.converters import *
from intelark.items import *

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
    "NumDisplaysSupported": int,
    "MaxMem": sizeToBytes,
    "EmbeddedDramMB": sizeToBytes,
    "MaxMemoryBandwidth": sizeToBytes,
    "UltraPathInterconnectLinks": int,
    "AVX512FusedMultiplyAddUnits": int,
    "InstructionSetExtensions": toList,
    "DiscreteGraphicsComputeUnitCount": int,
    "DiscreteNumDisplaysSupported": int,
    "MemoryMaxSpeedMhz": speedToHz,
    "PackageSize":toPackage,
    "MaxTDP": toTDP,
    "BusNumPorts": int,
}


class BaseSpider(scrapy.Spider):
    """
    Base spider for common tasks
    """

    def parse(self, response):
        raise NotImplementedError

    def cleantxt(self, v: str) -> str:
        v = v.replace("Intel", "")
        v = v.replace("\u2122", "")  # tm
        v = v.replace("\u00ae", "")  # (c)
        v = v.replace("\u2021", "")  #

        v = ' '.join(v.split())
        v = v.strip()
        return v

    # Series-specific CPU list such as Atom CPUs
    def parse_series(self, response: scrapy.http.Response):
        for link in response.xpath("//tr/td/a/@href"):
            if link.root.find("/products/") == -1:
                self.logger.error("product not found from link, skipping")
                continue
            yield scrapy.Request(response.urljoin(link.root), callback=self.parse_specs)

    def parse_specs(self, response: scrapy.http.Response):
        """
        Get specifications of one CPU
        """

        # Get Intel Ark internal CPU id from URL
        arkcpuid = int(urlsplit(response.url).path.strip('/').split('/')[6])

        cpuname = response.xpath("//div/h1/text()").get()
        cpuname = self.cleantxt(cpuname)

        specs = {
            "URL": response.url,
            "name": cpuname,
            "arkid": arkcpuid,
        }

        # Collect explanations of different fields
        # For example:
        # "GraphicsMaxFreq": "Graphics Max Dynamic Frequency"
        legends = {}

        for section in response.xpath("//div[@class='arkProductSpecifications']/div/section/div"):
            header = section.xpath("div/h2/text()").get()
            if header not in specs:
                # Add header
                specs[header] = {}
                legends[header] = {}

            for data in section.xpath("ul[@class='specs-list']/li"):
                # Find specifications under each header
                k = data.xpath("span[@class='value']/@data-key").get()

                if k == "null":
                    continue

                legend = "".join(data.xpath("span[@class='label']//text()").getall()).strip()
                legends[header][k] = self.cleantxt(legend)

                # Get value, such as "5 GHz"
                v = "".join(data.xpath("span[@class='value']//text()").getall()).strip()

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
                        reason = f"FAILED: {k}: {v}"
                        # Stop the entire spider (for debugging purposes)
                        #raise scrapy.exceptions.CloseSpider(reason)
                        raise ValueError(reason)

                specs[header][k] = v

        # Specification object is now complete

        yield CPULegendItem(legends)

        has_socket = False
        has_id = False

        if "SocketsSupported" in specs["Package Specifications"]:
            has_socket = True

        if "ProcessorNumber" in specs["Essentials"]:
            has_id = True

        if has_id:
            # CPU specs lists number such as Q6600
            specs["id"] = specs["Essentials"]["ProcessorNumber"]
            del specs["Essentials"]["ProcessorNumber"]

        if not has_socket:
            yield CPUSpecsUnknownItem(specs)
        else:
            # many sockets might be supported
            sockets = specs["Package Specifications"]["SocketsSupported"].split(", ")
            del specs["Package Specifications"]["SocketsSupported"]

            for socket in sockets:
                specs["socket"] = socket
                yield CPUSpecsItem(specs)


class CpuSpecListSpider(BaseSpider):
    """
    Spider for getting list of CPUs
    """
    name = 'cpuspecs'
    allowed_domains = ['ark.intel.com']
    start_urls = ['https://ark.intel.com/content/www/us/en/ark.html']

    def parse(self, response: scrapy.http.Response):
        for panelId in response.xpath("//div[@data-parent-panel-key='Processors']/div/div/@data-panel-key"):
            # Series such as Core, Atom, Xeon, etc, ....
            for link in response.xpath(f"//div[@data-parent-panel-key='{panelId.root}']/div/div/span/a/@href"):
                yield scrapy.Request(response.urljoin(link.root), callback=self.parse_series)


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

        if url.find("/products/") == -1:
            raise ValueError(f"/products/ not found from url {url}")

        self.start_urls = [url]

    def parse(self, response: scrapy.http.Response):
        yield scrapy.Request(response.url, callback=self.parse_specs)


class SeriesSpider(BaseSpider):
    """
    Spider for getting CPU specifications for series of CPUs
    Example: 2nd Generation Intel® Xeon® Scalable Processors
    """
    name = 'series'
    allowed_domains = ['ark.intel.com']
    start_urls = ['https://ark.intel.com/content/www/us/en/ark/products/series/']

    def __init__(self, url: str):
        if url == "":
            url = None

        if url is None:
            raise ValueError("Invalid url given")

        if url.find("/products/") == -1:
            raise ValueError(f"/products/ not found from url {url}")

        if url.find("/series/") == -1:
            raise ValueError(f"/series/ not found from url {url}")

        self.start_urls = [url]

    def parse(self, response: scrapy.http.Response):
        yield scrapy.Request(response.url, callback=self.parse_series)
