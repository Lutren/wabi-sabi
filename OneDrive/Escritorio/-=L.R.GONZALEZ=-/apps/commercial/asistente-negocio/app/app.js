const STORAGE_KEY = "medioevo_business_assistant_profile";
const LOG_KEY = "medioevo_business_assistant_approval_log";
const COMPACT_KEY = "medioevo_business_assistant_compact_mode";
const TUTORIAL_SEEN_KEY = "medioevo_business_assistant_tutorial_seen";
const PRODUCT_VERSION = "1.0.0";

const profileForm = document.querySelector("#profile-form");
const draftButton = document.querySelector("#draft-button");
const copyButton = document.querySelector("#copy-button");
const approveButton = document.querySelector("#approve-button");
const watchClipboardButton = document.querySelector("#watch-clipboard-button");
const voiceDictateButton = document.querySelector("#voice-dictate-button");
const voiceReadButton = document.querySelector("#voice-read-button");
const demoMessageButton = document.querySelector("#demo-message-button");
const approvalLog = document.querySelector("#approval-log");
const incomingMessage = document.querySelector("#incoming-message");
const draftOutput = document.querySelector("#draft-output");
const sendStatus = document.querySelector("#send-status");
const monitorStatus = document.querySelector("#monitor-status");
const emailSendLink = document.querySelector("#email-send-link");
const whatsappSendLink = document.querySelector("#whatsapp-send-link");
const autoDraftOk = document.querySelector("#auto-draft-ok");
const voiceAlertOk = document.querySelector("#voice-alert-ok");
const assistantState = document.querySelector("#assistant-state");
const savedBusinessName = document.querySelector("#saved-business-name");
const messageState = document.querySelector("#message-state");
const draftState = document.querySelector("#draft-state");
const flowSteps = [1, 2, 3].map((step) => document.querySelector(`#flow-step-${step}`));
const tutorialPanel = document.querySelector("#tutorial-panel");
const tutorialOpenButton = document.querySelector("#tutorial-open-button");
const tutorialCloseButton = document.querySelector("#tutorial-close-button");
const tutorialStartButton = document.querySelector("#tutorial-start-button");
const tutorialDemoButton = document.querySelector("#tutorial-demo-button");
const toolbarDemoButton = document.querySelector("#toolbar-demo-button");
const compactModeButton = document.querySelector("#compact-mode-button");
const exportDataButton = document.querySelector("#export-data-button");
const clearDataButton = document.querySelector("#clear-data-button");
const dataStatus = document.querySelector("#data-status");

let clipboardTimer = null;
let lastClipboardText = "";

function jumpTo(selector, currentStep) {
  const target = document.querySelector(selector);
  if (!target) return;
  target.scrollIntoView({ behavior: "smooth", block: "start" });
  refreshInterface(currentStep);
}

function openTutorial() {
  if (!tutorialPanel) return;
  tutorialPanel.hidden = false;
  tutorialOpenButton?.setAttribute("aria-expanded", "true");
}

function closeTutorial() {
  if (!tutorialPanel) return;
  tutorialPanel.hidden = true;
  tutorialOpenButton?.setAttribute("aria-expanded", "false");
  localStorage.setItem(TUTORIAL_SEEN_KEY, "true");
}

function applyCompactMode(enabled) {
  document.body.classList.toggle("compact-mode", enabled);
  compactModeButton?.setAttribute("aria-pressed", enabled ? "true" : "false");
  localStorage.setItem(COMPACT_KEY, enabled ? "true" : "false");
}

function loadToolbarState() {
  applyCompactMode(localStorage.getItem(COMPACT_KEY) === "true");
  tutorialOpenButton?.setAttribute("aria-expanded", "false");
  if (localStorage.getItem(TUTORIAL_SEEN_KEY) !== "true") {
    openTutorial();
  }
}

function readProfile() {
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw ? JSON.parse(raw) : null;
}

