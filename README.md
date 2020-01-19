# scrapy-intel-ark
Web crawler for Intel ARK (ark.intel.com)

## Requirements

* Python
* [Scrapy](https://scrapy.org/)

## CPU specs spider

    scrapy crawl cpuspecs
    
Everything is downloaded to `./items/cpuspecs` directory in JSON format. Each CPU is in it's own socket directory. 

### Notes
* Some product information pages do **not** contain CPU product ID (**Q6600**), so they are skipped
* Some product information pages do **not** contain socket information, so they are skipped