
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter

async def main():
    browser_config = BrowserConfig(
        verbose=True,
        headless=False,
        )
    md_generator = DefaultMarkdownGenerator(
            content_filter = PruningContentFilter(
                threshold=0.48,
                threshold_type="fixed",
                min_word_threshold=5
            ),
            # content_filter = BM25ContentFilter(
            #     user_query="Generative AI",
            #     # Adjust for stricter or looser results
            #     bm25_threshold=1.2  
    #),
        options={
            "ignore_links": True,
            "escape_html": False,
            "body_width": 80,
            "ignore_images": True,
            "skip_internal_links": True,
            "include_sup_sub": True
        }
    )
   
    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        excluded_tags=['form', 'header', 'footer', 'nav'],
        #exclude_external_links=True,
        #process_iframes=False,
        #remove_overlay_elements=True,
        only_text=True,
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator,
        delay_before_return_html = 5.0,
        css_selector=".main-content",  # Focus on .main-content region only
        remove_forms=True,             # Specifically strip <form> elements
        remove_overlay_elements=True,  # Attempt to remove modals/popups
    )

    async with AsyncWebCrawler(browser_config=browser_config) as crawler:
        result = await crawler.arun("https://agraniai.com/about-us/",
        run_config=run_config
        )
        if result.success:
            print("Raw Content:",result.markdown)
            print("========================================================================================")     
            print("Markdown Content:",result.markdown_v2.raw_markdown)
            print("========================================================================================")
            print("Fit MarkDown:",result.markdown_v2.fit_markdown)
            print("========================================================================================")

        else:
            print(result.error_message)
        
if __name__ == "__main__":
    asyncio.run(main())