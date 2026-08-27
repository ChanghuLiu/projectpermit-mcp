# Cline / remote MCP install guide

ProjectPermit is already hosted. Do not clone or run a local server unless you are contributing to the codebase.

## Recommended remote connection

Use this Streamable HTTP endpoint:

`https://projectpermit-mcp-production.up.railway.app/mcp`

Current developer-validation preview requires no account, API key, or wallet.

For Cline CLI, open the remote MCP setup wizard with:

```bash
cline mcp install projectpermit --transport http https://projectpermit-mcp-production.up.railway.app/mcp
```

When the wizard asks for authentication, choose no authentication / open connection for the current preview.

## First verification

1. Connect to the remote MCP endpoint.
2. List tools. You should see:
   - `projectpermit_info`
   - `check_project_requirements`
3. Call `projectpermit_info` first. It returns the supported jurisdiction IDs, project families, address-resolution coverage, and a starter example.
4. Then call `check_project_requirements` with normalized project facts.

Starter example:

```json
{
  "jurisdiction": "ottawa_on",
  "project": {
    "family": "window_door",
    "action": "replace_same_size"
  },
  "property": {
    "heritage": false
  },
  "resolve_address": false
}
```

For a multi-case evaluation, optionally set `context.client_tag` to a stable non-PII identifier such as `cline-pilot-acme`. ProjectPermit hashes this value before telemetry is written; do not put a customer name, email, civic address, or other personal information in the tag.

## Scope and safety

ProjectPermit currently covers Gatineau, Ottawa, Toronto, Mississauga, Laval, Longueuil, and Vancouver. Results are evidence-linked municipal permit/planning preflight information. They are not municipal authorization, legal advice, engineering certification, or building-code design approval.

If a project is outside supported rules or official-source evidence is ambiguous, the engine is designed to preserve uncertainty rather than invent a definitive answer.
