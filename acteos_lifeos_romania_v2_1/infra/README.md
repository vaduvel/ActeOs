# Infrastructure baseline

Local development provisions PostgreSQL only. Production reference architecture uses managed PostgreSQL in an EU region, separate object storage for authorized source snapshots, an API deployment, one worker deployment, mobile distribution through EAS and the curator portal through a managed web platform.

Secrets never enter Git. Environments are development, staging and production. Production publication of rules requires a separate role and four-eyes approval.
