import asyncio
import pandas as pd
import uuid
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter

class URLProcessor:
    def __init__(self, urls):
        self.urls = urls
        self.data = []
        self.browser_config =  BrowserConfig(
        verbose=True
        )
        self.md_generator = DefaultMarkdownGenerator(
            content_filter = PruningContentFilter(
                threshold=0.48,
                threshold_type="dynamic",
                min_word_threshold=10
            ),
            options={
            "ignore_links": True,
            "escape_html": False,
            "body_width": 80,
            "ignore_images": True,
            "skip_internal_links": True,
            "include_sup_sub": True
        }
    )
        self.run_config = CrawlerRunConfig(
            word_count_threshold=10,
            excluded_tags=['form', 'header', 'footer', 'nav'],
            exclude_external_links=True,
            process_iframes=True,
            remove_overlay_elements=True,
            only_text=True,
            cache_mode=CacheMode.BYPASS,
            markdown_generator=self.md_generator  # Replace with your markdown generator if needed
        )

    async def process_urls(self):
        async with AsyncWebCrawler(browser_config=self.browser_config) as crawler:
            for url in self.urls:
                result = await crawler.arun(
                    url=url,
                    config=self.run_config
                )
                if result.success:
                    md_object = result.markdown_v2
                    unique_id = str(uuid.uuid4())
                    self.data.append({
                        "url": url,
                        "unique_id": unique_id,
                        "content": md_object.fit_markdown
                    })
                else:
                    print(f"Not able to scrape the {url} with an error message {result.error_message}")
    
    def get_data_as_dataframe(self):
        return pd.DataFrame(self.data)



# Example usage
urls = ['https://timesofindia.indiatimes.com/technology/tech-news/indian-it-hiring-in-2025-the-jobs-that-will-be-in-biggest-demand/articleshow/116634317.cms', 'https://economictimes.indiatimes.com/news/company/corporate-trends/2025-forecast-what-does-2025-hold-for-indias-it-services-sector-tech-jobs-it-hiring-it-sector/articleshow/116880465.cms', 'https://jfsdigital.org/articles-and-essays/2017-2/year-2025-two-scenarios-for-the-indian-it-industry/', 'https://jfsdigital.org/wp-content/uploads/2017/10/Year-2025-Two-Scenarios-For-the-Indian-IT-Industry.pdf', 'https://www.quora.com/How-will-the-job-market-be-in-India-in-IT-in-2024-2025', 'https://www.livemint.com/news/india/job-scenario-indian-employers-hoping-to-outpace-others-in-chips-computing-tech-11736253791345.html', 'https://hr.economictimes.indiatimes.com/news/trends/22-lakh-indian-it-professionals-likely-to-leave-jobs-by-2025-report/94574864', 'https://www.hirist.tech/blog/top-10-it-companies-offering-permanent-work-from-home-2023/', 'https://www.business-standard.com/industry/news/indian-it-hiring-set-to-rebound-by-2025-ai-and-data-science-to-dominate-124122400224_1.html', 'http://jojulhij.pf/liderpen', 'http://uzsedul.lu/ehuihwo', 'https://content.techgig.com/hiring/2025-it-hiring-in-india-fresh-graduates-tier-2-cities-and-emerging-technologies/articleshow/116662874.cms', 'http://bakpowa.qa/azise', 'https://aimexpress.in/indian-it-hiring-in-2025-set-to-rebound-with-ai-and-data-science-roles-leading-the-job-market/', 'http://ted.br/cadus', 'https://acarasolutions.in/blog/indias-it-industry-in-2025-growth-trends-challenges/', 'http://iv.edu/ofo', 'https://economictimes.indiatimes.com/jobs/hr-policies-trends/indias-job-market-projected-to-grow-9-pc-in-2025-led-by-it-retail-telecom-bfsi-sectors-report/articleshow/116474136.cms', 'https://ianslive.in/it-jobs-set-to-surge-by-85-pc-in-2025-gccs-the-driver-report--20240808175018', 'https://timesofindia.indiatimes.com/business/india-business/good-news-for-freshers-indian-it-sector-entry-level-hiring-set-to-double-in-fy25/articleshow/113842030.cms', 'https://www.shiksha.com/online-courses/articles/top-highest-paid-jobs-it-sector/', 'https://karat.com/how-tech-hiring-is-changing-for-2025/', 'https://www.hirist.tech/blog/recession-in-it-sector-when-will-it-start-and-end/', 'https://www.cnbctv18.com/business/information-technology/it-hiring-india-2024-it-jobs-seen-recovering-from-january-2025-19477203.htm', 'https://www.ibef.org/industry/information-technology-india', 'https://economictimes.indiatimes.com/topic/indian-job-scenario', 'https://www.livemint.com/industry/infotech/huge-hiring-by-indian-it-companies-seen-expected-in-coming-months-11625727080259.html', 'http://hiohemi.vc/toheha', 'https://www.ndtv.com/education/explained-it-sectors-ai-first-vision-and-hiring-trends-for-2025-7540022', 'http://udo.eh/aneto', 'https://money.rediff.com/news/market/indian-it-hiring-rebound-in-2025-ai-data-science-jobs-to-boom/20098720241224', 'http://da.ki/ponaek', 'https://www.siasat.com/indian-companies-to-increase-hiring-by-10-pc-in-2025-report-3156222/', 'http://jidmebdec.ax/ze', 'https://analyticsindiamag.com/it-services/what-to-expect-from-indian-it-in-2025/', 'http://abo.mr/ger', 'https://hr.economictimes.indiatimes.com/news/trends/indian-it-hiring-2025-promises-rebound-ai/data-science-roles-to-dominate-job-market/116635320', 'https://telecom.economictimes.indiatimes.com/news/industry/hiring-in-indian-it-sector-likely-to-see-8-10-growth-in-2024-report/106318083', 'https://bestcolleges.indiatoday.in/news-detail/india-job-outlook-2025-how-it-energy-infra-logistics-will-drive-hiring', 'https://economictimes.indiatimes.com/jobs/hr-policies-trends/indian-it-hiring-2025-promises-rebound-ai/data-science-roles-to-dominate-job-market/articleshow/116619527.cms', 'https://m.economictimes.com/tech/information-tech/hiring-in-indian-it-sector-likely-to-see-8-10-growth-in-2024-report/amp_articleshow/106316064.cms', 'https://upstox.com/news/business-news/latest-updates/indian-it-hiring-expected-to-rebound-in-2025-ai-data-science-roles-to-dominate-job-market/article-136809/', 'https://www.careerindia.com/news/indian-it-industry-recovery-2025-outlook-011-046539.html', 'https://m.economictimes.com/jobs/hr-policies-trends/indias-job-market-projected-to-grow-9-pc-in-2025-led-by-it-retail-telecom-bfsi-sectors-report/amp_articleshow/116474136.cms', 'https://news.outsourceaccelerator.com/indian-it-job-market-growth-by-2025/', 'https://www.business-standard.com/technology/tech-news/emerging-tech-to-drive-india-s-job-market-with-20-growth-in-2025-report-124123100686_1.html']


processor = URLProcessor(urls)
# To run the async method, you need to use an event loop
asyncio.run(processor.process_urls())

df = processor.get_data_as_dataframe()
df.to_excel("search_output_1.xlsx", index=False)