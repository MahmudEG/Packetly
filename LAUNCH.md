# Launch checklist

Everything on the site is built and deployed. These are the steps that are outside
the repository — ordered so that each one unblocks the next.

Facts you will need:

| | |
| --- | --- |
| Site | `https://packetly.ly` |
| Sitemap | `https://packetly.ly/sitemap.xml` (59 URLs) |
| Repo | `MahmudEG/Packetly`, Pages from `main` → `/docs` |
| DNS host | Libyan Spider (`ns1`–`ns5.ns.ly`) |
| Analytics | GA4 `G-QG6N52FTQC` |
| AdSense | `ca-pub-4081538671702116` |

---

## 1. Google Search Console

Nothing is indexed until this is done. Everything else in this file is downstream of it.

Use a **URL-prefix property**, not a Domain property. A Domain property can only be
verified with a DNS TXT record, and the Libyan Spider panel already silently dropped
the A records once. URL-prefix verification is a meta tag that deploys with the site,
so the registrar is not involved. `www.packetly.ly` does not exist, so a URL-prefix
property on `https://packetly.ly/` covers the whole site.

1. https://search.google.com/search-console → **Add property** → **URL prefix** →
   `https://packetly.ly/`
2. Choose **HTML tag**. Copy only the `content="..."` value, not the whole tag.
3. Paste it into `build.py`:
   ```python
   GOOGLE_VERIFY = 'paste-the-token-here'
   ```
4. `python build.py && python check_content.py && git add -A && git commit -m "Add Search Console verification" && git push`
5. Wait for the Pages build (~1 min), then click **Verify**.
6. **Sitemaps** → submit `sitemap.xml`.
7. **URL Inspection** → enter `https://packetly.ly/` → **Request indexing**.
   Do the same for two or three sheets you care most about. The quota is small;
   don't try to submit all 59.

Expect nothing for days, then partial coverage. "Discovered – currently not indexed"
is normal for a new domain and does not mean something is broken.

## 2. Bing Webmaster Tools

Worth doing on its own, and Bing's index is what ChatGPT search reads — so this is
the main lever for being cited by AI assistants, not just ranking in Bing.

1. https://www.bing.com/webmasters → **Import from Google Search Console** (carries
   the verification across, no second token needed).
2. If importing fails, verify with the meta tag instead and set `BING_VERIFY` in
   `build.py` the same way as above.
3. Submit `https://packetly.ly/sitemap.xml`.
4. Use **IndexNow** from the dashboard to push new URLs when you add sheets.

## 3. AdSense

1. **AdSense → Sites** → confirm `packetly.ly` shows *Ready* / ads.txt authorised.
   The file is live at `/ads.txt`; Google re-crawls it on its own schedule, so a
   warning for up to a day is expected.
2. Wait for site approval. The loader is on every page but serves nothing until then.
3. Once approved, either turn on **Auto ads**, or ask for manual units to be placed
   in `build.py` (the natural slot is between the cheat table and the walkthrough).
4. **Privacy & messaging → GDPR** — turn on Google's certified CMP if you want
   personalised ads for EEA/UK visitors. If you do, delete `docs/consent.js` and its
   `<script>` tag in `build.py`, or visitors will see two banners.

## 4. Analytics sanity check

1. Open the site in a normal browser, accept the cookie banner.
2. **GA4 → Reports → Realtime** — you should appear within seconds.
   If not, the cause is almost always an ad blocker, not the tag.
3. **Admin → Data streams → Enhanced measurement** — confirm it is on. The site
   navigates client-side, so page views between sheets depend on history-change
   tracking, which Enhanced measurement provides.

## 5. The domain question

`.ly` is Libya's ccTLD and is **not** on
[Google's generic ccTLD list](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites),
so Google reads it as geo-targeted to Libya. Search Console's International Targeting
override was retired in 2022, and `hreflang` does not apply to a single-locale site.

If US/UK/CA traffic is the goal, register `packetly.com` and 301 the `.ly` onto it.
Doing that now, with almost no backlinks, costs nothing. In a year it means throwing
away accumulated authority. The `.ly` still works as a short link.

## 6. After indexing — what actually moves the number

Technical SEO removes obstacles; it does not create demand.

- **Target long-tail intent.** Nobody outranks Cisco for `show ip route`. But
  "how to read show interfaces counters errors output" is winnable, and the
  interpretation paragraphs are already better than most of what ranks.
- **Be where the readers are** — r/networking, r/sysadmin, r/ITCareerQuestions.
  These are also heavily cited by AI answer engines, so it serves SEO and GEO at once.
- **Fix the thin pages.** `contact` is under 600 characters and offers no actual
  contact route; `about` has no named author. For a site giving advice people run in
  production, a real author with credentials helps both E-E-A-T and AdSense review.

---

## Adding a sheet later

```bash
# edit guides.py, then:
python build.py && python check_content.py
git add -A && git commit -m "Add <name> cheat sheet" && git push
```

`check_content.py` asserts the sheet count, so it will fail until you bump the
number in it — that is deliberate. A new category also needs an entry in `INTRO`
in `build.py` and in `TOPICS` in `check_content.py`.
