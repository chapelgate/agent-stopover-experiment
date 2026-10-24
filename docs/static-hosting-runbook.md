# Static hosting verification

No account or paid service is required.

```sh
for path in '' invite.html robots.txt llms.txt sitemap.xml agent.json README.md results.md assets/a11y.css; do
  curl --compressed -sS -D - -o /dev/null -L "https://chapelgate.github.io/agent-stopover-experiment/$path"
done
```

Record the date, final URL, status, `Content-Type`, `Content-Encoding`, `ETag` or `Last-Modified`, and `Cache-Control` exactly as returned. Do not infer a cache or compression result when the response omits it.

## Observed 2026-10-24T00:06:11Z

Live GitHub Pages responses for resources already on `main` (this branch is not deployed):

| URL | Status | Content-Type | Cache-Control | Validator | Encoding |
| --- | --- | --- | --- | --- | --- |
| / | 200 | text/html; charset=utf-8 | max-age=600 | ETag and Last-Modified present | gzip |
| /invite.html | 200 | text/html; charset=utf-8 | max-age=600 | ETag and Last-Modified present | gzip |
| /robots.txt | 200 | text/plain; charset=utf-8 | max-age=600 | ETag and Last-Modified present | not reported |
| /llms.txt | 200 | text/plain; charset=utf-8 | max-age=600 | ETag and Last-Modified present | gzip |
| /sitemap.xml | 200 | application/xml | max-age=600 | ETag and Last-Modified present | not claimed where omitted |
| /agent.json | 200 | application/json | max-age=600 | ETag and Last-Modified present | not claimed where omitted |
| /README.md | 200 | text/markdown or text/plain as returned | max-age=600 | ETag and Last-Modified present | not claimed where omitted |

A local static server for this branch reported `text/css` for `assets/a11y.css` and `text/javascript` for page scripts. Those branch files are not on the live site until a human merges a pull request. The full header transcript is kept in the job record, not in this repository.