function writeProfile(form) {
  const data = new FormData(form);
  const profile = {
    businessName: data.get("businessName"),
    contactEmail: data.get("contactEmail"),
    customerEmail: data.get("customerEmail"),
    customerWhatsapp: data.get("customerWhatsapp"),
    tone: data.get("tone"),
    priceList: data.get("priceList"),
    businessHours: data.get("businessHours"),
    businessNotes: data.get("businessNotes"),
    savedAt: new Date().toISOString(),
    publicProfile: "public_safe",
    autonomy: "human_approved_external_send"
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
  return profile;
}

function loadProfileIntoForm() {
  const profile = readProfile();
  if (!profile) return;

  document.querySelector("#business-name").value = profile.businessName || "";
  document.querySelector("#contact-email").value = profile.contactEmail || "";
  document.querySelector("#customer-email").value = profile.customerEmail || "";
  document.querySelector("#customer-whatsapp").value = profile.customerWhatsapp || "";
  document.querySelector("#tone").value = profile.tone || "claro";
  document.querySelector("#price-list").value = profile.priceList || "";
  document.querySelector("#business-hours").value = profile.businessHours || "";
  document.querySelector("#business-notes").value = profile.businessNotes || "";
}

function setFlowStep(currentStep) {
  const profile = readProfile();
  const hasMessage = Boolean(incomingMessage.value.trim());
  const hasDraft = Boolean(draftOutput.value.trim());
  const reviewed = document.querySelector("#reviewed-ok").checked;

  flowSteps.forEach((item, index) => {
    if (!item) return;
    const step = index + 1;
    const done =
      (step === 1 && Boolean(profile)) ||
      (step === 2 && hasMessage && hasDraft) ||
      (step === 3 && reviewed);

    item.classList.toggle("is-current", step === currentStep);
    item.classList.toggle("is-done", done);
  });
}

function refreshInterface(currentStep = 1) {
  const profile = readProfile();
  const hasMessage = Boolean(incomingMessage.value.trim());
  const hasDraft = Boolean(draftOutput.value.trim());
  const reviewed = document.querySelector("#reviewed-ok").checked;

  if (assistantState) {
    assistantState.textContent = profile ? "Negocio listo" : "Setup pendiente";
  }

  if (savedBusinessName) {
    savedBusinessName.textContent = profile?.businessName || "Guarda tu negocio para empezar.";
  }

  if (messageState) {
    messageState.textContent = hasMessage ? "Mensaje cargado" : "Sin mensaje";
  }

  if (draftState) {
    if (reviewed && hasDraft) {
      draftState.textContent = "Respuesta aprobada";
    } else if (hasDraft) {
      draftState.textContent = "Respuesta por revisar";
    } else {
      draftState.textContent = "Sin respuesta";
    }
  }

  setFlowStep(currentStep);
}

function toneLine(tone) {
  const lines = {
    claro: "Gracias por escribirnos. Te ayudo con gusto.",
    cercano: "Gracias por tu mensaje, con gusto te apoyo.",
    breve: "Gracias. Te dejo la respuesta concreta.",
    premium: "Gracias por contactarnos. Revisamos tu solicitud con atencion."
  };
  return lines[tone] || lines.claro;
}

function generateDraft(profile, message) {
  const cleanMessage = message.trim();
  if (!cleanMessage) {
    return "Escribe o pega primero el mensaje del cliente.";
  }

  const lower = cleanMessage.toLowerCase();
  const answerBlocks = [];

  if (/(precio|precios|costo|cu[aá]nto|cuanto|tarifa|vale|cobran)/i.test(lower)) {
    answerBlocks.push(profile.priceList ? `Precios: ${profile.priceList}` : "Te puedo compartir precios segun el servicio que necesites.");
  }

  if (/(horario|hora|abren|abierto|atienden|disponible)/i.test(lower)) {
    answerBlocks.push(profile.businessHours ? `Horarios: ${profile.businessHours}` : "Podemos revisar disponibilidad y horario para atenderte.");
  }

  if (/(cita|agendar|reservar|turno|consulta)/i.test(lower)) {
    answerBlocks.push("Si quieres, podemos agendar una cita. Dime que dia y horario te queda mejor.");
  }

  if (/(pago|pagos|tarjeta|transferencia|efectivo|factura)/i.test(lower)) {
    answerBlocks.push(profile.businessNotes ? `Notas de pago o atencion: ${profile.businessNotes}` : "Podemos confirmar forma de pago antes de avanzar.");
  }

  if (!answerBlocks.length) {
    answerBlocks.push("Puedo ayudarte. Para darte una respuesta precisa, confirmame el servicio que necesitas y para cuando lo necesitas.");
  }

  return [
    `Hola, gracias por contactar a ${profile.businessName}.`,
    toneLine(profile.tone),
    "",
    ...answerBlocks,
    "",
    "Mensaje recibido:",
    `"${cleanMessage.slice(0, 420)}${cleanMessage.length > 420 ? "..." : ""}"`,
    "",
    "Quedo atento.",
    "",
    `${profile.businessName}`,
    profile.contactEmail
  ].join("\n");
}

function speak(text) {
  if (!("speechSynthesis" in window) || !text) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "es-MX";
  utterance.rate = 0.95;
  window.speechSynthesis.speak(utterance);
}

function beep() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audio = new AudioContext();
    const oscillator = audio.createOscillator();
    const gain = audio.createGain();
    oscillator.frequency.value = 740;
    gain.gain.value = 0.05;
    oscillator.connect(gain);
    gain.connect(audio.destination);
    oscillator.start();
    setTimeout(() => {
      oscillator.stop();
      audio.close();
    }, 180);
  } catch {
    // Audio is optional.
  }
}

