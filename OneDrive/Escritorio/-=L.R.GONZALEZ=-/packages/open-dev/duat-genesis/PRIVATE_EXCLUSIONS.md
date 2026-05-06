# Private Exclusions

This package must never include:

- DUAT Geodia private runtime, source, fixtures or bridge code;
- MEDIOEVO RPG/TCG source, scenes, assets, lore, card data or balance data;
- Claudio private runtime, prompts, sessions, logs or credentials;
- books, canon vaults or unreleased editorial content;
- user Downloads raw source files;
- medical, biological or neurological datasets;
- API keys, tokens, `.env` files or local machine paths.

If a future adapter needs private data, keep it in a private repo or private
runtime and expose only a sanitized contract.
