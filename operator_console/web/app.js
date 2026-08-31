"use strict";

const GIB = 1024 ** 3;

const elements = {
  introStatus: document.querySelector("#introStatus"),
  pilotProject: document.querySelector("#pilotProject"),
  providerGrid: document.querySelector("#providerGrid"),
  taskGrid: document.querySelector("#taskGrid"),
  materialNote: document.querySelector("#materialNote"),
  generationProfile: document.querySelector("#generationProfile"),
  executionStrategy: document.querySelector("#executionStrategy"),
  profileDescription: document.querySelector("#profileDescription"),
  strategyDescription: document.querySelector("#strategyDescription"),
  prompt: document.querySelector("#prompt"),
  shotBinding: document.querySelector("#shotBinding"),
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
  preflightSwap: document.querySelector("#preflightSwap"),
  abortMemory: document.querySelector("#abortMemory"),
  swapGrowth: document.querySelector("#swapGrowth"),
  mpsFraction: document.querySelector("#mpsFraction"),
  riskAcknowledged: document.querySelector("#riskAcknowledged"),
  riskMessage: document.querySelector("#riskMessage"),
  parameterGrid: document.querySelector("#parameterGrid"),
  remoteParameterPanel: document.querySelector("#remoteParameterPanel"),
  remoteParameterSummary: document.querySelector("#remoteParameterSummary"),
  budgetSection: document.querySelector("#budgetSection"),
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
  generationProfileKey: "wan_balance_backtest",
  executionStrategy: "mps_model_offload_bounded",
  preflight: null,
  preflightFingerprint: null,
  selectedJobId: null,
  selectedJob: null,
  refreshTimer: null,
  requestInFlight: false,
  toastTimer: null,
  projectBinding: null,
};