function notifyNewMessage(message) {
  const preview = message.slice(0, 90);
  beep();
  monitorStatus.textContent = `Nuevo mensaje detectado: ${preview}${message.length > 90 ? "..." : ""}`;

  if ("Notification" in window) {
    if (Notification.permission === "granted") {
      new Notification("Nuevo mensaje de cliente", { body: preview });
    } else if (Notification.permission !== "denied") {
      Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
          new Notification("Nuevo mensaje de cliente", { body: preview });
        }
      });
    }
  }

  if (voiceAlertOk.checked) {
    speak("Nuevo mensaje de cliente. Estoy preparando la respuesta.");
  }
}

function createDraftFromCurrentMessage() {
  const profile = readProfile();
  if (!profile) {
    draftOutput.value = "Guarda primero los datos minimos del negocio.";
    updateSendLinks();
    refreshInterface(1);
    return;
  }

  draftOutput.value = generateDraft(profile, incomingMessage.value);
  document.querySelector("#reviewed-ok").checked = false;
  writeLog({
    timestamp: new Date().toLocaleString(),
    action: "respuesta_creada",
    note: "pendiente de revision"
  });
  updateSendLinks();
  refreshInterface(2);
}

async function readClipboardText() {
  if (window.medioevo?.readClipboardText) {
    return window.medioevo.readClipboardText();
  }
  if (navigator.clipboard?.readText) {
    return navigator.clipboard.readText();
  }
  throw new Error("clipboard_unavailable");
}

async function pollClipboard() {
  try {
    const text = (await readClipboardText()).trim();
    if (!text || text.length < 8 || text === lastClipboardText) return;

    lastClipboardText = text;
    incomingMessage.value = text;
    refreshInterface(2);
    notifyNewMessage(text);
    writeLog({
      timestamp: new Date().toLocaleString(),
      action: "mensaje_detectado",
      note: "desde portapapeles"
    });
    if (autoDraftOk.checked) {
      createDraftFromCurrentMessage();
    }
  } catch {
    monitorStatus.textContent = "No puedo leer el portapapeles aqui. Pega el mensaje o usa dictado.";
  }
}

function normalizeWhatsappNumber(value) {
  return String(value || "").replace(/\D/g, "");
}

function setSendLink(link, href, enabled) {
  link.href = enabled ? href : "#";
  link.classList.toggle("ready", enabled);
  link.classList.toggle("disabled", !enabled);
  link.setAttribute("aria-disabled", enabled ? "false" : "true");
}

