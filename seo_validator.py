import requests
from bs4 import BeautifulSoup
import time

page_url = input("Enter Page URL: ").strip()
expected_canonical = input("Enter Expected Canonical URL: ").strip()

score = 0
total = 0

try:
    response = requests.get(
        page_url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15
    )

    soup = BeautifulSoup(response.text, "lxml")

    print("\n================ SEO REPORT ================\n")

    # STATUS CODE
    total += 1
    if response.status_code == 200:
        score += 1
        print(f"PASS  Status Code : {response.status_code}")
    else:
        print(f"FAIL  Status Code : {response.status_code}")

    # CANONICAL
    print("\nCANONICAL")
    print("--------------------------------")

    canonical = soup.find("link", rel="canonical")

    if canonical:
        actual = canonical.get("href", "").strip()

        total += 1
        score += 1
        print("Present : PASS")

        print(f"Expected : {expected_canonical}")
        print(f"Actual   : {actual}")

        total += 1
        if actual == expected_canonical:
            score += 1
            print("Match    : PASS")
        else:
            print("Match    : FAIL")
    else:
        total += 2
        print("Canonical Missing")

    # TITLE
    print("\nTITLE")
    print("--------------------------------")

    title = soup.title.string.strip() if soup.title else ""

    print(f"Value : {title}")

    total += 1
    if title:
        score += 1
        print("Result : PASS")
    else:
        print("Result : FAIL")

    total += 1
    if 30 <= len(title) <= 60:
        score += 1
        print(f"Length : {len(title)} (PASS)")
    else:
        print(f"Length : {len(title)} (FAIL)")

    # META DESCRIPTION
    print("\nMETA DESCRIPTION")
    print("--------------------------------")

    meta = soup.find("meta", attrs={"name": "description"})
    desc = meta.get("content", "").strip() if meta else ""

    print(f"Value : {desc}")

    total += 1
    if desc:
        score += 1
        print("Result : PASS")
    else:
        print("Result : FAIL")

    total += 1
    if 50 <= len(desc) <= 160:
        score += 1
        print(f"Length : {len(desc)} (PASS)")
    else:
        print(f"Length : {len(desc)} (FAIL)")

    # H1
    print("\nH1 TAGS")
    print("--------------------------------")

    h1s = soup.find_all("h1")

    if h1s:
        for i, h1 in enumerate(h1s, 1):
            print(f"H1-{i}: {h1.get_text(strip=True)}")

    total += 1
    if len(h1s) > 0:
        score += 1
        print("Present : PASS")
    else:
        print("Present : FAIL")

    total += 1
    if len(h1s) == 1:
        score += 1
        print("Count   : PASS")
    else:
        print(f"Count   : FAIL ({len(h1s)})")

    # ROBOTS
    print("\nROBOTS META")
    print("--------------------------------")

    robots = soup.find("meta", attrs={"name": "robots"})

    total += 1
    if robots:
        score += 1
        robots_value = robots.get("content", "")
        print(f"Value  : {robots_value}")
        print("Result : PASS")
    else:
        print("Result : FAIL")

    # OPEN GRAPH
    print("\nOPEN GRAPH")
    print("--------------------------------")

    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")

    total += 1
    if og_title:
        score += 1
        print("OG Title:")
        print(og_title.get("content", ""))
        print("Result : PASS")
    else:
        print("OG Title Missing")

    total += 1
    if og_desc:
        score += 1
        print("\nOG Description:")
        print(og_desc.get("content", ""))
        print("Result : PASS")
    else:
        print("OG Description Missing")

    # TWITTER
    print("\nTWITTER TAGS")
    print("--------------------------------")

    tw_title = soup.find("meta", attrs={"name": "twitter:title"})
    tw_desc = soup.find("meta", attrs={"name": "twitter:description"})

    total += 1
    if tw_title:
        score += 1
        print("Twitter Title:")
        print(tw_title.get("content", ""))
        print("Result : PASS")
    else:
        print("Twitter Title Missing")

    total += 1
    if tw_desc:
        score += 1
        print("\nTwitter Description:")
        print(tw_desc.get("content", ""))
        print("Result : PASS")
    else:
        print("Twitter Description Missing")

    # SCHEMA
    print("\nSCHEMA")
    print("--------------------------------")

    schema = soup.find_all("script", type="application/ld+json")

    total += 1
    if schema:
        score += 1
        print(f"Schema Count : {len(schema)}")
        print("Result : PASS")
    else:
        print("Result : FAIL")

    print("\n===========================================")
    print(f"OVERALL SCORE : {score}/{total}")

    if score == total:
        print("SEO STATUS : PASS")
    else:
        print("SEO STATUS : REVIEW REQUIRED")

except Exception as e:
    print(f"ERROR : {e}")

print("\nClosing in 15 seconds...")
time.sleep(15)
