# Architecture

React/Vite browser UI → cookie-authenticated FastAPI `/api/v1` → SQLite and local Ollama. External server integrations use scoped Bearer keys associated with the key owner's app space. A client key is **not** delegated end-user identity. PWA shell cache excludes API responses. There are no cloud providers, vector store, active tools or MCP server.

SQLite v1 tables are created idempotently; startup upgrade adds v2 columns/tables/indexes without replacing existing data. Formal migration tooling remains outstanding. Chat sends a bounded context of at most 16 history entries, five explicit app memories, three lexical document chunks and an optional project instruction. Document content is untrusted. Browser and backend use SSE streaming. A 503 leaves the user's unsent message out of the database if no model is installed.
