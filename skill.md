# Qdrant Skills

Agent skills encoding deep Qdrant knowledge for coding agents.

## Start with search

For specific tasks, symptoms, or troubleshooting questions, start with the [skills search](https://skills.qdrant.tech/search?query=your+query+here).

Use hierarchical navigation when exploring an area broadly.
## Qdrant Advisor

- [qdrant-advisor](https://skills.qdrant.tech/meta/qdrant-advisor/SKILL.md) — Meta-skill that loads the relevant Qdrant skill live at trigger time, so you install one skill instead of the full set and always get current guidance. Ships no static content of its own.

## Available Skills

- [qdrant-clients-sdk](https://skills.qdrant.tech/qdrant-clients-sdk/SKILL.md) — Client SDKs for Python, TypeScript, Rust, Go, .NET, and Java.
- [qdrant-deployment-options](https://skills.qdrant.tech/qdrant-deployment-options/SKILL.md) — Choosing between local, Docker, self-hosted, Cloud, and embedded deployments.
- [qdrant-edge](https://skills.qdrant.tech/qdrant-edge/SKILL.md) — Building on the embedded in-process shard: server sync, on-device BM25, snapshots, and what to reuse versus implement.
- [qdrant-hybrid-cloud-setup](https://skills.qdrant.tech/qdrant-hybrid-cloud-setup/SKILL.md) — Setting up a Hybrid Cloud environment: cluster prerequisites, storage/CSI, agent connectivity, exposure, and common pitfalls.
- [qdrant-managed-cloud-quickstart](https://skills.qdrant.tech/qdrant-managed-cloud-quickstart/SKILL.md) — Getting a first Managed Cloud cluster running and connected: free vs standard, API keys, strict mode, Cloud Inference, and choices you can't undo.
- [qdrant-migration-tool](https://skills.qdrant.tech/qdrant-migration-tool/SKILL.md) — Using the Qdrant Migration Tool CLI to move data from another vector database into Qdrant.
- [qdrant-model-migration](https://skills.qdrant.tech/qdrant-model-migration/SKILL.md) — Switching embedding models without downtime.
- [qdrant-monitoring](https://skills.qdrant.tech/qdrant-monitoring/SKILL.md) — Monitoring, observability, health checks, and debugging production issues.
  - [qdrant-monitoring-setup](https://skills.qdrant.tech/qdrant-monitoring/setup/SKILL.md) — Setting up Prometheus, health probes, alerting, and log centralization.
  - [qdrant-monitoring-debugging](https://skills.qdrant.tech/qdrant-monitoring/debugging/SKILL.md) — Diagnosing production issues from metrics and observability data.
- [qdrant-multitenancy](https://skills.qdrant.tech/qdrant-multitenancy/SKILL.md) — Isolating multiple tenants within a Qdrant deployment: payload partitioning, tiered multitenancy, and region-based data isolation.
- [qdrant-performance-optimization](https://skills.qdrant.tech/qdrant-performance-optimization/SKILL.md) — Search speed, memory usage, and indexing performance tuning.
  - [qdrant-search-speed-optimization](https://skills.qdrant.tech/qdrant-performance-optimization/search-speed-optimization/SKILL.md) — Diagnosing and fixing slow search and high query latency.
  - [qdrant-memory-usage-optimization](https://skills.qdrant.tech/qdrant-performance-optimization/memory-usage-optimization/SKILL.md) — Diagnosing and reducing RAM usage and out-of-memory crashes.
  - [qdrant-indexing-performance-optimization](https://skills.qdrant.tech/qdrant-performance-optimization/indexing-performance-optimization/SKILL.md) — Diagnosing and fixing slow ingestion and indexing.
- [qdrant-scaling](https://skills.qdrant.tech/qdrant-scaling/SKILL.md) — Scaling decisions: data volume, QPS, latency, horizontal vs vertical.
  - [qdrant-scaling-data-volume](https://skills.qdrant.tech/qdrant-scaling/scaling-data-volume/SKILL.md) — Scaling when data no longer fits or needs more storage.
  - [qdrant-scaling-qps](https://skills.qdrant.tech/qdrant-scaling/scaling-qps/SKILL.md) — Increasing query throughput (QPS).
  - [qdrant-scaling-query-volume](https://skills.qdrant.tech/qdrant-scaling/scaling-query-volume/SKILL.md) — Handling large result sets and scroll-heavy workloads.
  - [qdrant-minimize-latency](https://skills.qdrant.tech/qdrant-scaling/minimize-latency/SKILL.md) — Reducing per-query latency and tail (p99) latency.
- [qdrant-search-quality](https://skills.qdrant.tech/qdrant-search-quality/SKILL.md) — Diagnosing bad results, search strategies, hybrid search, and reranking.
  - [qdrant-search-quality-diagnosis](https://skills.qdrant.tech/qdrant-search-quality/diagnosis/SKILL.md) — Diagnosing irrelevant, wrong, or missing results.
  - [qdrant-search-strategies](https://skills.qdrant.tech/qdrant-search-quality/search-strategies/SKILL.md) — Choosing strategies: hybrid search, reranking, relevance feedback.
- [qdrant-sizing](https://skills.qdrant.tech/qdrant-sizing/SKILL.md) — Sizing RAM, disk, CPU, and node count before a deployment is provisioned.
- [qdrant-version-upgrade](https://skills.qdrant.tech/qdrant-version-upgrade/SKILL.md) — Safe upgrade paths, compatibility guarantees, and rolling upgrades.

## Navigating this skill tree

Skills structure is hierarchical. Each `SKILL.md` links to its sub-skills, and those links are the navigation mechanism; follow them rather than assembling paths yourself.

- Read the `SKILL.md` for the relevant skill, then follow its links to go deeper. This page lists the top two levels; skills nest up to four levels, and the deeper ones are reachable only through the links inside each `SKILL.md`.
- If you do not have a link to the skill you need, do not guess the path. Fetch the [complete index of every skill](https://skills.qdrant.tech/llms.txt), including the ones this page does not list, or search: https://skills.qdrant.tech/search?query=your+query+here
- When fetching `SKILL.md` files via a URL tool, preserve all Markdown links exactly as written. Do not paraphrase, summarize away, or omit URLs.
- Search returns a full skill with its links intact, so a hit can be acted on directly.
