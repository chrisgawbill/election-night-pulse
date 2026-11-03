// Election results connector: a minimal remote MCP server (Streamable HTTP, stateless)
// that wraps civicAPI (https://civicapi.org, free, no key; attribution requested).
// Deploy as a Cloudflare Worker, then add its URL as a custom connector in claude.ai.

const API = 'https://civicapi.org/api/v2/race/';
const UA = 'Mozilla/5.0 (compatible; ElectionNightPulse/1.0; +https://civicapi.org)';
const MAX_IDS = 45; // Workers Free allows 50 subrequests per invocation
const CACHE_SECONDS = 60; // shields civicAPI when many viewers refresh at once

const TOOL = {
  name: 'election_results',
  description:
    'Live vote counts, percent reporting and winner calls for election races from civicAPI, by race id. ' +
    'Returns one row per candidate: race_id, race_name, state, percent_reporting, last_updated, candidate, party, votes, percent, winner.',
  inputSchema: {
    type: 'object',
    properties: {
      ids: { type: 'string', description: 'Comma-separated civicAPI race ids (at most 45), e.g. "87438,55857"' },
      slot: { type: 'string', description: 'Optional refresh slot label; ignored by the server, lets clients bust caches.' }
    },
    required: ['ids']
  }
};

async function fetchRace(id) {
  // One subrequest per race; Cloudflare's edge cache holds each answer for CACHE_SECONDS.
  const res = await fetch(API + id, {
    headers: { 'User-Agent': UA, Accept: 'application/json' },
    cf: { cacheTtl: CACHE_SECONDS, cacheEverything: true }
  });
  if (!res.ok) return { id, error: `civicAPI ${res.status}`, retry: res.status >= 500 };
  return { id, data: await res.json() };
}

async function results(args, ctx) {
  const ids = String(args.ids || '')
    .split(',').map((s) => s.trim()).filter((s) => /^\d+$/.test(s)).slice(0, MAX_IDS);
  if (!ids.length) throw new Error('No valid race ids given');
  if (String(args.ids).split(',').filter((x) => x.trim()).length > MAX_IDS) throw new Error(`At most ${MAX_IDS} race ids per call`);
  const got = await Promise.all(ids.map((id) => fetchRace(id).catch((e) => ({ id, error: String(e), retry: true }))));
  // Retry server errors once, within the 50-subrequest budget of Workers Free.
  let budget = 49 - ids.length;
  await new Promise((r) => setTimeout(r, 400));
  await Promise.all(got.map(async (g, i) => {
    if (!g.retry || budget <= 0) return;
    budget--;
    got[i] = await fetchRace(g.id).catch((e) => ({ id: g.id, error: String(e) }));
  }));
  const rows = [];
  const errors = [];
  for (const g of got) {
    if (g.error || !g.data || !Array.isArray(g.data.candidates)) { errors.push({ race_id: Number(g.id), error: g.error || 'no data' }); continue; }
    const d = g.data;
    for (const c of d.candidates) {
      rows.push({
        race_id: Number(g.id),
        race_name: d.election_name,
        state: d.province,
        percent_reporting: d.percent_reporting ?? null,
        last_updated: d.last_updated ?? null,
        candidate: c.name,
        party: c.party,
        votes: c.votes ?? 0,
        percent: c.percent ?? null,
        winner: !!c.winner
      });
    }
  }
  return { rows, errors, source: 'civicAPI (civicapi.org)', fetched_at: new Date().toISOString() };
}

function rpc(id, result) { return { jsonrpc: '2.0', id, result }; }
function rpcError(id, code, message) { return { jsonrpc: '2.0', id, error: { code, message } }; }

async function handle(msg, ctx) {
  const { id, method, params } = msg;
  if (method === 'initialize') {
    return rpc(id, {
      protocolVersion: params?.protocolVersion || '2025-03-26',
      capabilities: { tools: {} },
      serverInfo: { name: 'election-results', version: '1.0.0' }
    });
  }
  if (method === 'ping') return rpc(id, {});
  if (method === 'tools/list') return rpc(id, { tools: [TOOL] });
  if (method === 'tools/call') {
    if (params?.name !== TOOL.name) return rpcError(id, -32602, 'Unknown tool');
    try {
      const out = await results(params.arguments || {}, ctx);
      return rpc(id, { content: [{ type: 'text', text: JSON.stringify(out) }], structuredContent: out });
    } catch (e) {
      return rpc(id, { content: [{ type: 'text', text: String(e.message || e) }], isError: true });
    }
  }
  if (id === undefined) return null; // notification
  return rpcError(id, -32601, 'Method not found');
}

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Accept, Mcp-Session-Id, Mcp-Protocol-Version, Authorization'
};

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });
    if (request.method === 'GET') return new Response('Method Not Allowed', { status: 405, headers: CORS });
    if (request.method !== 'POST') return new Response('Not found', { status: 404, headers: CORS });
    let body;
    try { body = await request.json(); } catch { return Response.json(rpcError(null, -32700, 'Parse error'), { status: 400, headers: CORS }); }
    const batch = Array.isArray(body);
    const out = (await Promise.all((batch ? body : [body]).map((m) => handle(m, ctx)))).filter(Boolean);
    if (!out.length) return new Response(null, { status: 202, headers: CORS });
    return Response.json(batch ? out : out[0], { headers: CORS });
  }
};
