from base64 import b64decode, b64encode
from pathlib import Path
import re
import textwrap
from urllib.request import Request, urlopen


SOURCE_URL = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
OUTPUT_PATH = Path("openai-gfwlist.txt")
READABLE_PATH = Path("openai-rules.txt")

CORE_RULES = {
    "||chatgpt.com",
    "||oaistatic.com",
    "||oaistatsig.com",
    "||oaiusercontent.com",
    "||openai.com",
    "||openaimerge.com",
}

# Muse (Meta's personal agent, https://muse.ai) is geo-gated to the US. Keeping it
# in the same subscription means one rule set covers every AI service that has to
# leave Hong Kong. Domains come from muse.ai's own CSP (2026-11-09) plus the ones
# SagerNet's AI category lists. facebook.com / instagram.com are deliberately NOT
# included: they work from Hong Kong and would proxy unrelated traffic.
MUSE_RULES = {
    "||muse.ai",
    "||meta.ai",
    "||metaaiusercontent.com",
    "||metaaivm.com",
    "||ecto1usercontent.com",
    "||auth.meta.com",
}

HOST_RE = re.compile(
    r"(?i)(?<![a-z0-9-])(?:[a-z0-9-]+\.)*"
    r"(?:openai\.com|chatgpt\.com|oaistatic\.com|oaistatsig\.com|"
    r"oaiusercontent\.com|openaimerge\.com|muse\.ai|meta\.ai|"
    r"metaaiusercontent\.com|metaaivm\.com|ecto1usercontent\.com|"
    r"auth\.meta\.com)(?=$|[/^:*?|])"
)


def fetch_source() -> str:
    request = Request(SOURCE_URL, headers={"User-Agent": "openai-gfwlist-builder/1.0"})

    with urlopen(request, timeout=30) as response:
        encoded = response.read()

    decoded = b64decode(b"".join(encoded.split())).decode("utf-8")
    if "[AutoProxy 0.2.9]" not in decoded:
        raise RuntimeError("upstream file is not an AutoProxy list")
    return decoded


def main() -> None:
    source = fetch_source()
    rules = {
        line.strip()
        for line in source.splitlines()
        if line.strip()
        and not line.lstrip().startswith(("!", "@@"))
        and HOST_RE.search(line)
    }
    rules.update(CORE_RULES)
    rules.update(MUSE_RULES)
    if not rules:
        raise RuntimeError("no OpenAI or Muse rules were found")

    decoded = "\n".join(
        [
            "[AutoProxy 0.2.9]",
            "! Title: OpenAI, ChatGPT and Muse AI",
            f"! Source: {SOURCE_URL}",
            *sorted(rules),
            "",
        ]
    )
    encoded = b64encode(decoded.encode("utf-8")).decode("ascii")

    with OUTPUT_PATH.open("w", encoding="ascii", newline="\n") as output:
        output.write(textwrap.fill(encoded, 76) + "\n")
    with READABLE_PATH.open("w", encoding="utf-8", newline="\n") as readable:
        readable.write(decoded)

    print(f"wrote {len(rules)} rules")


if __name__ == "__main__":
    main()