const shotStateLabels = {
  PLANNED: "待生成",
  GENERATING: "作业中",
  CANDIDATES_READY: "已有候选",
  SELECTED: "已选择",
  RETRY_AVAILABLE: "可重试",
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

function isRemoteProvider(profile) {
  return profile?.execution_backend === "remote_api";
}

function modelStatus(key) {
  return state.overview?.models.find((item) => item.key === key);
}

function renderCatalog() {
  const catalog = state.overview.catalog;
  elements.providerGrid.innerHTML = catalog.providers.map((profile) => {
    const model = modelStatus(profile.key);
    const remote = isRemoteProvider(profile);
    const runtimeReady = profile.startable;
    const statusLabel = remote ? "远端预检" : runtimeReady ? "已观察运行" : "运行性未知";
    const statusClass = remote || runtimeReady ? "ready" : "blocked";
    const statusLine = remote
      ? `凭据环境：${escapeHtml(profile.credential_env || "—")} · ${model?.credential_present ? "已检测到环境变量" : "未检测到密钥"}`
      : `缓存：${escapeHtml(model?.state || "unknown")} · ${formatBytes(model?.cache_bytes)}`;
    return `
      <label class="provider-card ${profile.key === state.providerKey ? "is-selected" : ""}" data-provider="${escapeHtml(profile.key)}">
        <input type="radio" name="provider" value="${escapeHtml(profile.key)}" ${profile.key === state.providerKey ? "checked" : ""}>
        <span class="provider-top"><strong>${escapeHtml(profile.name)}</strong><span class="provider-state state-${statusClass}">${statusLabel}</span></span>
        <span class="provider-id">${escapeHtml(profile.model_id)}</span>
        <p class="provider-message">${escapeHtml(profile.risk_message)} ${statusLine}</p>
      </label>`;
  }).join("");
  elements.taskGrid.innerHTML = catalog.task_types.map((task) => `
    <label class="task-card ${task.key === state.taskType ? "is-selected" : ""} ${task.available ? "" : "is-unavailable"}" data-task="${escapeHtml(task.key)}">
      <input type="radio" name="task_type" value="${escapeHtml(task.key)}" ${task.key === state.taskType ? "checked" : ""} ${task.available ? "" : "disabled"}>
      <strong>${escapeHtml(task.label)}</strong>
      <p>${escapeHtml(task.description)}</p>
    </label>`).join("");
  bindCatalogEvents();
  renderExecutionControls();
  applyGenerationProfile();
  renderMaterialNote();
  state.catalogRendered = true;
}

function bindCatalogEvents() {
  elements.providerGrid.querySelectorAll("input[name=provider]").forEach((input) => {
    input.addEventListener("change", () => {
      state.providerKey = input.value;
      elements.providerGrid.querySelectorAll(".provider-card").forEach((card) => card.classList.toggle("is-selected", card.dataset.provider === state.providerKey));
      syncProviderBackend();
      renderExecutionControls();
      applyGenerationProfile();
      renderMaterialNote();
      elements.executionId.value = newExecutionId();
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
  elements.generationProfile.addEventListener("change", () => {
    state.generationProfileKey = elements.generationProfile.value;
    applyGenerationProfile();
    invalidatePreflight();
  });
  elements.executionStrategy.addEventListener("change", () => {
    state.executionStrategy = elements.executionStrategy.value;
    updateExecutionDescriptions();
    invalidatePreflight();
  });
}

function generationProfile(key = state.generationProfileKey) {
  return state.overview?.catalog.generation_profiles.find((item) => item.key === key);
}

function executionStrategy(key = state.executionStrategy) {
  return state.overview?.catalog.execution_strategies.find((item) => item.key === key);
}

function syncProviderBackend() {
  const profile = providerProfile(state.providerKey);
  const remote = isRemoteProvider(profile);
  if (remote) {
    state.executionStrategy = profile.default_execution_strategy || "remote_precheck_only";
    if (profile.default_generation_profile_key) {
      state.generationProfileKey = profile.default_generation_profile_key;
    }
  } else if (state.executionStrategy === "remote_precheck_only") {
    state.executionStrategy = "mps_model_offload_bounded";
  }
}

function renderExecutionControls() {
  const profiles = state.overview.catalog.generation_profiles.filter((item) => item.provider_key === state.providerKey);
  if (!profiles.some((item) => item.key === state.generationProfileKey)) {
    const provider = providerProfile(state.providerKey);
    const preferredKey = provider?.default_generation_profile_key || state.overview.catalog.defaults.generation_profile_key;
    const preferred = profiles.find((item) => item.key === preferredKey);
    state.generationProfileKey = (preferred || profiles[0])?.key || "";
  }
  elements.generationProfile.innerHTML = profiles.map((item) => `<option value="${escapeHtml(item.key)}">${escapeHtml(item.name)}</option>`).join("");
  elements.generationProfile.value = state.generationProfileKey;

  const backend = providerProfile(state.providerKey)?.execution_backend || "local_diffusers";
  const strategies = state.overview.catalog.execution_strategies.filter(
    (item) => (item.execution_backend || "local_diffusers") === backend
  );
  if (!strategies.some((item) => item.key === state.executionStrategy)) {
    const recommended = strategies.find((item) => item.recommended);
    state.executionStrategy = (recommended || strategies[0])?.key || "";
  }
  elements.executionStrategy.innerHTML = strategies.map((item) => `
    <option value="${escapeHtml(item.key)}">${escapeHtml(item.name)}${item.recommended ? "（推荐）" : ""}</option>`).join("");
  elements.executionStrategy.value = state.executionStrategy;
  updateExecutionDescriptions();
}

function updateExecutionDescriptions() {
  elements.profileDescription.textContent = generationProfile()?.description || "当前提供者没有可用生成档位。";
  elements.strategyDescription.textContent = executionStrategy()?.description || "执行策略不可用。";
}

function applyGenerationProfile() {
  const profile = providerProfile(state.providerKey);
  const selected = generationProfile();
  if (!profile || !selected) return;
  const remote = isRemoteProvider(profile);
  const parameters = selected.parameters;
  elements.parameterGrid.hidden = remote;
  elements.remoteParameterPanel.hidden = !remote;
  elements.budgetSection.hidden = remote;
  elements.jobForm.classList.toggle("is-remote-provider", remote);
  if (remote) {
    const parts = [
      parameters.resolution,
      parameters.duration != null ? `${parameters.duration}s` : null,
      parameters.ratio,
    ].filter(Boolean);
    if ("generate_audio" in parameters) {
      parts.push(parameters.generate_audio ? "原生音频" : "无音频");
    }
    if ("watermark" in parameters) {
      parts.push(parameters.watermark ? "含水印" : "无水印");
    }
    elements.remoteParameterSummary.textContent =
      `固定试验：${parts.join(" · ")}。默认只预检，不使用自由提示词，也不提交计费任务。`;
  } else {
    elements.width.value = parameters.width;
    elements.height.value = parameters.height;
    elements.numFrames.value = parameters.num_frames;
    elements.numSteps.value = parameters.num_inference_steps;
    elements.guidance.value = parameters.guidance_scale;
    elements.fps.value = parameters.fps;
  }
  elements.riskMessage.textContent = profile.risk_message;
  updateExecutionDescriptions();
}

function renderMaterialNote() {
  const task = state.overview?.catalog.task_types.find((item) => item.key === state.taskType);
  if (!task) return;
  const remoteProfile = providerProfile(state.providerKey);
  if (isRemoteProvider(remoteProfile)) {
    elements.materialNote.textContent =
      `当前是 ${remoteProfile.name} 远端预检：使用已登记的固定试验合同，不上传素材，也不提交计费请求。`;
    return;
  }
  elements.materialNote.textContent = task.requires_material
    ? "该类型需要参考素材；当前尚未接入上传和来源登记。"
    : "当前是文生视频：无需选择素材，提示词是本次作业的主要生成输入。";
}

function renderPilotProject() {
  const project = state.overview?.pilot_projects?.[0];
  if (!project) {
    elements.pilotProject.innerHTML = '<div class="pilot-loading">未发现可用的 30 秒样片合同。</div>';
    return;
  }
  const progress = project.progress;
  const percent = progress.shots_with_completed_candidates / Math.max(1, progress.planned_shot_count) * 100;
  elements.pilotProject.innerHTML = `
    <div class="pilot-head">
      <div>
        <span class="eyebrow">30 SECOND PILOT · DRAFT</span>
        <div class="pilot-title-line"><h2>${escapeHtml(project.title)}</h2><span class="pilot-state">非权威样片草案</span></div>
        <p class="pilot-copy">${escapeHtml(project.logline)} 六个镜头分别生成、失败可续跑；只有人工选中的候选才能在后续进入时间线。</p>
      </div>
      <div class="pilot-metrics">
        <div class="pilot-metric"><strong>30s</strong><span>目标时长</span></div>
        <div class="pilot-metric"><strong>${progress.shots_with_completed_candidates}/${progress.planned_shot_count}</strong><span>镜头有候选</span></div>
        <div class="pilot-metric"><strong>${progress.selected_shot_count}</strong><span>已人工选择</span></div>
        <button class="primary-button" type="button" data-pilot-assemble="${escapeHtml(project.project_id)}" ${progress.selected_shot_count === progress.planned_shot_count ? "" : "disabled"}>组装结构样片</button>
      </div>
    </div>
    <div class="pilot-progress"><i style="width:${percent}%"></i></div>
    <div class="shot-grid">
      ${project.shots.map((shot) => `
        <article class="shot-card ${state.projectBinding?.shot_id === shot.shot_id ? "is-bound" : ""}">
          <div class="shot-card-top"><span class="shot-index">${escapeHtml(shot.shot_id)} · ${shot.duration_seconds}s</span><span class="shot-status">${escapeHtml(shotStateLabels[shot.state] || shot.state)}${shot.completed_candidate_count ? ` · ${shot.completed_candidate_count} 候选` : ""}</span></div>
          <h3>${escapeHtml(shot.title)}</h3>
          <p>${escapeHtml(shot.purpose)}</p>
          ${shot.candidate_observations?.[0] ? `<p class="shot-observation">源 ${escapeHtml(shot.candidate_observations[0].source_duration_seconds || "—")}s · ${escapeHtml((shot.candidate_observations[0].source_resolution || []).join("×") || "未知尺寸")} · 仍需人工复审</p>` : ""}
          <button class="secondary-button" type="button" data-pilot-project="${escapeHtml(project.project_id)}" data-pilot-shot="${escapeHtml(shot.shot_id)}">${state.projectBinding?.shot_id === shot.shot_id ? "已载入" : "准备此镜头"}</button>
        </article>`).join("")}
    </div>`;
}

function loadPilotShot(projectId, shotId) {
  const project = state.overview?.pilot_projects?.find((item) => item.project_id === projectId);
  const shot = project?.shots.find((item) => item.shot_id === shotId);
  if (!project || !shot) {
    showToast("无法读取对应镜头合同。");
    return;
  }
  state.projectBinding = {
    project_id: project.project_id,
    shot_id: shot.shot_id,
    project_contract_sha256: project.contract_sha256,
    prompt_sha256: shot.prompt_sha256,
  };
  elements.prompt.value = shot.generation_prompt;
  elements.promptCount.textContent = `${elements.prompt.value.length} / 2000`;
  elements.shotBinding.textContent = `已绑定 ${project.project_id} / ${shot.shot_id} · ${shot.title}；修改提示词会使合同预检失败。`;
  elements.shotBinding.classList.add("is-active");
  elements.executionId.value = newExecutionId();
  invalidatePreflight();
  renderPilotProject();
  elements.prompt.scrollIntoView({ behavior: "smooth", block: "center" });
  showToast(`已载入 ${shot.shot_id}；尚未登记或启动模型。`);
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
  const shotPart = state.projectBinding?.shot_id ? `-${state.projectBinding.shot_id}` : "";
  const prefix = isRemoteProvider(providerProfile(state.providerKey))
    ? state.providerKey.toUpperCase()
    : `LOCAL-${state.providerKey.toUpperCase()}`;
  return `${prefix}${shotPart}-${stamp}`;
}

function formRequest() {
  if (isRemoteProvider(providerProfile(state.providerKey))) {
    return {
      provider_key: state.providerKey,
      task_type: state.taskType,
      generation_profile_key: state.generationProfileKey,
      execution_strategy: state.executionStrategy,
      execute: false,
    };
  }
  return {
    provider_key: state.providerKey,
    task_type: state.taskType,
    generation_profile_key: state.generationProfileKey,
    execution_strategy: state.executionStrategy,
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
    preflight_max_swap_used_bytes: Number(elements.preflightSwap.value) * GIB,
    abort_min_available_memory_bytes: Number(elements.abortMemory.value) * GIB,
    max_swap_growth_bytes: Number(elements.swapGrowth.value) * GIB,
    mps_memory_fraction: Number(elements.mpsFraction.value) / 100,
    risk_acknowledged: elements.riskAcknowledged.checked,
    project_binding: state.projectBinding,
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
  const canRegister = result.passed && providerProfile(state.providerKey)?.startable;
  elements.registerButton.disabled = !canRegister;
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
    elements.registerButton.disabled = !(state.preflight?.passed && providerProfile(state.providerKey)?.startable);
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
    <div class="host-foot"><span>内存状态 <strong>${escapeHtml(({healthy: "正常", recovering: "换页恢复中", elevated: "偏紧", critical: "临界"})[memory.pressure] || "未知")}</strong></span><span>生成进程 <strong>${state.overview.active_generation_processes.length}</strong></span></div>`;
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
          <span class="job-item-top"><span>${escapeHtml(job.project_binding?.shot_id || job.provider_key.toUpperCase())}</span>${jobStateBadge(job)}</span>
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
    const profileName = generationProfile(job.generation_profile_key)?.name || job.generation_profile_key;
    const strategyName = executionStrategy(job.execution_strategy)?.name || job.execution_strategy;
    elements.confirmationCard.innerHTML = `${head}
      <div class="confirm-spec">
        <div class="confirm-title"><span>不可变执行标识</span><strong>${escapeHtml(job.execution_id)}</strong></div>
        <div class="confirm-title"><span>作业标识</span><strong>${escapeHtml(job.job_id)}</strong></div>
        <div class="confirm-title"><span>生成档位</span><strong>${escapeHtml(profileName)}</strong></div>
        <div class="confirm-title"><span>执行策略</span><strong>${escapeHtml(strategyName)}</strong></div>
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
    const binding = job.project_binding;
    const metrics = job.evidence_metrics;
    const evidenceControls = metrics ? `
      <div class="confirm-title"><span>候选媒体观察</span><strong>${escapeHtml(metrics.duration_seconds || "—")}s · ${escapeHtml((metrics.resolution || []).join("×") || "未知尺寸")} · ${escapeHtml(metrics.fps || "—")} fps</strong></div>
      <div class="confirm-title"><span>资源峰值</span><strong>进程 ${formatBytes(metrics.process_tree_peak_rss_bytes)} · MPS ${formatBytes(metrics.mps_peak_driver_allocated_bytes)}</strong></div>` : "";
    const selectionControl = job.state === "COMPLETED" && binding ? `
      <p class="confirm-instruction">该输出只是 ${escapeHtml(binding.shot_id)} 的候选。输入镜头标识后，才把它选入当前结构时间线。</p>
      <input class="confirm-input" id="selectionInput" autocomplete="off" placeholder="输入 ${escapeHtml(binding.shot_id)}">
      <button class="primary-button" id="selectCandidateButton" type="button" disabled>选为当前镜头</button>` : "";
    elements.confirmationCard.innerHTML = `${head}
      <div class="confirm-spec">
        <div class="confirm-title"><span>终止原因</span><strong>${escapeHtml(job.terminal_reason || "—")}</strong></div>
        ${evidenceControls}
        <a class="secondary-button observatory-link" href="http://127.0.0.1:4319/?execution_id=${encodeURIComponent(job.execution_id)}" target="_blank" rel="noopener">查看执行证据 ↗</a>
        ${selectionControl}
        <div class="job-events">${events}</div>
      </div>`;
    if (binding && job.state === "COMPLETED") {
      const input = document.querySelector("#selectionInput");
      const button = document.querySelector("#selectCandidateButton");
      input.addEventListener("input", () => { button.disabled = input.value !== binding.shot_id; });
      button.addEventListener("click", () => selectCandidate(job, binding, input.value));
    }
  }
}

async function selectCandidate(job, binding, confirmation) {
  const button = document.querySelector("#selectCandidateButton");
  button.disabled = true;
  button.textContent = "选择中…";
  try {
    await apiPost(`/api/v1/pilots/${encodeURIComponent(binding.project_id)}/shots/${encodeURIComponent(binding.shot_id)}/select`, {
      job_id: job.job_id,
      confirmation_shot_id: confirmation,
    });
    showToast(`${binding.shot_id} 已选择；这不是质量通过。`);
    await refreshOverview();
  } catch (error) {
    showToast(`候选选择失败：${error.message}`);
    button.disabled = false;
    button.textContent = "选为当前镜头";
  }
}

async function assemblePilot(projectId) {
  const confirmation = window.prompt(`输入完整项目标识以组装 30 秒结构样片：\n${projectId}`);
  if (confirmation === null) return;
  try {
    const result = await apiPost(`/api/v1/pilots/${encodeURIComponent(projectId)}/assemble`, {
      confirmation_project_id: confirmation,
    });
    showToast(`结构样片已组装：${result.assembly_id}。`);
    await refreshOverview();
  } catch (error) {
    showToast(`组装失败：${error.message}`);
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
      const defaults = state.overview.catalog.defaults;
      state.providerKey = defaults.provider_key;
      state.taskType = defaults.task_type;
      state.generationProfileKey = defaults.generation_profile_key;
      state.executionStrategy = defaults.execution_strategy;
      renderCatalog();
      elements.seed.value = defaults.seed;
      elements.timeout.value = defaults.timeout_seconds;
      elements.preflightMemory.value = defaults.preflight_min_available_memory_bytes / GIB;
      elements.preflightSwap.value = defaults.preflight_max_swap_used_bytes / GIB;
      elements.abortMemory.value = defaults.abort_min_available_memory_bytes / GIB;
      elements.swapGrowth.value = defaults.max_swap_growth_bytes / GIB;
      elements.mpsFraction.value = defaults.mps_memory_fraction * 100;
      elements.executionId.value = newExecutionId();
    }
    elements.introStatus.innerHTML = '<span>控制服务</span><strong>已连接 · 等待人工操作</strong>';
    elements.freshness.dateTime = state.overview.generated_at;
    elements.freshness.textContent = formatTime(state.overview.generated_at);
    renderHost();
    renderPilotProject();
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
elements.pilotProject.addEventListener("click", (event) => {
  const assemblyButton = event.target.closest("[data-pilot-assemble]");
  if (assemblyButton) {
    assemblePilot(assemblyButton.dataset.pilotAssemble);
    return;
  }
  const button = event.target.closest("[data-pilot-shot]");
  if (button) loadPilotShot(button.dataset.pilotProject, button.dataset.pilotShot);
});
document.addEventListener("visibilitychange", scheduleRefresh);

refreshOverview();
