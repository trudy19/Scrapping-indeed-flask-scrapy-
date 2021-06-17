import scrapy
from items import IndeedItem


# use crrawler process to run spider from within a python script
from scrapy.crawler import CrawlerProcess

# needed to parse settings
import json
class BloparsegSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.indeed.com/jobs?q=sales+representative&l=United+States&start=0']
    item_count = 0


    def start_requests(self):
        # reset output file
        with open('wellness.jsonl', 'w') as f:
            f.write('')
    
        # settings content
        settings = ''
        
        # load settings from local file
        with open('settings.json', 'r') as f:
            for line in f.read():
                settings += line
        
        # parse settings
        settings = json.loads(settings)
        yield scrapy.Request('https://www.indeed.com/jobs?q=sales+representative&l=United+States&start=0', callback=self.parse)

    def state(self, response):
        jobs=response.xpath('.//*[@data-tn-component="organicJob"]')
        for a in jobs:
            yield response.follow(a, callback=self.parse)



    def parse(self, response):        
        jobs=response.xpath('.//*[@data-tn-component="organicJob"]')
        print("number og job per page")
        print(len(jobs))
        item = {}
                   

        for job in jobs:
            
            item['title'] = job.xpath('.//a[@data-tn-element="jobTitle"]/@title').get()
            item['link_url'] = job.xpath(".//h2[@class='title']//a/@href").get()
            item['location'] = job.xpath('.//span[@class="location accessible-contrast-color-location"]/text()').get()
            item['company'] = job.xpath(".//span[@class='company']//a/text()").extract() 
            string=''
            for i in job.xpath(".//div[@class='summary']//ul/li/text()").extract():
                string =string+i
            item['description']=string 
            print(job.xpath('.//a[@data-tn-element="jobTitle"]/@title').extract()[0])
            with open('wellness.jsonl', 'a') as f:
                print ("saved")
                f.write(json.dumps(item, indent=2) + '\n')
            self.item_count += 1
            yield item
        print(self.item_count)
        if self.item_count > 29:
            with open('wellness.jsonl', 'a') as f:
                print ("saved")
              #  f.write(json.dumps(item, indent=2) + ']'+'\n')
            #raise CloseSpider('item_exceeded')
            return item
 
        next_page_url = response.css('#resultsCol > nav > div > ul > li > a::attr(href)').extract_first()

        if next_page_url:
            link_first, link_second = response.url.split('&start=')
            link_second = int(link_second) + 10
            link = f'{link_first}&start={link_second}'
            if link_second==50 :
                return item

            print(link)
            yield response.follow(link, self.parse)


            #next_page_url = response.urljoin(next_page_url)
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(BloparsegSpider)
    process.start()      