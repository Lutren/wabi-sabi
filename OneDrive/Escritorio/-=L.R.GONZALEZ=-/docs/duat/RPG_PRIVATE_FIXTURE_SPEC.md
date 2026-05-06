# RPG Private Fixture Spec

Estado: `PRIVATE_FIXTURE_SPEC_ONLY / NO_PRIVATE_LORE`.

No se encontro una ruta privada explicitamente autorizada dentro de esta tarea
para escribir un fixture real del RPG. Por eso se deja solo especificacion
public-safe y una fixture sintetica generica en:

`fixtures/duat/public_synthetic_fixture.json`

Esa fixture no contiene lore, assets, nombres reales, rutas del juego, escenas,
prompts ni runtime privado. Sirve para validar contrato.

## Contrato minimo

Salida esperada: `LivingWorldEvents`.

### 10 NPCs sinteticos

1. `npc_01`: observer
2. `npc_02`: trader
3. `npc_03`: messenger
4. `npc_04`: guard
5. `npc_05`: artisan
6. `npc_06`: healer
7. `npc_07`: scribe
8. `npc_08`: farmer
9. `npc_09`: scout
10. `npc_10`: elder

### 3 zonas sinteticas

1. `zone_01`: market
2. `zone_02`: gate
3. `zone_03`: workshop

### 20 eventos sinteticos

Los eventos `evt_001` a `evt_020` estan definidos en la fixture publica como
eventos genericos de observacion, comercio, mensaje, inspeccion, reparacion y
revision. Todos declaran:

- `npc_id`
- `zone_id`
- `signal`
- `residue`
- `phi_eff`
- `output: LivingWorldEvents`

## Siguiente paso privado

Crear la fixture real solo en una ruta privada aprobada por ActionGate. Antes de
usar material del RPG real:

1. registrar hash de fuente;
2. bloquear publicacion;
3. validar que no cruza `packages/open-dev`;
4. correr secret scan;
5. ejecutar falsador `living_world_fixture_contract`.
