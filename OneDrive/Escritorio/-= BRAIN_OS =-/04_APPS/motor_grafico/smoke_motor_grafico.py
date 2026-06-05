"""Local smoke test for motor_grafico.

Verifies that VibeForge can create a world and materialize a scene without
writing files, calling providers, building bundles, or publishing artifacts.
"""

from __future__ import annotations

import json

from vibeforge_engine import VibeForge


def main() -> int:
    engine = VibeForge(seed="motor_grafico_smoke")
    world = engine.generate_world("smoke_world", complexity=3)
    scene = engine.sketch_to_scene("altar gate temple shrine", "smoke_world")

    assert world.seed_hash.startswith("vf_")
    assert world.complexity == 3
    assert len(world.biomes) == 3
    assert scene.world_hash == world.seed_hash
    assert len(scene.entities) >= 3

    print(
        json.dumps(
            {
                "ok": True,
                "schema": "motor_grafico.smoke.v0_1",
                "world": world.seed_hash,
                "entities": len(scene.entities),
                "provider_called": False,
                "files_written": False,
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
