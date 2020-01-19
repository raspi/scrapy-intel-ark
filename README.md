# scrapy-intel-ark
Web crawler for Intel ARK ([ark.intel.com](https://ark.intel.com))

## Requirements

* Python
* [Scrapy](https://scrapy.org/)

## CPU specs spider

Downloads all CPU specifications as JSON files.

    scrapy crawl cpuspecs
    
Everything is downloaded to `items/cpuspecs` directory. Each CPU is in it's own socket subdirectory. 

### Notes
* 30 day cache is used in `settings.py`
* Some product information pages do **not** contain CPU product ID (**Q6600**), so they are skipped
* Some product information pages do **not** contain socket information, so they are skipped
