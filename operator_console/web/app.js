"use strict";

const GIB = 1024 ** 3;

const elements = {
  introStatus: document.querySelector("#introStatus"),
  providerGrid: document.querySelector("#providerGrid"),
  taskGrid: document.querySelector("#taskGrid"),
  materialNote: document.querySelector("#materialNote"),
  prompt: document.querySelector("#prompt"),
  promptCount: document.querySelector("#promptCount"),
  executionId: document.querySelector("#executionId"),
  generateId: document.querySelector("#generateId"),
  width: document.querySelector("#width"),
  height: document.querySelector("#height"),
  numFrames: document.querySelector("#numFrames"),
  numSteps: document.querySelector("#numSteps"),
  guidance: document.querySelector("#guidance"),
  fps: document.querySelector("#fps"),
  seed: document.querySelector("#seed"),
  timeout: document.querySelector("#timeout"),
  preflightMemory: document.querySelector("#preflightMemory"),
  abortMemory: document.querySelector("#abortMemory"),
  swapGrowth: document.querySelector("#swapGrowth"),
  riskAcknowledged: document.querySelector("#riskAcknowledged"),
  riskMessage: document.querySelector("#riskMessage"),
  preflightTitle: document.querySelector("#preflightTitle"),
  preflightDescription: document.querySelector("#preflightDescription"),
  preflightResults: document.querySelector("#preflightResults"),
  preflightButton: document.querySelector("#preflightButton"),
  registerButton: document.querySelector("#registerButton"),
  hostCard: document.querySelector("#hostCard"),
  confirmationCard: document.querySelector("#confirmationCard"),
  jobCount: document.querySelector("#jobCount"),
  jobList: document.querySelector("#jobList"),
  freshness: document.querySelector("#freshness"),
  toast: document.querySelector("#toast"),
  jobForm: document.querySelector("#jobForm"),
};

const state = {
  overview: null,
  csrfToken: null,
  catalogRendered: false,
  providerKey: "wan",
  taskType: "text_to_video",
  preflight: null,
  preflightFingerprint: null,
  selectedJobId: null,
  selectedJob: null,
  refreshTimer: null,
  requestInFlight: false,
  toastTimer: null,
};

const jobStateLabels = {
  REGISTERED: "已登记",
  STARTING: "正在启动",
  RUNNING: "正在运行",
  STOP_REQUESTED: "正在停止",
  COMPLETED: "已形成输出",
  FAILED: "执行未完成",
  STOPPED: "已停止",
};

