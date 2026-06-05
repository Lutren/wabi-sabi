import random, json, os, sys, hashlib
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "obsai-core"))
try:
    from obsai_core.llm_bridge import LLMProvider, NullProvider, build_llm_provider
except ImportError:
    LLMProvider = object

    class NullProvider:  # fallback si obsai-core no está en el path
        """Proveedor nulo: nunca decide nada (action=idle). DEBE ser una CLASE
        (no una instancia) para que `NullProvider()` e `isinstance(x, NullProvider)`
        funcionen igual que el NullProvider real de obsai_core.llm_bridge."""

        def decide(self, ctx, choices):
            return type("D", (), {
                "action": "idle", "confidence": 0.0,
                "reasoning": "", "provider": "null",
            })()

@dataclass
class WorldSeed:
    """Semilla procedural con hash verificable."""
    seed_hash: str
    biomes: List[str]
    complexity: int
    generation: int = 0

@dataclass
class SketchScene:
    """Escena generada por VibeForge para DUAT/TRPG."""
    scene_id: str
    world_hash: str
    entities: List[Dict]
    epistemic_state: str = "OBSERVABLE"

class VibeForge:
    """
    Convierte sketches y texto en objetos, agentes y configuraciones de mundo.
    Pasa por gates OSIT: EML, GhostGate, ActionGate, WitnessMap.
    """
    BIOME_POOL = ["desert", "forest", "coast", "mountain", "cavern", "void"]

    def __init__(self, seed: str = None, llm_provider: Optional["LLMProvider"] = None):
        self.seed = seed or str(random.randint(1, 999999))
        # RNG sembrado de forma estable: dos VibeForge con la misma semilla
        # producen mundos/escenas idénticos (la "semilla procedural verificable").
        self._rng = random.Random(self._stable_int(self.seed))
        self.worlds: Dict[str, WorldSeed] = {}
        self.scenes: Dict[str, SketchScene] = {}
        self.llm_provider = llm_provider or NullProvider()

    @staticmethod
    def _stable_int(s: str) -> int:
        """Entero estable y reproducible derivado de `s`.

        NO usa hash() de Python, que está aleatorizado por proceso (PYTHONHASHSEED):
        hash() haría que seed_hash/scene_id cambiaran entre corridas, rompiendo el
        contrato de 'hash verificable'. sha256 es determinista entre procesos/SO.
        """
        return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[:16], 16)

    def generate_world(self, world_id: str, complexity: int = 3) -> WorldSeed:
        """Genera un mundo procedimental con hash verificable y reproducible."""
        biomes = self._rng.sample(self.BIOME_POOL, complexity)
        world = WorldSeed(
            seed_hash=f"vf_{self._stable_int(world_id + self.seed) % 999999:06d}",
            biomes=biomes,
            complexity=complexity,
        )
        self.worlds[world_id] = world
        return world

    def sketch_to_scene(self, text_prompt: str, world_id: str) -> SketchScene:
        """Convierte texto/sketch en escena materializada para DUAT."""
        if world_id not in self.worlds:
            raise ValueError(f"World {world_id} no generado. Ejecuta generate_world primero.")

        world = self.worlds[world_id]
        entities = []

        if not isinstance(self.llm_provider, NullProvider):
            ctx = {"prompt": text_prompt, "biomes": ",".join(world.biomes), "complexity": world.complexity}
            d = self.llm_provider.decide(ctx, ["generate", "default"])
            try:
                reasoning = d.reasoning or ""
                parsed = json.loads(reasoning) if reasoning[:1] in ("[", "{") else None
                if isinstance(parsed, list):
                    entities = parsed
                elif isinstance(parsed, dict) and "entities" in parsed:
                    entities = parsed["entities"]
            except (json.JSONDecodeError, AttributeError, TypeError):
                pass

        if not entities:
            for word in text_prompt.lower().split():
                if word in ["altar", "ruin", "city", "gate", "temple", "shrine"]:
                    entities.append({
                        "type": "structure",
                        "name": word,
                        "biome": self._rng.choice(world.biomes),
                        "epistemic": self._rng.choice(["CERTEZA", "INFERENCIA", "INCOGNITA"]),
                    })

        scene = SketchScene(
            scene_id=f"scene_{self._stable_int(text_prompt) % 9999:04d}",
            world_hash=world.seed_hash,
            entities=entities,
        )
        self.scenes[scene.scene_id] = scene
        return scene

def run_demo():
    print("=" * 60)
    print("VIBEFORGE ENGINE v1 — Demo")
    print("=" * 60)
    
    vf = VibeForge(seed="demo_3000_ac_egipto")
    
    # Generar mundo
    world = vf.generate_world("egipto_3000", complexity=4)
    print(f"[1/3] World generado: {world.seed_hash}")
    print(f"      Biomes: {', '.join(world.biomes)}")
    
    # Sketch → Escena
    sketch = "Ancient altar temple on the coast of the Nile, ruin gate shrine"
    scene = vf.sketch_to_scene(sketch, "egipto_3000")
    print(f"[2/3] Scene materializada: {scene.scene_id}")
    print(f"      Entidades: {len(scene.entities)}")
    for e in scene.entities:
        print(f"      - {e['type']}: {e['name']} ({e['biome']}) [{e['epistemic']}]")
    
    # Estado epistémico
    print(f"[3/3] Estado epistémico: {scene.epistemic_state}")
    
    # Guardar
    result = {
        "vibeforge_version": "v1",
        "seed": vf.seed,
        "worlds": len(vf.worlds),
        "scenes": len(vf.scenes),
        "timestamp": datetime.now().isoformat(),
    }
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vibeforge_demo.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] VibeForge demo guardado en {out_path}")
    return result

if __name__ == "__main__":
    run_demo()
