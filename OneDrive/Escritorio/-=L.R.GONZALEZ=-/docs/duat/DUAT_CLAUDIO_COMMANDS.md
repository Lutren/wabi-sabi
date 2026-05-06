# DUAT Claudio Commands

Estado: `COMMAND_CONTRACT / READ_ONLY`.

## Comandos

### `status`

Uso:

```powershell
python -m claudio.adapters.duat_readonly_adapter status
```

Devuelve el modo local, fuentes disponibles, frontera publico/privada, gate y
comandos disponibles.

### `report`

Uso:

```powershell
python -m claudio.adapters.duat_readonly_adapter report overview
python -m claudio.adapters.duat_readonly_adapter report public
python -m claudio.adapters.duat_readonly_adapter report boundary
```

Scopes:

| scope | uso |
|---|---|
| `overview` | vista local general |
| `public` | solo fuentes de carril publico |
| `internal` | inventario interno redacted, sin contenidos privados |
| `boundary` | estado de frontera y bloqueos |

### `falsify`

Uso:

```powershell
python -m claudio.adapters.duat_readonly_adapter falsify readonly_adapter
python -m claudio.adapters.duat_readonly_adapter falsify duat_public_boundary
```

Claims iniciales:

- `duat_public_boundary`
- `readonly_adapter`
- `duat_claims_low`
- `living_world_fixture_contract`
- `source_registry_hashes`
- `comms_actiongate`

### `source_registry`

Uso:

```powershell
python -m claudio.adapters.duat_readonly_adapter source_registry
```

Devuelve fuentes, privacidad, licencia/politica y hashes. No devuelve contenido
privado ni rutas absolutas.

## Integracion COMMS

Claudio debe tratar cada salida del adapter como evidencia para un
`ObservationEnvelope`. Si falta hash, si el scope es privado, o si el claim no
tiene falsador, el gate queda `REVIEW` o `BLOCK`.

## Acciones bloqueadas

- `write`
- `apply`
- `delete`
- `move`
- `publish`
- fetch de red
- prediccion social real
- exportar material privado

El modulo define `write()` y `apply()` solo para fallar explicitamente con
`ReadOnlyViolation`.
