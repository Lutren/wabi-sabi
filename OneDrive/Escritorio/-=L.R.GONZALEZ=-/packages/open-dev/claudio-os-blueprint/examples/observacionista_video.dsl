# Observacionista DSL example for a safe Content Forge render.
intent crear_video_medioevo_local
belief assets_aprobados true
goal render_preview_10s
evidence asset_catalog runtime/content_forge/asset_catalog.json
evidence job_manifest runtime/content_forge/jobs/demo/manifest.json
state observando
state planificando
state renderizando
risk medium local_render
action local_render tags=render,local
approval publish
witness runtime/content_forge/jobs/demo/witness.jsonl
recovery on_hold pedir_assets_o_brief
recovery on_degrade render_preview_baja_resolucion
recovery on_failure conservar_job_logs_y_comando

