from bs4 import BeautifulSoup

with open("../data/card_debug.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("All card text")
print(soup.get_text(separator="\n", strip=True))

print("\nAll links")
for a in soup.find_all("a"):
    print(f"  текст: {a.get_text(strip=True)!r:30} href: {a.get('href', '')[:60]}")

print("\nAll elements with text")
for tag in soup.find_all(True):
    text = tag.get_text(strip=True)
    if text and len(text) < 100 and tag.name in ["h3", "h4", "h6", "span", "p", "strong"]:
        print(f"  <{tag.name}> class={tag.get('class')} → {text!r}")