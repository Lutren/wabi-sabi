# PRIVATE_GAME_BOUNDARY

Status: active boundary.

## Rule

The game and TCG are private. They must not be published, open-sourced, moved into public package folders, or included in free developer releases.

## Private Paths

Always exclude:

```txt
-=MEDIOEVO=-\-=LIBROS\metaevo-tcg\**
-=MEDIOEVO=-\-=LIBROS\claudio\tcg\**
-=MEDIOEVO=-\-=LIBROS\claudio\runtime\game_bridge\**
PRODUCTOS_MEDIOEVO\04_AUDIOVISUAL_Y_TCG\**
```

Review manually before publishing anything that contains:

```txt
tcg
game
juego
metaevo
cards
deck
minigames
lore
bridge
```

## Packaging Denylist

Any public or free developer package must deny:

- source code from private game paths;
- original game assets;
- card data and game balance files;
- private lore;
- internal builds;
- screenshots or marketing assets not explicitly approved;
- game bridge integrations.

## Commercial Future

The game may become a commercial product later, but it needs a separate release process:

- private repo or private release branch;
- own README_PRIVATE;
- own license/proprietary terms;
- own QA checklist;
- own product manifest;
- no cross-contamination with open-source tooling.

## DUAT Private Bridge

DUAT Geodia may inform the game only through a private bridge. It must not be
open-sourced or copied into public DUAT Genesis.

Allowed privately:

- world pulse events;
- NPC memory/schedule/intent;
- rumors, quests, faction tension and economy signals;
- private validation fixtures.

Blocked publicly:

- DUAT Geodia source, fixtures or bridges;
- RPG scripts, scenes, assets, lore, card data and balance;
- `LivingWorldEvent` records containing private evidence URIs or local paths.