function updateSendLinks() {
  const profile = readProfile();
  const draft = draftOutput.value.trim();
  const reviewed = document.querySelector("#reviewed-ok").checked;
  const canSend = Boolean(profile && draft && reviewed);

  const emailReady = canSend && Boolean(profile.customerEmail);
  const mailSubject = `Respuesta de ${profile?.businessName || "mi negocio"}`;
  const mailto = `mailto:${encodeURIComponent(profile?.customerEmail || "")}?subject=${encodeURIComponent(mailSubject)}&body=${encodeURIComponent(draft)}`;
  setSendLink(emailSendLink, mailto, emailReady);

  const whatsappNumber = normalizeWhatsappNumber(profile?.customerWhatsapp);
  const whatsappReady = canSend && whatsappNumber.length >= 8;
  const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(draft)}`;
  setSendLink(whatsappSendLink, whatsappUrl, whatsappReady);

  if (!profile) {
    sendStatus.textContent = "Guarda los datos minimos para activar el envio.";
  } else if (!draft) {
    sendStatus.textContent = "Crea una respuesta antes de enviar.";
  } else if (!reviewed) {
    sendStatus.textContent = "Marca que ya revisaste el texto.";
  } else if (!emailReady && !whatsappReady) {
    sendStatus.textContent = "Agrega correo o WhatsApp del cliente.";
  } else {
    sendStatus.textContent = "Listo: abre correo o WhatsApp y pulsa Enviar en tu app.";
  }
  refreshInterface(canSend ? 3 : draft ? 2 : profile ? 1 : 1);
}

function readLog() {
  const raw = localStorage.getItem(LOG_KEY);
  return raw ? JSON.parse(raw) : [];
}

function writeLog(entry) {
  const log = [entry, ...readLog()].slice(0, 20);
  localStorage.setItem(LOG_KEY, JSON.stringify(log));
  renderLog();
}

function renderLog() {
  approvalLog.innerHTML = "";
  readLog().forEach((entry) => {
    const item = document.createElement("li");
    item.textContent = `${entry.timestamp} · ${entry.action} · ${entry.note}`;
    approvalLog.appendChild(item);
  });
}

function buildExportPayload() {
  return {
    product: "Asistente de Negocio MEDIOEVO",
    version: PRODUCT_VERSION,
    profile: "public_safe",
    exportedAt: new Date().toISOString(),
    businessProfile: readProfile(),
    approvalLog: readLog()
  };
}

function downloadJson(filename, payload) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

function resetLocalData() {
  [STORAGE_KEY, LOG_KEY, COMPACT_KEY, TUTORIAL_SEEN_KEY].forEach((key) => localStorage.removeItem(key));
  profileForm.reset();
  incomingMessage.value = "";
  draftOutput.value = "";
  document.querySelector("#reviewed-ok").checked = false;
  applyCompactMode(false);
  renderLog();
  updateSendLinks();
  refreshInterface(1);
}

profileForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const profile = writeProfile(profileForm);
  writeLog({
    timestamp: new Date().toLocaleString(),
    action: "datos_guardados",
    note: `${profile.businessName}`
  });
  document.querySelector("#paso-2").scrollIntoView({ behavior: "smooth", block: "start" });
  updateSendLinks();
  refreshInterface(2);
});

draftButton.addEventListener("click", () => {
  createDraftFromCurrentMessage();
});

watchClipboardButton.addEventListener("click", async () => {
  if (clipboardTimer) {
    clearInterval(clipboardTimer);
    clipboardTimer = null;
    watchClipboardButton.textContent = "Activar avisos";
    monitorStatus.textContent = "Avisos pausados.";
    return;
  }

  try {
    lastClipboardText = (await readClipboardText()).trim();
  } catch {
    lastClipboardText = "";
  }

  clipboardTimer = setInterval(pollClipboard, 3000);
  watchClipboardButton.textContent = "Pausar avisos";
  monitorStatus.textContent = "Avisos activos: copia un mensaje y lo detecto solo.";
  refreshInterface(2);
  if (voiceAlertOk.checked) {
    speak("Avisos activos.");
  }
});

voiceDictateButton.addEventListener("click", () => {
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    monitorStatus.textContent = "Dictado no disponible en este equipo. Puedes pegar el mensaje.";
    return;
  }

  const recognition = new Recognition();
  recognition.lang = "es-MX";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  monitorStatus.textContent = "Escuchando...";
  recognition.onresult = (event) => {
    incomingMessage.value = event.results[0][0].transcript;
    refreshInterface(2);
    notifyNewMessage(incomingMessage.value);
    if (autoDraftOk.checked) {
      createDraftFromCurrentMessage();
    }
  };
  recognition.onerror = () => {
    monitorStatus.textContent = "No pude escuchar bien. Intenta otra vez o pega el mensaje.";
  };
  recognition.start();
});

voiceReadButton.addEventListener("click", () => {
  speak(draftOutput.value || "Aun no hay respuesta para leer.");
});

demoMessageButton.addEventListener("click", () => {
  incomingMessage.value = "Hola, quiero saber precios, horarios y si puedo agendar una cita.";
  refreshInterface(2);
  notifyNewMessage(incomingMessage.value);
  if (autoDraftOk.checked) {
    createDraftFromCurrentMessage();
  }
});

toolbarDemoButton?.addEventListener("click", () => {
  demoMessageButton.click();
  jumpTo("#paso-2", 2);
});

tutorialDemoButton?.addEventListener("click", () => {
  demoMessageButton.click();
  closeTutorial();
  jumpTo("#paso-2", 2);
});

tutorialStartButton?.addEventListener("click", () => {
  closeTutorial();
  jumpTo("#paso-1", 1);
});

tutorialOpenButton?.addEventListener("click", () => {
  if (tutorialPanel?.hidden) {
    openTutorial();
  } else {
    closeTutorial();
  }
});

tutorialCloseButton?.addEventListener("click", closeTutorial);

compactModeButton?.addEventListener("click", () => {
  applyCompactMode(!document.body.classList.contains("compact-mode"));
});

exportDataButton?.addEventListener("click", () => {
  const filename = `medioevo_asistente_negocio_respaldo_${new Date().toISOString().slice(0, 10)}.json`;
  downloadJson(filename, buildExportPayload());
  if (dataStatus) {
    dataStatus.textContent = "Respaldo descargado. Guardalo donde tengas tus documentos.";
  }
  writeLog({
    timestamp: new Date().toLocaleString(),
    action: "respaldo_descargado",
    note: "datos locales exportados"
  });
});

clearDataButton?.addEventListener("click", () => {
  const ok = window.confirm("Esto borra datos del negocio, historial y preferencias guardadas en este equipo. Continuar?");
  if (!ok) return;
  resetLocalData();
  if (dataStatus) {
    dataStatus.textContent = "Datos locales borrados.";
  }
});

document.querySelectorAll("[data-jump]").forEach((button) => {
  button.addEventListener("click", () => {
    const selector = button.getAttribute("data-jump");
    const step = Number(selector?.match(/\d+/)?.[0] || 1);
    if (selector) jumpTo(selector, step);
  });
});

copyButton.addEventListener("click", async () => {
  if (!draftOutput.value.trim()) return;
  try {
    await navigator.clipboard.writeText(draftOutput.value);
    writeLog({
      timestamp: new Date().toLocaleString(),
      action: "respuesta_copiada",
      note: "lista para pegar"
    });
  } catch {
    draftOutput.focus();
    draftOutput.select();
    writeLog({
      timestamp: new Date().toLocaleString(),
      action: "copiado_manual",
      note: "usa Ctrl+C"
    });
  }
});

approveButton.addEventListener("click", () => {
  const reviewed = document.querySelector("#reviewed-ok").checked;
  if (!reviewed || !draftOutput.value.trim()) {
    writeLog({
      timestamp: new Date().toLocaleString(),
      action: "aprobacion_pendiente",
      note: "falta revisar o crear respuesta"
    });
    updateSendLinks();
    refreshInterface(3);
    return;
  }

  writeLog({
    timestamp: new Date().toLocaleString(),
    action: "respuesta_aprobada",
    note: "envio externo habilitado"
  });
  updateSendLinks();
  refreshInterface(3);
});

emailSendLink.addEventListener("click", () => {
  if (emailSendLink.classList.contains("disabled")) return;
  writeLog({
    timestamp: new Date().toLocaleString(),
    action: "correo_abierto",
    note: "envio final ocurre en la app de correo"
  });
});

whatsappSendLink.addEventListener("click", () => {
  if (whatsappSendLink.classList.contains("disabled")) return;
  writeLog({
    timestamp: new Date().toLocaleString(),
    action: "whatsapp_abierto",
    note: "envio final ocurre en WhatsApp"
  });
});

document.querySelector("#reviewed-ok").addEventListener("change", updateSendLinks);
draftOutput.addEventListener("input", updateSendLinks);
incomingMessage.addEventListener("input", () => refreshInterface(2));

loadProfileIntoForm();
renderLog();
loadToolbarState();
updateSendLinks();
refreshInterface(readProfile() ? 2 : 1);