const jobStateClasses = {
  REGISTERED: "registered",
  STARTING: "starting",
  RUNNING: "running",
  STOP_REQUESTED: "stop_requested",
  COMPLETED: "completed",
  FAILED: "failed",
  STOPPED: "stopped",
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatBytes(value, precision = 1) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  const bytes = Number(value);
  if (bytes === 0) return "0 B";
  const units = ["B", "KiB", "MiB", "GiB", "TiB"];
  const index = Math.min(Math.floor(Math.log(Math.abs(bytes)) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** index).toFixed(index ? precision : 0)} ${units[index]}`;
}

function formatTime(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add("is-visible");
  window.clearTimeout(state.toastTimer);
  state.toastTimer = window.setTimeout(() => elements.toast.classList.remove("is-visible"), 2800);
}

function providerProfile(key) {
  return state.overview?.catalog.providers.find((item) => item.key === key);
}

function modelStatus(key) {
  return state.overview?.models.find((item) => item.key === key);
}

function renderCatalog() {
  const catalog = state.overview.catalog;
  elements.providerGrid.innerHTML = catalog.providers.map((profile) => {
    const model = modelStatus(profile.key);
    const runtimeReady = profile.startable;
    const statusLabel = runtimeReady ? "已观察运行" : "运行性未知";
    const statusClass = runtimeReady ? "ready" : "blocked";
    return `
      <label class="provider-card ${profile.key === state.providerKey ? "is-selected" : ""}" data-provider="${escapeHtml(profile.key)}">
        <input type="radio" name="provider" value="${escapeHtml(profile.key)}" ${profile.key === state.providerKey ? "checked" : ""}>
        <span class="provider-top"><strong>${escapeHtml(profile.name)}</strong><span class="provider-state state-${statusClass}">${statusLabel}</span></span>
        <span class="provider-id">${escapeHtml(profile.model_id)}</span>
        <p class="provider-message">${escapeHtml(profile.risk_message)} 缓存：${escapeHtml(model?.state || "unknown")} · ${formatBytes(model?.cache_bytes)}</p>
      </label>`;
  }).join("");
  elements.taskGrid.innerHTML = catalog.task_types.map((task) => `
    <label class="task-card ${task.key === state.taskType ? "is-selected" : ""} ${task.available ? "" : "is-unavailable"}" data-task="${escapeHtml(task.key)}">
      <input type="radio" name="task_type" value="${escapeHtml(task.key)}" ${task.key === state.taskType ? "checked" : ""} ${task.available ? "" : "disabled"}>
      <strong>${escapeHtml(task.label)}</strong>
      <p>${escapeHtml(task.description)}</p>
    </label>`).join("");
  bindCatalogEvents();
  applyProviderDefaults();
  renderMaterialNote();
  state.catalogRendered = true;
}

function bindCatalogEvents() {
  elements.providerGrid.querySelectorAll("input[name=provider]").forEach((input) => {
    input.addEventListener("change", () => {
      state.providerKey = input.value;
      elements.providerGrid.querySelectorAll(".provider-card").forEach((card) => card.classList.toggle("is-selected", card.dataset.provider === state.providerKey));
      applyProviderDefaults();
      invalidatePreflight();
    });
  });
  elements.taskGrid.querySelectorAll("input[name=task_type]").forEach((input) => {
    input.addEventListener("change", () => {
      state.taskType = input.value;
      elements.taskGrid.querySelectorAll(".task-card").forEach((card) => card.classList.toggle("is-selected", card.dataset.task === state.taskType));
      renderMaterialNote();
      invalidatePreflight();
    });
  });
}

function applyProviderDefaults() {
  const profile = providerProfile(state.providerKey);
  if (!profile) return;
  const defaults = profile.defaults;
  elements.width.value = defaults.width;
  elements.height.value = defaults.height;
  elements.numFrames.value = defaults.num_frames;
  elements.numSteps.value = defaults.num_inference_steps;
  elements.guidance.value = defaults.guidance_scale;
  elements.fps.value = defaults.fps;
  elements.riskMessage.textContent = profile.risk_message;
}

function renderMaterialNote() {
  const task = state.overview?.catalog.task_types.find((item) => item.key === state.taskType);
  if (!task) return;
  elements.materialNote.textContent = task.requires_material
    ? "该类型需要参考素材；当前尚未接入上传和来源登记。"
    : "当前是文生视频：无需选择素材，提示词是本次作业的主要生成输入。";
}

function newExecutionId() {
  const date = new Date();
  const stamp = [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0"),
    "-",
    String(date.getHours()).padStart(2, "0"),
    String(date.getMinutes()).padStart(2, "0"),
    String(date.getSeconds()).padStart(2, "0"),
  ].join("");
  return `LOCAL-${state.providerKey.toUpperCase()}-${stamp}`;
}

function formRequest() {
  return {
    provider_key: state.providerKey,
    task_type: state.taskType,
    execution_id: elements.executionId.value.trim().toUpperCase(),
    prompt: elements.prompt.value.trim(),
    seed: Number(elements.seed.value),
    parameters: {
      width: Number(elements.width.value),
      height: Number(elements.height.value),
      num_frames: Number(elements.numFrames.value),
      num_inference_steps: Number(elements.numSteps.value),
      guidance_scale: Number(elements.guidance.value),
      fps: Number(elements.fps.value),
    },
    timeout_seconds: Number(elements.timeout.value),
    preflight_min_available_memory_bytes: Number(elements.preflightMemory.value) * GIB,
    abort_min_available_memory_bytes: Number(elements.abortMemory.value) * GIB,
    max_swap_growth_bytes: Number(elements.swapGrowth.value) * GIB,
    risk_acknowledged: elements.riskAcknowledged.checked,
  };
}

function fingerprint(value) {
  return JSON.stringify(value);
}

function invalidatePreflight() {
  const current = fingerprint(formRequest());
  if (state.preflightFingerprint === current) return;
  state.preflight = null;
  state.preflightFingerprint = null;
  elements.registerButton.disabled = true;
  elements.preflightTitle.textContent = "需要重新预检";
  elements.preflightDescription.textContent = "输入或资源预算已经变化。";
  elements.preflightResults.innerHTML = "";
}

async function apiPost(path, body) {
  const response = await fetch(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Senknet-CSRF": state.csrfToken,
    },
    body: JSON.stringify(body),
  });
  const value = await response.json();
  if (!response.ok) {
    const error = new Error(value.error?.message || `HTTP ${response.status}`);
    error.details = value.error?.details;
    error.code = value.error?.code;
    throw error;
  }
  return value;
}

async function runPreflight() {
  elements.preflightButton.disabled = true;
  elements.preflightButton.textContent = "检查中…";
  try {
    const request = formRequest();
    const result = await apiPost("/api/v1/preflight", request);
    state.preflight = result;
    state.preflightFingerprint = fingerprint(request);
    renderPreflight(result);
  } catch (error) {
    showToast(`预检请求失败：${error.message}`);
  } finally {
    elements.preflightButton.disabled = false;
    elements.preflightButton.textContent = "运行预检";
  }
}

function renderPreflight(result) {
  elements.preflightTitle.textContent = result.passed ? "预检通过，可以登记" : `${result.blocking_count} 项阻断`;
  elements.preflightDescription.textContent = result.passed
    ? "当前现实满足登记条件；启动时仍会再次检查。"
    : "修正字段或资源状态后重新预检。";
  const errorRows = (result.errors || []).map((error) => ({
    status: "blocked",
    label: error.field,
    message: error.message,
  }));
  elements.preflightResults.innerHTML = [...errorRows, ...(result.checks || [])].map((check) => `
    <div class="check-row is-${escapeHtml(check.status)}">
      <span class="check-dot">${check.status === "passed" ? "✓" : "!"}</span>
      <div><strong>${escapeHtml(check.label)}</strong><p>${escapeHtml(check.message)}</p></div>
    </div>`).join("");
  elements.registerButton.disabled = !result.passed;
}

async function registerJob() {
  if (!state.preflight?.passed || state.preflightFingerprint !== fingerprint(formRequest())) {
    invalidatePreflight();
    showToast("请先对当前输入重新执行预检。");
    return;
  }
  elements.registerButton.disabled = true;
  elements.registerButton.textContent = "登记中…";
  try {
    const job = await apiPost("/api/v1/jobs", formRequest());
    state.selectedJobId = job.job_id;
    state.selectedJob = job;
    showToast("作业请求已登记；尚未启动模型。 ");
    renderConfirmation();
    await refreshOverview();
  } catch (error) {
    if (error.details) renderPreflight(error.details);
    showToast(`登记失败：${error.message}`);
  } finally {
    elements.registerButton.textContent = "登记不可变作业";
    elements.registerButton.disabled = !state.preflight?.passed;
  }
}

function renderHost() {
  const system = state.overview.system;
  const memory = system.memory;
  const swap = system.swap;
  const disk = system.disk;
  elements.hostCard.innerHTML = `
    <div class="side-head"><div><span class="eyebrow">LIVE HOST</span><h2>启动资源</h2></div><span class="live-pill"><i></i>实时</span></div>
    <div class="host-overview">
      <div class="memory-orbit" style="--value:${memory.used_percent * 3.6}deg"><span>${Number(memory.used_percent).toFixed(0)}%</span></div>
      <div class="host-lines">
        ${hostLine("可用", memory.available_bytes, memory.total_bytes)}
        ${hostLine("换页", swap.used_bytes, swap.total_bytes)}
        ${hostLine("磁盘", disk.free_bytes, disk.total_bytes)}
      </div>
    </div>
    <div class="host-foot"><span>内存压力 <strong>${escapeHtml(memory.pressure)}</strong></span><span>生成进程 <strong>${state.overview.active_generation_processes.length}</strong></span></div>`;
}

function hostLine(label, value, total) {
  const percent = Math.min(100, Number(value || 0) / Math.max(1, Number(total || 0)) * 100);
  return `<div class="host-line"><span>${escapeHtml(label)}</span><div class="tiny-track"><i style="width:${percent}%"></i></div><strong>${formatBytes(value)}</strong></div>`;
}

function jobStateBadge(job) {
  const label = jobStateLabels[job.state] || job.state;
  const css = jobStateClasses[job.state] || "blocked";
  return `<span class="job-state state-${css}">${escapeHtml(label)}</span>`;
}

function renderJobs() {
  const jobs = state.overview.jobs || [];
  elements.jobCount.textContent = `${jobs.length} 项`;
  elements.jobList.innerHTML = jobs.length
    ? jobs.map((job) => `
        <button class="job-item ${job.job_id === state.selectedJobId ? "is-selected" : ""}" type="button" data-job-id="${escapeHtml(job.job_id)}">
          <span class="job-item-top"><span>${escapeHtml(job.provider_key.toUpperCase())}</span>${jobStateBadge(job)}</span>
          <strong>${escapeHtml(job.execution_id)}</strong>
          <p>${escapeHtml(job.prompt)}</p>
        </button>`).join("")
    : '<div class="empty-list">尚无本地作业</div>';
}

function renderConfirmation() {
  const job = state.selectedJob;
  if (!job) {
    elements.confirmationCard.innerHTML = `
      <div class="side-head"><div><span class="eyebrow">EXPLICIT AUTHORITY</span><h2>启动确认</h2></div></div>
      <div class="empty-confirmation"><span>⌁</span><strong>尚未登记作业</strong><p>预检通过并登记后，必须再次输入执行标识才能启动。</p></div>`;
    return;
  }
  const head = `<div class="side-head"><div><span class="eyebrow">EXPLICIT AUTHORITY</span><h2>启动确认</h2></div>${jobStateBadge(job)}</div>`;
  if (job.state === "REGISTERED") {
    elements.confirmationCard.innerHTML = `${head}
      <div class="confirm-spec">
        <div class="confirm-title"><span>不可变执行标识</span><strong>${escapeHtml(job.execution_id)}</strong></div>
        <div class="confirm-title"><span>作业标识</span><strong>${escapeHtml(job.job_id)}</strong></div>
        <p class="confirm-instruction">输入完整执行标识 <code>${escapeHtml(job.execution_id)}</code>，确认后才会加载模型。</p>
        <input class="confirm-input" id="confirmationInput" autocomplete="off" placeholder="输入执行标识">
        <div class="confirm-actions"><button class="primary-button" id="startJobButton" type="button" disabled>确认并启动</button></div>
      </div>`;
    const input = document.querySelector("#confirmationInput");
    const button = document.querySelector("#startJobButton");
    input.addEventListener("input", () => { button.disabled = input.value !== job.execution_id; });
    button.addEventListener("click", () => startJob(job, input.value));
  } else if (["STARTING", "RUNNING", "STOP_REQUESTED"].includes(job.state)) {
    elements.confirmationCard.innerHTML = `${head}
      <div class="running-actions">
        <div class="running-callout"><strong>${job.state === "STOP_REQUESTED" ? "停止信号已发出" : "模型作业正在运行"}</strong>进程 ${escapeHtml(job.pid || "—")} · 观测台将显示阶段、内存和输出。</div>
        <a class="secondary-button observatory-link" href="http://127.0.0.1:4319/?execution_id=${encodeURIComponent(job.execution_id)}" target="_blank" rel="noopener">在观测台查看 ↗</a>
        <button class="danger-button" id="stopJobButton" type="button" ${job.state === "STOP_REQUESTED" ? "disabled" : ""}>安全停止作业</button>
      </div>`;
    document.querySelector("#stopJobButton")?.addEventListener("click", () => stopJob(job));
  } else {
    const events = (job.events || []).slice().reverse().map((event) => `
      <div class="event-row"><span>${String(event.sequence).padStart(2, "0")}</span><div><strong>${escapeHtml(event.event_type)}</strong><time>${escapeHtml(formatTime(event.recorded_at))}</time></div></div>`).join("");
    elements.confirmationCard.innerHTML = `${head}
      <div class="confirm-spec">
        <div class="confirm-title"><span>终止原因</span><strong>${escapeHtml(job.terminal_reason || "—")}</strong></div>
        <a class="secondary-button observatory-link" href="http://127.0.0.1:4319/?execution_id=${encodeURIComponent(job.execution_id)}" target="_blank" rel="noopener">查看执行证据 ↗</a>
        <div class="job-events">${events}</div>
      </div>`;
  }
}

async function startJob(job, confirmation) {
  const button = document.querySelector("#startJobButton");
  button.disabled = true;
  button.textContent = "启动中…";
  try {
    state.selectedJob = await apiPost(`/api/v1/jobs/${encodeURIComponent(job.job_id)}/start`, {
      confirmation_execution_id: confirmation,
    });
    showToast("执行进程已启动；请在观测台查看资源与阶段。 ");
    renderConfirmation();
    await refreshOverview();
  } catch (error) {
    showToast(`启动被阻断：${error.message}`);
    button.disabled = false;
    button.textContent = "确认并启动";
  }
}

async function stopJob(job) {
  const button = document.querySelector("#stopJobButton");
  button.disabled = true;
  button.textContent = "正在停止…";
  try {
    state.selectedJob = await apiPost(`/api/v1/jobs/${encodeURIComponent(job.job_id)}/stop`, {});
    showToast("停止信号已发送到对应进程树。 ");
    renderConfirmation();
    await refreshOverview();
  } catch (error) {
    showToast(`停止失败：${error.message}`);
    button.disabled = false;
    button.textContent = "安全停止作业";
  }
}

async function selectJob(jobId) {
  state.selectedJobId = jobId;
  try {
    const response = await fetch(`/api/v1/jobs/${encodeURIComponent(jobId)}`, { cache: "no-store" });
    const value = await response.json();
    if (!response.ok) throw new Error(value.error?.message || `HTTP ${response.status}`);
    state.selectedJob = value;
    renderJobs();
    renderConfirmation();
  } catch (error) {
    showToast(`无法读取作业：${error.message}`);
  }
}

async function refreshOverview() {
  if (state.requestInFlight) return;
  state.requestInFlight = true;
  try {
    const response = await fetch("/api/v1/operator", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.overview = await response.json();
    state.csrfToken = state.overview.csrf_token;
    if (!state.catalogRendered) {
      renderCatalog();
      elements.seed.value = state.overview.catalog.defaults.seed;
      elements.executionId.value = newExecutionId();
    }
    elements.introStatus.innerHTML = '<span>控制服务</span><strong>已连接 · 等待人工操作</strong>';
    elements.freshness.dateTime = state.overview.generated_at;
    elements.freshness.textContent = formatTime(state.overview.generated_at);
    renderHost();
    renderJobs();
    if (state.selectedJobId) {
      const selectedExists = state.overview.jobs.some((job) => job.job_id === state.selectedJobId);
      if (selectedExists) await selectJob(state.selectedJobId);
      else { state.selectedJobId = null; state.selectedJob = null; renderConfirmation(); }
    }
  } catch (error) {
    elements.introStatus.innerHTML = '<span>控制服务</span><strong>连接中断</strong>';
    showToast(`无法连接本地控制服务：${error.message}`);
  } finally {
    state.requestInFlight = false;
    scheduleRefresh();
  }
}

function scheduleRefresh() {
  window.clearTimeout(state.refreshTimer);
  state.refreshTimer = window.setTimeout(refreshOverview, document.hidden ? 6000 : 2000);
}

elements.prompt.addEventListener("input", () => {
  elements.promptCount.textContent = `${elements.prompt.value.length} / 2000`;
});
elements.generateId.addEventListener("click", () => {
  elements.executionId.value = newExecutionId();
  invalidatePreflight();
});
elements.preflightButton.addEventListener("click", runPreflight);
elements.registerButton.addEventListener("click", registerJob);
elements.jobForm.addEventListener("input", invalidatePreflight);
elements.jobForm.addEventListener("change", invalidatePreflight);
elements.jobList.addEventListener("click", (event) => {
  const item = event.target.closest("[data-job-id]");
  if (item) selectJob(item.dataset.jobId);
});
document.addEventListener("visibilitychange", scheduleRefresh);

refreshOverview();
