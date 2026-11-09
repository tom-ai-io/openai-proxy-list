# OpenAI + Muse AI Proxy List

A small AutoProxy/GFWList-compatible subscription covering the AI services that are
geo-gated away from Hong Kong: first-party OpenAI/ChatGPT domains and Meta's Muse.

## Subscription URL

```text
https://raw.githubusercontent.com/tom-ai-io/openai-proxy-list/main/openai-gfwlist.txt
```

CDN fallback:

```text
https://fastly.jsdelivr.net/gh/tom-ai-io/openai-proxy-list@main/openai-gfwlist.txt
```

Use AutoProxy/GFWList format, Base64 encoding, and send matching traffic through
your proxy profile. Keep the default rule as Direct.

## What it includes

OpenAI / ChatGPT:

- `chatgpt.com`
- `oaistatic.com`
- `oaistatsig.com`
- `oaiusercontent.com`
- `openai.com`
- `openaimerge.com`

Muse (Meta's personal agent, <https://muse.ai>):

- `muse.ai`
- `meta.ai`
- `metaaiusercontent.com`
- `metaaivm.com`
- `ecto1usercontent.com`
- `auth.meta.com`

The Muse host set comes from muse.ai's own CSP header and SagerNet's AI category
(checked 2026-11-09). `facebook.com` and `instagram.com` are intentionally excluded:
they work from Hong Kong and would proxy unrelated traffic.

The generator also extracts matching rules from the upstream
[GFWList](https://github.com/gfwlist/gfwlist) and writes both a readable and
Base64 subscription file.

Third-party services listed in OpenAI's network guidance, such as WorkOS,
Intercom, Stripe, Sentry, Datadog, SendGrid, and Cloudflare, are intentionally
excluded so this subscription does not proxy unrelated traffic.

## Daily update

GitHub Actions runs the generator every day at `02:17 UTC` (`10:17`
Asia/Hong_Kong) and commits only when the generated files change. The workflow
can also be run manually from the Actions tab.
