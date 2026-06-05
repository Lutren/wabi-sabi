// VIBE FORGE — frontend de la forja de mundos/escenas. Fiel a vibeforge_engine.py (vocabulario y reglas).
// Reimplementa la forja en JS (determinista, offline) y RENDERIZA con el MOTOR compartido (mv-boot → MV.createEngine).
// Propósito: convertir semilla + texto/sketch en mundo procedural + escena materializada, BAJO gates OSIT.
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);

  // ── Forja determinista (espejo de vibeforge_engine.py) ──────────────────────
  const BIOME_POOL = ["desert", "forest", "coast", "mountain", "cavern", "void"];
  const KEYWORDS = ["altar", "ruin", "city", "gate", "temple", "shrine"];
  // sinónimos es→en para el comando en lenguaje natural (sketch_to_scene busca las inglesas)
  const SYN = { altar: "altar", ruina: "ruin", ruin: "ruin", ciudad: "city", city: "city", puerta: "gate", gate: "gate", templo: "temple", temple: "temple", santuario: "shrine", shrine: "shrine" };
  const BIOME_ES = { desert: "Desierto", forest: "Bosque", coast: "Costa", mountain: "Montaña", cavern: "Caverna", void: "Vacío" };
  function stableInt(s) { let h = 2166136261 >>> 0; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const pad = (n, w) => String(n).padStart(w, "0");

  class VibeForge {
    constructor(seed) { this.seed = seed || String(Math.floor(Math.random() * 999999)); this.rng = mulberry32(stableInt(this.seed)); this.worlds = {}; this.scenes = {}; }
    generateWorld(worldId, complexity) {
      const pool = [...BIOME_POOL], biomes = [];
      for (let i = 0; i < complexity && pool.length; i++) biomes.push(pool.splice(Math.floor(this.rng() * pool.length), 1)[0]);
      const w = { seed_hash: "vf_" + pad(stableInt(worldId + this.seed) % 999999, 6), biomes, complexity, generation: 0, id: worldId };
      this.worlds[worldId] = w; return w;
    }
    sketchToScene(prompt, worldId) {
      const world = this.worlds[worldId]; if (!world) throw new Error("World " + worldId + " no generado.");
      const entities = [];
      for (const word of prompt.toLowerCase().split(/\s+/))
        if (KEYWORDS.includes(word)) entities.push({ type: "structure", name: word,
          biome: world.biomes[Math.floor(this.rng() * world.biomes.length)],
          epistemic: ["CERTEZA", "INFERENCIA", "INCOGNITA"][Math.floor(this.rng() * 3)] });
      const scene = { scene_id: "scene_" + pad(stableInt(prompt) % 9999, 4), world_hash: world.seed_hash, entities, epistemic_state: "OBSERVABLE" };
      this.scenes[scene.scene_id] = scene; return scene;
    }
  }

  // ── Gates OSIT (contrato de motor_grafico/README) ───────────────────────────
  const GATES = [
    { id: "publication", nombre: "PublicationGate", estado: "BLOCK", color: "#ff4444", nota: "no publica nada sin gate explícito" },
    { id: "build", nombre: "BuildGate", estado: "REVIEW_REQUIRED", color: "#ffd166", nota: "construir bundle requiere revisión" },
    { id: "release", nombre: "ReleaseGate", estado: "BLOCK", color: "#ff4444", nota: "no libera artefactos" },
    { id: "runtime", nombre: "RuntimeRunGate", estado: "REVIEW_LOCAL_RUN", color: "#ffd166", nota: "ejecutar motor = revisión local" },
  ];
  const EPI_COLOR = { CERTEZA: "#24e8ff", INFERENCIA: "#7fe3b0", INCOGNITA: "#ffd166", OBSERVABLE: "#c79bff" };

  // ── Estado de la app ────────────────────────────────────────────────────────
  const cv = $("vf-canvas"); const ctx = cv.getContext("2d", { alpha: false });
  let vf = new VibeForge($("seed").value || undefined);
  let world = null, scene = null, engine = null, running = false, rafId = 0, tick = 0;

  function log(tag, msg, color) {
    const el = $("vf-log"); if (!el) return;
    const d = document.createElement("div"); d.className = "vf-logline";
    d.innerHTML = `<span class="lg" style="color:${color || "#7fe3b0"}">${tag}</span> ${msg}`;
    el.appendChild(d); while (el.children.length > 50) el.removeChild(el.firstChild); el.scrollTop = el.scrollHeight;
  }

  // ── Motor: conexión automática (mv-boot) ────────────────────────────────────
  const BOOT = "../../-=LR WORKING BENCH=-/DUAT_UNIFIED/engine_web/mv-boot.js";
  function connectMotor() {
    return new Promise((resolve) => {
      if (window.MV && window.MV.__boot) return resolve(true);
      const s = document.createElement("script"); s.src = encodeURI(BOOT); s.async = true;
      s.onload = () => resolve(!!(window.MV && window.MV.__boot)); s.onerror = () => resolve(false);
      document.head.appendChild(s);
    }).then((ok) => ok ? window.MV.connect({ groups: ["core"] }) : null).then((MV) => {
      const chip = $("motor-status");
      if (MV) { window.MOTOR = MV; chip.textContent = "Motor: conectado · " + MV.loaded.length + " módulos"; chip.className = "chip ok";
        log("MOTOR", "Conectado (" + MV.loaded.length + " módulos). Render por MV.createEngine.", "#24e8ff"); }
      else { chip.textContent = "Motor: no disponible (render local)"; chip.className = "chip warn";
        log("MOTOR", "No disponible — render de respaldo local.", "#ffd166"); }
      return MV;
    });
  }

  // ── Construye el estado DUAT desde la escena (entidades → edificios) ────────
  function buildState() {
    const W = 12 + (world ? world.complexity : 3) * 2, H = 10 + (world ? world.complexity : 3);
    const buildings = [], ents = scene ? scene.entities : [];
    ents.forEach((e, i) => {
      const x = 3 + (i % 4) * 4, y = 3 + Math.floor(i / 4) * 4;
      const phi = e.epistemic === "CERTEZA" ? 0.82 : e.epistemic === "INFERENCIA" ? 0.5 : 0.25;
      buildings.push({ id: "e" + i, x, y, type: e.name, level: 1 + (i % 3), Phi_eff: phi, gate: e.epistemic === "INCOGNITA" ? "REVIEW" : "PASS" });
    });
    const agents = []; for (let i = 0; i < 8; i++) agents.push({ id: "a" + i, x: 2 + Math.random() * (W - 4), y: 2 + Math.random() * (H - 4), gate: "PASS" });
    const R = scene ? (0.15 + 0.1 * scene.entities.filter(e => e.epistemic === "INCOGNITA").length) : 0.3;
    return { tick: tick, width: W, height: H, R: Math.min(0.9, R), Phi_eff: 0.6, regime: "FUNCIONAL", gate: "REVIEW", physicsR: 0.1, tiles: [], buildings, agents, tasks: [] };
  }

  // ── Render: motor si está; respaldo isométrico si no ────────────────────────
  function fallbackPaint(state) {
    ctx.fillStyle = "#0a0f14"; ctx.fillRect(0, 0, cv.width, cv.height);
    const TW = 40, TH = 20, ox = cv.width / 2, oy = 60;
    const col = { desert: "#7a6a3a", forest: "#2a4a2a", coast: "#2a4a5a", mountain: "#4a4a55", cavern: "#3a2a4a", void: "#1a1024" };
    for (let gx = 0; gx < state.width; gx++) for (let gy = 0; gy < state.height; gy++) {
      const sx = (gx - gy) * TW / 2 + ox, sy = (gx + gy) * TH / 2 + oy;
      const biome = world ? world.biomes[(gx + gy) % world.biomes.length] : "void";
      ctx.fillStyle = ((gx + gy) & 1) ? col[biome] : col[biome] + "cc";
      ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx + TW / 2, sy + TH / 2); ctx.lineTo(sx, sy + TH); ctx.lineTo(sx - TW / 2, sy + TH / 2); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = "#0c1014"; ctx.stroke();
    }
    for (const b of state.buildings) {
      const sx = (b.x - b.y) * TW / 2 + ox, sy = (b.x + b.y) * TH / 2 + oy;
      ctx.fillStyle = b.gate === "REVIEW" ? "#ffd166" : "#24e8ff";
      ctx.fillRect(sx - 8, sy - 18, 16, 22); ctx.strokeStyle = "#0a0f14"; ctx.strokeRect(sx - 8, sy - 18, 16, 22);
    }
  }
  function frame() {
    if (!running) return;
    tick++;
    const state = buildState(); state.tick = tick;
    try { if (engine) engine.frame(state, ctx); else fallbackPaint(state); }
    catch (e) { fallbackPaint(state); }
    rafId = requestAnimationFrame(frame);
  }
  function startRender() {
    if (window.MOTOR && window.MOTOR.createEngine && !engine) {
      try { engine = window.MOTOR.createEngine({ mode: "CITY", width: 24, height: 18, gi: false, contagion: true }); }
      catch (e) { engine = null; }
    }
    if (!running) { running = true; rafId = requestAnimationFrame(frame); }
  }

  // ── Render de paneles ───────────────────────────────────────────────────────
  function renderWorld() {
    const el = $("world-info"); if (!world) { el.innerHTML = '<span class="muted">Sin mundo. Genera uno.</span>'; return; }
    el.innerHTML = `<div class="kv"><span>seed_hash</span><b>${world.seed_hash}</b></div>
      <div class="kv"><span>complejidad</span><b>${world.complexity}</b></div>
      <div class="kv"><span>generación</span><b>${world.generation}</b></div>
      <div class="biomes">${world.biomes.map(b => `<span class="biome">${BIOME_ES[b] || b}</span>`).join("")}</div>`;
  }
  function renderScene() {
    const el = $("scene-info"); if (!scene) { el.innerHTML = '<span class="muted">Sin escena. Materializa un sketch.</span>'; return; }
    el.innerHTML = `<div class="kv"><span>scene_id</span><b>${scene.scene_id}</b></div>
      <div class="kv"><span>world_hash</span><b>${scene.world_hash}</b></div>
      <div class="kv"><span>estado</span><b style="color:${EPI_COLOR.OBSERVABLE}">${scene.epistemic_state}</b></div>
      <div class="entities">${scene.entities.length ? scene.entities.map(e =>
        `<div class="entity"><span class="en">${e.name}</span><span class="eb">${BIOME_ES[e.biome] || e.biome}</span>
         <span class="ep" style="color:${EPI_COLOR[e.epistemic]}">${e.epistemic}</span></div>`).join("")
        : '<span class="muted">0 entidades (usa palabras: altar, ruin, city, gate, temple, shrine)</span>'}</div>`;
  }
  function renderGates() {
    $("gate-console").innerHTML = GATES.map(g =>
      `<div class="gate-row"><span class="gn">${g.nombre}</span>
       <span class="gs" style="color:${g.color};border-color:${g.color}">${g.estado}</span>
       <span class="gnote">${g.nota}</span></div>`).join("");
  }

  // ── Acciones ─────────────────────────────────────────────────────────────────
  let worldCounter = 0;
  function genWorld() {
    const seed = $("seed").value.trim(); if (seed !== vf.seed) vf = new VibeForge(seed || undefined);
    const cx = parseInt($("complexity").value, 10);
    const wid = "w" + (++worldCounter);
    world = vf.generateWorld(wid, cx); scene = null;
    log("WORLD", `Mundo ${world.seed_hash} · ${world.biomes.map(b => BIOME_ES[b]).join(", ")}`, "#24e8ff");
    renderWorld(); renderScene(); startRender();
  }
  function materialize() {
    if (!world) { log("ERROR", "Genera un mundo primero.", "#ff4444"); return; }
    const prompt = $("sketch").value.trim() || "altar ruin temple gate";
    scene = vf.sketchToScene(prompt, world.id);
    log("SCENE", `Escena ${scene.scene_id} · ${scene.entities.length} entidades`, "#7fe3b0");
    engine = null;  // re-crear con el nuevo tamaño
    renderScene(); startRender();
  }

  // ── Comando en LENGUAJE NATURAL (sin LLM): lo mismo que los botones, hablando ──
  function parseCmd(raw) {
    const t = (raw || "").toLowerCase().trim(); if (!t) return; let did = "";
    const mSeed = t.match(/(?:semilla|seed)\s+([a-z0-9_\-]+)/);
    if (mSeed) { $("seed").value = mSeed[1]; vf = new VibeForge(mSeed[1]); did = "semilla=" + mSeed[1]; }
    const mCx = t.match(/(?:complejidad|biomas?|nivel)\D*(\d)/);
    if (mCx) { const n = Math.max(1, Math.min(6, +mCx[1])); $("complexity").value = n; $("complexity-val").textContent = n; did += (did ? " · " : "") + "complejidad=" + n; }
    const wantsScene = /materializa|escena|scene|sketch|construye|dibuja/.test(t) || Object.keys(SYN).some((k) => new RegExp("\\b" + k + "\\b").test(t));
    const wantsWorld = /genera|nuevo|crea|regenera|mundo|world/.test(t) && !wantsScene;
    if (wantsWorld) { genWorld(); did += (did ? " · " : "") + "mundo " + (world ? world.seed_hash : ""); }
    else if (wantsScene) {
      const found = []; for (const tok of t.split(/[^a-záéíóúñ]+/)) if (SYN[tok] && !found.includes(SYN[tok])) found.push(SYN[tok]);
      if (found.length) $("sketch").value = found.join(" ");
      materialize(); did += (did ? " · " : "") + "escena " + (scene ? scene.scene_id : "");
    }
    log("CMD", did || "no entendí — prueba: «genera mundo complejidad 5» · «materializa altar templo gate» · «semilla egipto»", "#c79bff");
  }

  // ── Cableado ─────────────────────────────────────────────────────────────────
  $("btn-cmd").addEventListener("click", () => { parseCmd($("vf-cmd").value); $("vf-cmd").value = ""; });
  $("vf-cmd").addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); parseCmd($("vf-cmd").value); $("vf-cmd").value = ""; } });
  $("btn-rand-seed").addEventListener("click", () => { $("seed").value = String(Math.floor(Math.random() * 999999)); });
  $("complexity").addEventListener("input", () => { $("complexity-val").textContent = $("complexity").value; });
  $("btn-gen-world").addEventListener("click", genWorld);
  $("btn-materialize").addEventListener("click", materialize);

  renderWorld(); renderScene(); renderGates();
  function resize() { cv.width = cv.clientWidth; cv.height = cv.clientHeight; }
  window.addEventListener("resize", resize); resize();
  connectMotor().then(() => { genWorld(); });   // autoconecta motor y forja un mundo de arranque
})();
