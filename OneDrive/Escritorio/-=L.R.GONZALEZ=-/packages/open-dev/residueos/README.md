# ResidueOS

ResidueOS is a local AI action gate. It evaluates proposed actions before they
execute and returns one stable status:

```txt
APPROVE
REVIEW
BLOCK
```

This MVP is a selective absorption from `residueos_mvp.zip`, registered in
`SOURCE_INTAKE_REGISTER.md`. It is not a wholesale copy of the ZIP. The original
JSON store is replaced with SQLite.

## Claims Boundary

- This is not a consciousness detector.
- Thresholds and weights are `DEMO_ONLY` until calibrated with a real dataset.
- Confusion matrices from synthetic examples are `DEMO_ONLY`.
- Human review is an audit workflow, not a guarantee of safety.

## Run

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\packages\open-dev\residueos"
python -m residueos.cli evaluate examples\sample_action.json --db runtime\residueos.sqlite
python -m residueos.cli actions --db runtime\residueos.sqlite
python -m residueos.cli serve --db runtime\residueos.sqlite --port 8787
```

Then open:

```txt
http://127.0.0.1:8787/api/health
```

## API

| method | path | purpose |
|---|---|---|
| GET | `/api/health` | health check |
| POST | `/api/evaluate` | evaluate and store an action |
| GET | `/api/actions` | list stored action records |
| GET | `/api/actions/<id>` | fetch one action record |
| POST | `/api/actions/<id>/approve` | attach human approval audit |
| POST | `/api/actions/<id>/block` | attach human block audit |
| GET | `/api/dashboard` | aggregate action stats |

## Test

```powershell
python -m unittest discover -s tests
```

## Stored Record

Each SQLite record stores:

- action JSON;
- decision JSON;
- optional human decision JSON;
- audit events for evaluation and human review;
- timestamps for creation and update.
