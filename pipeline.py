from agents import writer_chain, critic_chain
from tools import web_search, scrape_url
from rich import print

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # STEP 1 ---------- SEARCH
    print("\n" + " =" * 50)
    print("step 1 - search tool is working ...")
    print("=" * 50)

    search_results = web_search.invoke(topic)

    state["search_results"] = search_results

    print("\nsearch results:\n", state["search_results"])

    # STEP 2 ---------- SCRAPE
    print("\n" + " =" * 50)
    print("step 2 - scraping top resources ...")
    print("=" * 50)

    scraped_contents = []
    used_sources = []

    blocked_keywords = [
        "CLOUDFLARE",
        "enable javascript",
        "access denied",
        "captcha",
        "blocked"
    ]

    bad_content_keywords = [
        "about press copyright",
        "youtube",
        "how youtube works",
        "terms privacy",
        "google llc"
    ]

    skip_domains = [
        "youtube.com",
        "youtu.be"
    ]

    # scrape multiple good sources
    for result in search_results:

        try:
            url = result["url"]

            # skip bad domains
            if any(domain in url for domain in skip_domains):
                print(f"\nSkipping low quality domain: {url}")
                continue

            print(f"\nTrying URL: {url}")

            content = scrape_url.invoke(url)

            is_blocked = any(
                keyword.lower() in content.lower()
                for keyword in blocked_keywords
            )

            is_low_quality = any(
                keyword.lower() in content.lower()
                for keyword in bad_content_keywords
            )

            if is_blocked:
                print("Blocked page detected")
                continue

            if is_low_quality:
                print("Low quality content detected")
                continue

            # skip tiny/empty pages
            if len(content.strip()) < 500:
                print("Content too short")
                continue

            print(f"\nSuccessfully scraped: {url}")

            used_sources.append(url)

            scraped_contents.append({
                "url": url,
                "content": content[:4000]
            })

            # limit scraping to top 3 useful sources
            if len(scraped_contents) >= 3:
                break

        except Exception as e:
            print(f"Failed scraping {url}: {e}")

    # fallback
    if not scraped_contents:
        scraped_contents.append({
            "url": "No valid source found",
            "content": "No high quality content could be scraped."
        })

    state["used_sources"] = used_sources
    state["scraped_contents"] = scraped_contents

    print("\nSuccessfully used sources:\n")
    for src in used_sources:
        print(src)

    # STEP 3 ---------- WRITER
    print("\n" + " =" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = {
        "USED SOURCES": state["used_sources"],
        "SCRAPED RESEARCH": state["scraped_contents"]
    }

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal Report\n")
    print(state["report"])

    # STEP 4 ---------- CRITIC
    print("\n" + " =" * 50)
    print("step 4 - critic is reviewing the report")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\ncritic report\n")
    print(state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic : ")
    run_research_pipeline(topic)