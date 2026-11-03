# Election results connector (connector/)

A small remote MCP server that wraps [civicAPI](https://civicapi.org): free, needs no key, and asks for attribution.
It has one tool, `election_results(ids, slot?)`, which returns live votes, percent reporting
and winner calls for the civicAPI race IDs you give it. Election Night Pulse calls it straight from
the page, so refreshes don't use any Claude tokens.

## Deploy (free Cloudflare Workers, about 5 minutes)

**Option A: dashboard, no installs**
1. Sign in at dash.cloudflare.com, then go to **Workers & Pages → Create → Create Worker**.
2. Name it `election-results-mcp` and click **Deploy**, then **Edit code**.
3. Replace the code with `worker.js` and click **Deploy**.
4. Copy the URL, for example `https://election-results-mcp.<you>.workers.dev`.

**Option B: CLI**
```
npx wrangler login
npx wrangler deploy      # run in this folder
```

## Add it to Claude
In claude.ai, go to **Settings → Connectors → Add custom connector**:
- Name: `Election Results`
- URL: the Worker URL from above
- Auth: none

## Notes
- Responses are cached for 60 seconds at the edge, so many viewers make few calls to civicAPI.
- Up to 45 race ids per call: Workers Free allows 50 outbound requests per invocation.
- civicAPI blocks requests that don't send a browser-style User-Agent, so the Worker sends one.
- Each viewer of the dashboard needs this connector added to their own account,
  or the owner can share their connection from the dashboard's Sources panel.
