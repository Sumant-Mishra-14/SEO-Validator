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

    # Status Code
    total += 1
    if response.status_code == 200:
        score += 1
        print("PASS  Status Code (200)")
    else:
        print(f"FAIL  Status Code ({response.status_code})")

    # Canonical
    canonical = soup.find("link", rel="canonical")

    total += 1
    if canonical:
        score += 1
        print("PASS  Canonical Present")
    else:
        print("FAIL  Canonical Missing")

    total += 1
    if canonical:
        actual = canonical.get("href", "").strip()

        if actual == expected_canonical:
            score += 1
            print("PASS  Canonical Match")
        else:
            print("FAIL  Canonical Mismatch")
            print("Expected :", expected_canonical)
            print("Found    :", actual)

    # Title
    title = soup.title.string.strip() if soup.title else ""

    total += 1
    if title:
        score += 1
        print("PASS  Title Present")
    else:
        print("FAIL  Title Missing")

    total += 1
    if 30 <= len(title) <= 60:
        score += 1
        print(f"PASS  Title Length ({len(title)})")
    else:
        print(f"FAIL  Title Length ({len(title)})")

    # Meta Description
    meta = soup.find("meta", attrs={"name": "description"})
    desc = meta.get("content", "").strip() if meta else ""

    total += 1
    if desc:
        score += 1
        print("PASS  Meta Description Present")
    else:
        print("FAIL  Meta Description Missing")

    total += 1
    if 50 <= len(desc) <= 160:
        score += 1
        print(f"PASS  Meta Description Length ({len(desc)})")
    else:
        print(f"FAIL  Meta Description Length ({len(desc)})")

    # H1
    h1s = soup.find_all("h1")

    total += 1
    if len(h1s) > 0:
        score += 1
        print("PASS  H1 Present")
    else:
        print("FAIL  H1 Missing")

    total += 1
    if len(h1s) == 1:
        score += 1
        print("PASS  Single H1")
    else:
        print(f"FAIL  H1 Count ({len(h1s)})")

    # Robots
    robots = soup.find("meta", attrs={"name": "robots"})

    total += 1
    if robots:
        score += 1
        print("PASS  Robots Meta")
    else:
        print("FAIL  Robots Meta")

    # OG
    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")

    total += 1
    if og_title:
        score += 1
        print("PASS  OG Title")
    else:
        print("FAIL  OG Title")

    total += 1
    if og_desc:
        score += 1
        print("PASS  OG Description")
    else:
        print("FAIL  OG Description")

    # Twitter
    tw_title = soup.find("meta", attrs={"name": "twitter:title"})
    tw_desc = soup.find("meta", attrs={"name": "twitter:description"})

    total += 1
    if tw_title:
        score += 1
        print("PASS  Twitter Title")
    else:
        print("FAIL  Twitter Title")

    total += 1
    if tw_desc:
        score += 1
        print("PASS  Twitter Description")
    else:
        print("FAIL  Twitter Description")

    # Schema
    schema = soup.find_all("script", type="application/ld+json")

    total += 1
    if schema:
        score += 1
        print("PASS  Schema Found")
    else:
        print("FAIL  Schema Missing")

    print("\n===========================================")
    print(f"OVERALL SCORE : {score}/{total}")

    if score == total:
        print("SEO STATUS    : PASS")
    else:
        print("SEO STATUS    : REVIEW REQUIRED")

except Exception as e:
    print("ERROR :", e)

print("\nClosing in 15 seconds...")
time.sleep(15)
