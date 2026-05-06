# Mini Office

Inicio rapido para revision local.

## Windows

```bat
INSTALL_AND_RUN.bat
```

## Linux o macOS

```bash
chmod +x install_and_run.sh
./install_and_run.sh
```

## Manual

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python mini_office.py --no-browser
```

En Linux o macOS usa:

```bash
source venv/bin/activate
```

Abre:

```text
http://127.0.0.1:8000
```

## Que Hace

Mini Office presenta una oficina local para revisar materiales, tareas y roles
de agentes antes de empaquetarlos. Las acciones externas requieren aprobacion
humana y no se ejecutan desde esta guia.

## Roles

| Rol | Uso |
| --- | --- |
| Toshiro | Escritura y copy |
| Don Humo | Revision tecnica |
| Mac | Investigacion |
| Ronin | QA |
| Darvi | Archivo |

## Estado Comercial

Este paquete esta en `FOUNDER_ACCESS_REVIEW`. No publicar ni vender sin cerrar
licencia, instalador final, manifest, ZIP firmado y pruebas en maquina limpia.
