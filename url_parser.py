# -*- coding: utf-8 -*-

import asyncio
from playwright.async_api import async_playwright, Error as PlaywrightError
import logging
from urllib.parse import urljoin, urlparse
import json
import csv
import random
import argparse

CONCURRENT_REQUESTS = 10
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
]

def setup_logger():
    """
    Sets up an advanced logger. Logs to both file and console.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler("scraper.log", mode='w', encoding='utf-8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

logger = setup_logger()

def save_to_json(data, filename="url_structure.json"):
    """
    Saves data to a JSON file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Data saved to {filename}.")
    except IOError as e:
        logger.error(f"Error writing to {filename}: {e}")

def save_to_csv(data, filename="scraped_urls.csv"):
    """
    Saves data to a CSV file.
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["URL"])
            for url in data:
                writer.writerow([url])
        logger.info(f"Data saved to {filename}.")
    except IOError as e:
        logger.error(f"Error writing to {filename}: {e}")

def save_to_txt(data, filename="scraped_urls.txt"):
    """
    Saves data to a TXT file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for url in data:
                f.write(f"{url}\n")
        logger.info(f"Data saved to {filename}.")
    except IOError as e:
        logger.error(f"Error writing to {filename}: {e}")

def build_tree_string(url, structure, prefix="", visited=None):
    """
    Recursively builds a string representation of the URL tree.
    """
    if visited is None: visited = set()
    if url in visited: return ""
    visited.add(url)
    children = structure.get(url, [])
    tree_string = f"{prefix}├── {url}\n"
    for i, child in enumerate(children):
        is_last = i == len(children) - 1
        child_prefix = prefix + ("    " if is_last else "│   ")
        tree_string += build_tree_string(child, structure, child_prefix, visited)
    return tree_string

def visualize_url_structure(url_structure, start_url, filename="url_tree.txt"):
    """
    Saves the URL structure as a tree in a text file.
    """
    tree_representation = f"{start_url}\n"
    if start_url in url_structure:
        for i, link in enumerate(url_structure[start_url]):
            is_last = i == len(url_structure[start_url]) - 1
            prefix = "└── " if is_last else "├── "
            tree_representation += build_tree_string(link, url_structure, prefix, visited={start_url})
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(tree_representation)
        logger.info(f"URL tree structure saved to {filename}.")
    except IOError as e:
        logger.error(f"Error writing URL tree to file: {e}")

async def fetch_urls(context, url, semaphore):
    """
    Fetches all links from a given URL.
    """
    async with semaphore:
        user_agent = random.choice(USER_AGENTS)
        page = await context.new_page(user_agent=user_agent)
        logger.info(f"Scanning URL: {url} (User-Agent: {user_agent})")

        await asyncio.sleep(random.uniform(1, 3)) # Random delay

        try:
            await page.goto(url, timeout=10000, wait_until="domcontentloaded")
            links = await page.eval_on_selector_all("a", "elements => elements.map(element => element.href)")
            base_url = page.url
            links = [urljoin(base_url, link).rstrip('/') for link in links]
            logger.info(f"{len(links)} links found at: {url}")
            return links, url
        except PlaywrightError as e:
            logger.error(f"Playwright error at {url}: {e}")
            return [], url
        except Exception as e:
            logger.error(f"General error while scanning {url}: {e}")
            return [], url
        finally:
            await page.close()

async def crawl_website(context, start_url, max_depth=5):
    """
    Crawls a website up to a specific depth.
    """
    visited_urls = set()
    url_structure = {}
    tasks = []
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    domain = urlparse(start_url).netloc

    tasks.append(fetch_urls(context, start_url, semaphore))

    while tasks:
        completed_tasks, pending_tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        tasks = list(pending_tasks)

        for task in completed_tasks:
            links, url = task.result()

            if url in visited_urls:
                continue

            visited_urls.add(url)
            url_structure[url] = links

            path = urlparse(url).path
            depth = len(path.split('/')) -1
            if depth >= max_depth:
                continue

            for link in links:
                if link not in visited_urls and urlparse(link).netloc == domain:
                    tasks.append(fetch_urls(context, link, semaphore))

    return visited_urls, url_structure

async def main(start_url, max_depth):
    """
    Main function.
    """
    logger.info(f"Scan started for: {start_url}")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            visited_urls, url_structure = await crawl_website(context, start_url, max_depth)
            await browser.close()
        except PlaywrightError as e:
            logger.critical(f"Critical Playwright error during startup or execution: {e}")
            return
        except Exception as e:
            logger.critical(f"Unexpected error in main process: {e}")
            return

    all_urls = list(visited_urls)
    logger.info(f"Scan complete. Found {len(all_urls)} unique URLs.")

    logger.info("Saving data...")
    save_to_json(url_structure)
    save_to_csv(all_urls)
    save_to_txt(all_urls)
    visualize_url_structure(url_structure, start_url)
    logger.info("All operations completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraper for URL parsing.")
    parser.add_argument("start_url", help="The starting URL to crawl.")
    parser.add_argument("--max_depth", type=int, default=5, help="Maximum crawl depth.")
    args = parser.parse_args()

    asyncio.run(main(args.start_url, args.max_depth))
