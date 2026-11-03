# Election Night Pulse

Election-night dashboard for the 2026 midterms: a map of all 50 states showing each state's latest lean,
a Senate balance strip, a House tab with all 435 districts, and a click-through panel for each state's races (Texas includes statewide and
competitive U.S. House races).

- `connector/`: remote MCP server (Cloudflare Worker) that wraps [civicAPI](https://civicapi.org) for live results. See its README to deploy.
- `data/house.json`: all 435 House districts with incumbent, nominees, partisan lean, ratings and civicAPI `civic_id`. Built from Wikipedia's wikitext by `data/parse_house_wikipedia.py` and `data/build_house.py`.
- `data/races.json`: race list with candidates, final forecaster ratings and each race's civicAPI `civic_id`.
- `data/build_races.py`: script that generated `races.json`.
- `dashboard-page.html`: the dashboard page's source, a copy of what is stored in the Claude artifact.

Results data: civicAPI (civicapi.org). Ratings: Cook Political Report, Inside Elections and Sabato's Crystal Ball, via Wikipedia; Texas House ratings are 270toWin's consensus.

Live results refresh in the page's own code: hourly until 6pm Eastern on election night, then every 15 minutes.
