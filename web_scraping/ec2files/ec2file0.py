from scraper import * 
s = Scraper(start=0, end=1781, max_iter=30, scraper_instance=0) 
ids = s.get_ids() 
s.scrape_letterboxd(ids)