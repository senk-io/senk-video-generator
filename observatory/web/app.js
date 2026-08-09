"use strict";

const elements = {
  executionSelect: document.querySelector("#executionSelect"),
  refreshControl: document.querySelector("#refreshControl"),
  refreshLabel: document.querySelector("#refreshLabel"),
  clock: document.querySelector("#clock"),
  buildHero: document.querySelector("#buildHero"),
  systemCard: document.querySelector("#systemCard"),
  alertStack: document.querySelector("#alertStack"),
  stageRail: document.querySelector("#stageRail"),
  stageMeta: document.querySelector("#stageMeta"),
  systemLegend: document.querySelector("#systemLegend"),
  systemPeaks: document.querySelector("#systemPeaks"),
  systemChart: document.querySelector("#systemChart"),
  systemChartEmpty: document.querySelector("#systemChartEmpty"),
  mpsLegend: document.querySelector("#mpsLegend"),
  mpsPeaks: document.querySelector("#mpsPeaks"),
  mpsChart: document.querySelector("#mpsChart"),
  mpsChartEmpty: document.querySelector("#mpsChartEmpty"),
  modelGrid: document.querySelector("#modelGrid"),
  outputContent: document.querySelector("#outputContent"),
  evidenceSummary: document.querySelector("#evidenceSummary"),
  evidenceList: document.querySelector("#evidenceList"),
  contextContent: document.querySelector("#contextContent"),
  logSearch: document.querySelector("#logSearch"),
  followLogButton: document.querySelector("#followLogButton"),
  copyLogButton: document.querySelector("#copyLogButton"),
  terminal: document.querySelector("#terminal"),
  logContent: document.querySelector("#logContent"),
  historyMeta: document.querySelector("#historyMeta"),
  historyBody: document.querySelector("#historyBody"),
  boundaryStatement: document.querySelector("#boundaryStatement"),
  freshnessTime: document.querySelector("#freshnessTime"),
  toast: document.querySelector("#toast"),
};

const state = {
  data: null,
  refreshEnabled: true,
  refreshTimer: null,
  requestInFlight: false,
  selectedExecution: new URLSearchParams(window.location.search).get("execution_id"),
  activeTab: "request",
  followLog: true,
  rawLog: "",
  outputKey: null,
  toastTimer: null,
  chartSpecs: new Map(),
};

const statusDefinitions = {
  completed_observation: ["已观察到输出", "success"],
  completed_evidence: ["证据已闭包", "success"],
  active: ["正在构建", "active"],
  failed_observation: ["未形成输出", "danger"],
  interrupted_or_waiting: ["等待或已中断", "warning"],
  unknown: ["状态未知", "neutral"],
};

const phaseLabels = {
  NOT_STARTED: "尚未开始",
  WORKER_STARTED: "工作进程已启动",
  RESOLVING_MODEL_SNAPSHOT: "解析模型快照",
  LOADING_PIPELINE: "装载模型管线",
  TRANSFERRING_TO_MPS: "转移至 Metal",
  RUNNING_INFERENCE: "执行推理",
  EXPORTING_VIDEO: "导出视频",
  WORKER_COMPLETED: "工作进程完成",
  WORKER_FAILED: "工作进程失败",
};

const stageStatusLabels = {
  completed: "已观察",
  active: "进行中",
  failed: "发生异常",
  pending: "等待",
};

const modelStateDefinitions = {
  ready: ["缓存完整", "success"],
  downloading: ["下载中", "active"],
  available_other_revision: ["存在其他修订", "warning"],
  not_downloaded: ["未下载", "neutral"],
};

const evidenceKindLabels = {
  provider_trial: "提供者试运行",
  protected_write: "受保护写入",
  correctness: "正确性证据",
  migration: "迁移证据",
  evidence: "通用证据",
};

const chartColors = {
  mint: "#58f2c2",
  cyan: "#53c9f2",
  blue: "#7b9cff",
  amber: "#f5c76a",
  violet: "#b99cff",
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
  return `${(bytes / 1024 ** index).toFixed(index === 0 ? 0 : precision)} ${units[index]}`;
}

function formatDuration(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  const total = Math.max(0, Number(value));
  if (total < 60) return `${total.toFixed(total < 10 ? 1 : 0)} 秒`;
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const seconds = Math.floor(total % 60);
  if (hours) return `${hours}时 ${String(minutes).padStart(2, "0")}分 ${String(seconds).padStart(2, "0")}秒`;
  return `${minutes}分 ${String(seconds).padStart(2, "0")}秒`;
}

function formatTime(value, includeSeconds = false) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: includeSeconds ? "2-digit" : undefined,
    hour12: false,
  }).format(date);
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "boolean") return value ? "是" : "否";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function truncateHash(value, length = 12) {
  if (!value) return "—";
  const text = String(value);
  return text.length > length ? `${text.slice(0, length)}…` : text;
}

function statusBadge(status) {
  const [label, tone] = statusDefinitions[status] || [status || "未知", "neutral"];
  return `<span class="status-badge tone-${tone}">${escapeHtml(label)}</span>`;
}

function miniBadge(label, tone = "neutral") {
  return `<span class="mini-status tone-${tone}">${escapeHtml(label)}</span>`;
}

function booleanBadge(value, trueLabel = "是", falseLabel = "否") {
  return `<span class="table-badge tone-${value ? "success" : "neutral"}">${value ? trueLabel : falseLabel}</span>`;
}

function renderExecutionOptions(executions, selectedId) {
  const currentOptions = executions.map((item) => item.execution_id).join("|");
  if (elements.executionSelect.dataset.options !== currentOptions) {
    elements.executionSelect.innerHTML = executions.length
      ? executions
          .map((item) => {
            const active = item.active ? " · 运行中" : "";
            return `<option value="${escapeHtml(item.execution_id)}">${escapeHtml(item.execution_id)}${active}</option>`;
          })
          .join("")
      : '<option value="">尚无提供者执行</option>';
    elements.executionSelect.dataset.options = currentOptions;
  }
  elements.executionSelect.value = selectedId || "";
  elements.executionSelect.disabled = executions.length === 0;
}

function renderHero(data) {
  const execution = data.selected_execution;
  if (!execution) {
    elements.buildHero.innerHTML = `
      <div class="hero-head">
        <div><span class="eyebrow">BUILD STATUS</span><h1>等待首次视频构建</h1><p class="hero-subtitle">证据目录中尚无提供者试运行记录</p></div>
        ${statusBadge("unknown")}
      </div>
      <div class="empty-state"><span class="empty-glyph">◇</span><strong>观测服务已就绪</strong><span>启动兼容性试运行后将自动发现执行</span></div>`;
    return;
  }
  const lifecycle = execution.lifecycle;
  const observation = execution.observation;
  const elapsed = observation.elapsed_seconds;
  const currentStage = lifecycle.stages.find((item) => item.id === lifecycle.active_stage);
  const params = execution.request.parameters || {};
  const dimensions = params.width && params.height ? `${params.width} × ${params.height}` : "—";
  elements.buildHero.innerHTML = `
    <div class="hero-head">
      <div>
        <span class="eyebrow">BUILD STATUS · ${escapeHtml(execution.provider_identity || "PROVIDER")}</span>
        <h1>${escapeHtml(phaseLabels[lifecycle.phase] || lifecycle.phase)}</h1>
        <p class="hero-subtitle">${escapeHtml(execution.execution_id)} · ${escapeHtml(execution.model_id || "模型待确认")}</p>
      </div>
      ${statusBadge(lifecycle.state)}
    </div>
    <div class="hero-progress">
      <div class="progress-copy">
        <span>${escapeHtml(currentStage?.label || "阶段已闭合")}</span>
        <strong>${Number(lifecycle.progress_percent).toFixed(0)}%</strong>
      </div>
      <div class="progress-track"><span class="progress-fill" style="width:${Number(lifecycle.progress_percent)}%"></span></div>
      <div class="progress-foot">
        <span>${escapeHtml(currentStage?.description || "已形成当前现实观察")}</span>
        <span>${formatDuration(elapsed)}</span>
      </div>
    </div>
    <div class="hero-facts">
      <div class="hero-fact"><span>精确快照</span><strong title="${escapeHtml(execution.snapshot_revision)}">${escapeHtml(truncateHash(execution.snapshot_revision))}</strong></div>
      <div class="hero-fact"><span>输出规格</span><strong>${escapeHtml(dimensions)} · ${escapeHtml(params.num_frames ?? "—")} 帧</strong></div>
      <div class="hero-fact"><span>设备</span><strong>${escapeHtml((execution.request.device || "—").toUpperCase())}</strong></div>
      <div class="hero-fact"><span>工作区</span><strong>${data.project.worktree_dirty ? "有未提交变更" : "干净"} · ${escapeHtml(data.project.git_head || "—")}</strong></div>
    </div>`;
}

function renderSystem(system, runtime) {
  const memory = system.memory;
  const swap = system.swap;
  const disk = system.disk;
  const ringColor = memory.pressure === "critical" ? "#ff7c82" : memory.pressure === "elevated" ? "#f5c76a" : "#58f2c2";
  const pressureLabels = { healthy: "资源正常", elevated: "内存偏紧", critical: "内存临界" };
  elements.systemCard.innerHTML = `
    <div class="section-heading compact">
      <div><span class="eyebrow">LIVE HOST</span><h2>本机资源</h2></div>
      <span class="source-pill">实时采样</span>
    </div>
    <div class="system-overview">
      <div class="memory-ring" style="--ring-value:${memory.used_percent * 3.6}deg;--ring-color:${ringColor}">
        <div class="memory-ring-copy"><strong>${Number(memory.used_percent).toFixed(0)}%</strong><span>统一内存</span></div>
      </div>
      <div class="resource-list">
        ${resourceLine("可用", memory.available_bytes, memory.total_bytes)}
        ${resourceLine("换页", swap.used_bytes, swap.total_bytes)}
        ${resourceLine("磁盘", disk.used_bytes, disk.total_bytes)}
        ${resourceLine("CPU", system.cpu_percent, 100, "%")}
      </div>
    </div>
    <div class="host-state">
      <span>${escapeHtml(pressureLabels[memory.pressure] || "状态未知")}</span>
      <span><strong>${runtime.process_count}</strong> 个构建进程</span>
      <span><strong>${system.logical_cpu_count || "—"}</strong> 逻辑核心</span>
    </div>`;
}

function resourceLine(label, value, total, unit = "bytes") {
  const denominator = Number(total) || 1;
  const percent = Math.max(0, Math.min(100, Number(value || 0) / denominator * 100));
  const display = unit === "%" ? `${Number(value).toFixed(1)}%` : formatBytes(value);
  return `<div class="resource-line"><span class="resource-label">${escapeHtml(label)}</span><div class="mini-track"><span style="width:${percent}%"></span></div><strong>${escapeHtml(display)}</strong></div>`;
}

function renderAlerts(execution) {
  const warnings = execution?.warnings || [];
  elements.alertStack.innerHTML = warnings
    .map((warning) => `
      <div class="alert-card ${warning.severity === "critical" ? "is-critical" : ""}">
        <span class="alert-icon">!</span>
        <div><strong>${escapeHtml(warning.code)}</strong><p>${escapeHtml(warning.message)}</p></div>
      </div>`)
    .join("");
}

function renderStages(execution) {
  if (!execution) {
    elements.stageRail.innerHTML = '<div class="empty-state"><strong>尚无阶段数据</strong></div>';
    elements.stageMeta.textContent = "等待首次执行";
    return;
  }
  const lifecycle = execution.lifecycle;
  elements.stageMeta.textContent = `${phaseLabels[lifecycle.phase] || lifecycle.phase} · ${lifecycle.progress_percent}%`;
  elements.stageRail.innerHTML = lifecycle.stages
    .map((stage, index) => `
      <article class="stage-item is-${escapeHtml(stage.status)}">
        <span class="stage-index">${String(index + 1).padStart(2, "0")}</span>
        <strong>${escapeHtml(stage.label)}</strong>
        <p>${escapeHtml(stage.description)}</p>
        <span class="stage-state">${escapeHtml(stageStatusLabels[stage.status] || stage.status)}</span>
      </article>`)
    .join("");
}

function renderCharts(execution) {
  const processRows = execution?.process_metrics || [];
  const mpsRows = execution?.mps_metrics || [];
  const resources = execution?.resource_summary || {};
  const systemSeries = [
    { field: "process_tree_rss_bytes", label: "进程树", color: chartColors.mint },
    { field: "system_used_bytes", label: "系统已用", color: chartColors.cyan },
    { field: "swap_used_bytes", label: "交换空间", color: chartColors.amber },
  ];
  const mpsSeries = [
    { field: "mps_current_allocated_bytes", label: "当前分配", color: chartColors.violet },
    { field: "mps_driver_allocated_bytes", label: "驱动分配", color: chartColors.mint },
  ];
  renderLegend(elements.systemLegend, systemSeries);
  renderLegend(elements.mpsLegend, mpsSeries);
  elements.systemPeaks.innerHTML = [
    ["进程峰值", resources.process_tree_peak_rss_bytes],
    ["系统峰值", resources.system_peak_used_bytes],
    ["换页峰值", resources.system_peak_swap_used_bytes],
  ].map(([label, value]) => metricChip(label, formatBytes(value))).join("");
  elements.mpsPeaks.innerHTML = [
    ["当前分配峰值", resources.mps_peak_current_allocated_bytes],
    ["驱动分配峰值", resources.mps_peak_driver_allocated_bytes],
  ].map(([label, value]) => metricChip(label, formatBytes(value))).join("");
  configureChart(elements.systemChart, processRows, systemSeries, elements.systemChartEmpty);
  configureChart(elements.mpsChart, mpsRows, mpsSeries, elements.mpsChartEmpty);
}

function renderLegend(element, series) {
  element.innerHTML = series.map((item) => `<span class="legend-item"><i class="legend-swatch" style="background:${item.color}"></i>${escapeHtml(item.label)}</span>`).join("");
}

function metricChip(label, value) {
  return `<div class="metric-chip"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

function configureChart(canvas, rows, series, emptyElement) {
  state.chartSpecs.set(canvas, { rows, series, hoverIndex: null });
  emptyElement.classList.toggle("is-visible", rows.length === 0);
  canvas.style.visibility = rows.length ? "visible" : "hidden";
  drawChart(canvas);
}

function drawChart(canvas) {
  const spec = state.chartSpecs.get(canvas);
  if (!spec || !spec.rows.length) return;
  const rect = canvas.getBoundingClientRect();
  if (rect.width < 10 || rect.height < 10) return;
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(rect.width * ratio);
  canvas.height = Math.round(rect.height * ratio);
  const context = canvas.getContext("2d");
  context.scale(ratio, ratio);
  const width = rect.width;
  const height = rect.height;
  const plot = { left: 48, right: width - 12, top: 12, bottom: height - 25 };
  const values = spec.rows.flatMap((row) => spec.series.map((item) => Number(row[item.field] || 0)));
  const maxValue = Math.max(...values, 1);
  const maxX = Math.max(...spec.rows.map((row) => Number(row.elapsed_seconds || 0)), 1);
  context.clearRect(0, 0, width, height);
  context.font = '9px "SFMono-Regular", Menlo, monospace';
  context.textBaseline = "middle";
  for (let index = 0; index <= 4; index += 1) {
    const ratioY = index / 4;
    const y = plot.top + (plot.bottom - plot.top) * ratioY;
    const value = maxValue * (1 - ratioY);
    context.beginPath();
    context.strokeStyle = "rgba(184,225,211,0.08)";
    context.lineWidth = 1;
    context.moveTo(plot.left, y);
    context.lineTo(plot.right, y);
    context.stroke();
    context.fillStyle = "#607970";
    context.textAlign = "right";
    context.fillText(formatBytes(value, 0), plot.left - 7, y);
  }
  context.fillStyle = "#607970";
  context.textAlign = "left";
  context.fillText("0s", plot.left, plot.bottom + 16);
  context.textAlign = "right";
  context.fillText(formatAxisDuration(maxX), plot.right, plot.bottom + 16);
  for (const item of spec.series) {
    context.beginPath();
    let hasValue = false;
    spec.rows.forEach((row, index) => {
      const value = Number(row[item.field]);
      if (!Number.isFinite(value)) return;
      const x = plot.left + Number(row.elapsed_seconds || 0) / maxX * (plot.right - plot.left);
      const y = plot.bottom - value / maxValue * (plot.bottom - plot.top);
      if (!hasValue) context.moveTo(x, y);
      else context.lineTo(x, y);
      hasValue = true;
      if (index === spec.rows.length - 1) {
        context.save();
        context.fillStyle = item.color;
        context.shadowColor = item.color;
        context.shadowBlur = 9;
        context.beginPath();
        context.arc(x, y, 2.4, 0, Math.PI * 2);
        context.fill();
        context.restore();
      }
    });
    context.strokeStyle = item.color;
    context.lineWidth = 1.7;
    context.lineJoin = "round";
    context.lineCap = "round";
    context.stroke();
  }
  if (spec.hoverIndex !== null && spec.rows[spec.hoverIndex]) {
    drawChartHover(context, spec, plot, maxX, maxValue, width);
  }
  canvas.dataset.plotLeft = String(plot.left);
  canvas.dataset.plotRight = String(plot.right);
}

function drawChartHover(context, spec, plot, maxX, maxValue, width) {
  const row = spec.rows[spec.hoverIndex];
  const x = plot.left + Number(row.elapsed_seconds || 0) / maxX * (plot.right - plot.left);
  context.save();
  context.strokeStyle = "rgba(238,248,244,0.25)";
  context.setLineDash([3, 4]);
  context.beginPath();
  context.moveTo(x, plot.top);
  context.lineTo(x, plot.bottom);
  context.stroke();
  context.setLineDash([]);
  const boxWidth = 142;
  const boxHeight = 26 + spec.series.length * 17;
  const boxX = Math.min(Math.max(x + 9, plot.left), width - boxWidth - 6);
  const boxY = plot.top + 4;
  context.fillStyle = "rgba(4,9,7,0.94)";
  context.strokeStyle = "rgba(184,225,211,0.18)";
  context.lineWidth = 1;
  context.beginPath();
  context.roundRect(boxX, boxY, boxWidth, boxHeight, 8);
  context.fill();
  context.stroke();
  context.font = '9px "SFMono-Regular", Menlo, monospace';
  context.fillStyle = "#90a9a0";
  context.textAlign = "left";
  context.fillText(formatAxisDuration(Number(row.elapsed_seconds || 0)), boxX + 9, boxY + 14);
  spec.series.forEach((item, index) => {
    const value = Number(row[item.field]);
    context.fillStyle = item.color;
    context.fillText(item.label, boxX + 9, boxY + 33 + index * 17);
    context.fillStyle = "#eef8f4";
    context.textAlign = "right";
    context.fillText(Number.isFinite(value) ? formatBytes(value) : "—", boxX + boxWidth - 9, boxY + 33 + index * 17);
    context.textAlign = "left";
  });
  context.restore();
}

function formatAxisDuration(value) {
  if (value >= 3600) return `${(value / 3600).toFixed(1)}h`;
  if (value >= 60) return `${(value / 60).toFixed(1)}m`;
  return `${value.toFixed(0)}s`;
}

function renderModels(models) {
  elements.modelGrid.innerHTML = models.map((model) => {
    const [label, tone] = modelStateDefinitions[model.state] || [model.state, "neutral"];
    return `
      <article class="model-card">
        <div>
          <div class="model-name"><strong>${escapeHtml(model.name)}</strong>${miniBadge(label, tone)}</div>
          <div class="model-id">${escapeHtml(model.model_id)}</div>
          <div class="revision" title="${escapeHtml(model.observed_revision)}">rev · ${escapeHtml(truncateHash(model.observed_revision, 18))}</div>
        </div>
        <div class="model-facts">
          <div class="model-fact"><span>缓存</span><strong>${formatBytes(model.cache_bytes)}</strong></div>
          <div class="model-fact"><span>快照文件</span><strong>${model.snapshot_file_count}</strong></div>
          <div class="model-fact"><span>未完成</span><strong>${model.incomplete_file_count}</strong></div>
        </div>
      </article>`;
  }).join("");
}

function renderOutput(execution) {
  const output = execution?.output;
  const key = output?.available ? `${execution.execution_id}:${output.video_url}` : "empty";
  if (state.outputKey === key) return;
  state.outputKey = key;
  if (!output?.available) {
    elements.outputContent.innerHTML = '<div class="empty-state"><span class="empty-glyph">◫</span><strong>尚无可预览输出</strong><span>文件出现后将在这里显示</span></div>';
    return;
  }
  const metadata = output.metadata || {};
  const size = Array.isArray(metadata.size) ? metadata.size.join(" × ") : "—";
  elements.outputContent.innerHTML = `
    <div class="output-video-shell">
      <video controls muted preload="metadata" poster="${escapeHtml(output.thumbnail_url || "")}" src="${escapeHtml(output.video_url)}"></video>
    </div>
    <div class="output-meta">
      <div><span>画面</span><strong>${escapeHtml(size)}</strong></div>
      <div><span>帧率</span><strong>${escapeHtml(metadata.fps ?? "—")} fps</strong></div>
      <div><span>帧数</span><strong>${escapeHtml(metadata.decoded_frame_count ?? "—")}</strong></div>
      <div><span>摘要</span><strong title="${escapeHtml(output.sha256)}">${escapeHtml(truncateHash(output.sha256))}</strong></div>
    </div>`;
}

function renderEvidence(execution) {
  if (!execution) {
    elements.evidenceSummary.innerHTML = "";
    elements.evidenceList.innerHTML = '<div class="empty-state"><strong>尚无证据记录</strong></div>';
    return;
  }
  const evidence = execution.evidence;
  elements.evidenceSummary.innerHTML = `
    <div class="summary-stat"><span>证据清单</span><strong>${evidence.manifest_present ? "已形成" : "等待"}</strong></div>
    <div class="summary-stat"><span>实际文件</span><strong>${evidence.actual_file_count}</strong></div>
    <div class="summary-stat"><span>清单声明</span><strong>${evidence.manifest_declared_file_count ?? "—"}</strong></div>`;
  const boundaryRows = [
    ["正式事实", evidence.formal_fact_created, "未创建（符合边界）"],
    ["跨提供方合同", evidence.cross_provider_contract_created, "未创建（符合边界）"],
    ["制度冻结", evidence.institution_freeze_created, "未创建（符合边界）"],
  ].map(([name, created, missingLabel]) => `
    <div class="evidence-file">
      <code>${escapeHtml(name)}</code><span>治理边界</span><span class="file-state ${created ? "tone-success" : "tone-neutral"}">${created ? "已创建" : missingLabel}</span>
    </div>`).join("");
  const files = evidence.files.map((file) => `
    <div class="evidence-file">
      <code title="${escapeHtml(file.name)}">${escapeHtml(file.name)}</code>
      <span>${formatBytes(file.bytes)}</span>
      <span class="file-state ${file.manifested ? "tone-success" : "tone-warning"}">${file.manifested ? "已登记" : "未登记"}</span>
    </div>`).join("");
  elements.evidenceList.innerHTML = boundaryRows + files;
}

function contextItem(label, value, wide = false) {
  return `<dl class="context-item ${wide ? "is-wide" : ""}"><dt>${escapeHtml(label)}</dt><dd title="${escapeHtml(formatValue(value))}">${escapeHtml(formatValue(value))}</dd></dl>`;
}

function renderContext(data) {
  const execution = data.selected_execution;
  if (!execution) {
    elements.contextContent.innerHTML = '<div class="empty-state"><strong>尚无执行上下文</strong></div>';
    return;
  }
  let content = "";
  if (state.activeTab === "request") {
    const request = execution.request;
    const items = [
      contextItem("合同", request.contract_id, true),
      contextItem("创建时间", formatTime(request.created_at, true)),
      contextItem("随机种子", request.seed),
      contextItem("执行设备", request.device),
      contextItem("超时预算", formatDuration(request.timeout_seconds)),
      ...Object.entries(request.parameters || {}).map(([key, value]) => contextItem(key, value)),
      contextItem("固定提示词", request.prompt, true),
    ];
    content = `<div class="context-grid">${items.join("")}</div>`;
  } else if (state.activeTab === "environment") {
    content = `<div class="context-grid">${Object.entries(execution.environment || {}).map(([key, value]) => contextItem(key, value, key === "processor" || key === "git_head")).join("")}</div>`;
  } else {
    const relevant = data.runtime.processes.filter((item) => item.execution_id === execution.execution_id);
    content = relevant.length
      ? `<div class="context-grid">${relevant.flatMap((process) => [
          contextItem("PID", process.pid),
          contextItem("角色", process.role),
          contextItem("状态", process.status),
          contextItem("常驻内存", formatBytes(process.rss_bytes)),
          contextItem("运行时间", formatDuration(process.running_seconds)),
        ]).join("")}</div>`
      : '<div class="empty-state"><strong>当前没有对应运行进程</strong><span>历史执行仍可从证据包查看</span></div>';
  }
  elements.contextContent.innerHTML = content;
}

function renderLog(execution) {
  state.rawLog = execution?.log_tail || "";
  applyLogFilter();
}

function applyLogFilter() {
  const query = elements.logSearch.value.trim().toLocaleLowerCase("zh-CN");
  const text = query
    ? state.rawLog.split("\n").filter((line) => line.toLocaleLowerCase("zh-CN").includes(query)).join("\n")
    : state.rawLog;
  const next = text || (query ? "没有匹配的日志行。" : "当前执行尚未产生运行日志。 ");
  const changed = elements.logContent.textContent !== next;
  elements.logContent.textContent = next;
  if (changed && state.followLog) {
    requestAnimationFrame(() => {
      elements.logContent.scrollTop = elements.logContent.scrollHeight;
    });
  }
}

function mapEvidenceResult(value) {
  if (!value) return ["摘要不可用", "neutral"];
  if (value === "OBSERVED_OUTPUT_AVAILABLE") return ["已观察到输出", "success"];
  if (value === "OBSERVED_EXECUTION_WITHOUT_OUTPUT") return ["未观察到输出", "danger"];
  if (String(value).startsWith("PASS_AS_NON_AUTHORITATIVE")) return ["非权威证据已记录", "success"];
  if (value === "SUMMARY_UNAVAILABLE") return ["摘要不可用", "warning"];
  return [String(value), "neutral"];
}

function renderHistory(packages) {
  elements.historyMeta.textContent = `${packages.length} 个证据包`;
  elements.historyBody.innerHTML = packages.map((item) => {
    const [resultLabel, tone] = mapEvidenceResult(item.result);
    return `
      <tr data-execution="${item.kind === "provider_trial" ? escapeHtml(item.execution_id) : ""}">
        <td><code>${escapeHtml(item.execution_id)}</code></td>
        <td>${escapeHtml(evidenceKindLabels[item.kind] || item.kind)}</td>
        <td>${miniBadge(resultLabel, tone)}</td>
        <td>${booleanBadge(item.manifest_present, `${item.declared_file_count ?? "—"} 项`, "缺失")}</td>
        <td>${booleanBadge(item.formal_fact_created, "已创建", "未创建")}</td>
        <td>${booleanBadge(item.institution_freeze_created, "已创建", "未创建")}</td>
        <td>${escapeHtml(formatTime(item.modified_at, true))}</td>
      </tr>`;
  }).join("");
}

function renderFooter(data) {
  elements.boundaryStatement.textContent = data.governance_boundary.statement;
  elements.freshnessTime.dateTime = data.generated_at;
  elements.freshnessTime.textContent = formatTime(data.generated_at, true);
}

function renderDashboard(data) {
  state.data = data;
  const selectedId = data.selected_execution?.execution_id || null;
  renderExecutionOptions(data.executions, selectedId);
  renderHero(data);
  renderSystem(data.system, data.runtime);
  renderAlerts(data.selected_execution);
  renderStages(data.selected_execution);
  renderCharts(data.selected_execution);
  renderModels(data.models);
  renderOutput(data.selected_execution);
  renderEvidence(data.selected_execution);
  renderContext(data);
  renderLog(data.selected_execution);
  renderHistory(data.evidence_packages);
  renderFooter(data);
}

async function fetchDashboard() {
  if (state.requestInFlight) return;
  state.requestInFlight = true;
  const query = state.selectedExecution ? `?execution_id=${encodeURIComponent(state.selectedExecution)}` : "";
  try {
    const response = await fetch(`/api/v1/dashboard${query}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    renderDashboard(data);
    elements.refreshControl.classList.add("is-live");
    elements.refreshLabel.textContent = state.refreshEnabled ? "实时刷新" : "已暂停";
  } catch (error) {
    elements.refreshControl.classList.remove("is-live");
    elements.refreshLabel.textContent = "连接中断";
    showToast(`无法读取本地观测服务：${error.message}`);
  } finally {
    state.requestInFlight = false;
    scheduleRefresh();
  }
}

function scheduleRefresh() {
  window.clearTimeout(state.refreshTimer);
  if (!state.refreshEnabled) return;
  const delay = document.hidden ? 5000 : (state.data?.refresh_after_ms || 1000);
  state.refreshTimer = window.setTimeout(fetchDashboard, delay);
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add("is-visible");
  window.clearTimeout(state.toastTimer);
  state.toastTimer = window.setTimeout(() => elements.toast.classList.remove("is-visible"), 2600);
}

function updateClock() {
  elements.clock.textContent = new Intl.DateTimeFormat("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date());
}

function setupChartInteractions(canvas) {
  canvas.addEventListener("pointermove", (event) => {
    const spec = state.chartSpecs.get(canvas);
    if (!spec?.rows.length) return;
    const rect = canvas.getBoundingClientRect();
    const left = Number(canvas.dataset.plotLeft || 48);
    const right = Number(canvas.dataset.plotRight || rect.width - 12);
    const x = Math.max(left, Math.min(right, event.clientX - rect.left));
    const ratio = (x - left) / Math.max(1, right - left);
    spec.hoverIndex = Math.max(0, Math.min(spec.rows.length - 1, Math.round(ratio * (spec.rows.length - 1))));
    drawChart(canvas);
  });
  canvas.addEventListener("pointerleave", () => {
    const spec = state.chartSpecs.get(canvas);
    if (!spec) return;
    spec.hoverIndex = null;
    drawChart(canvas);
  });
}

elements.executionSelect.addEventListener("change", () => {
  state.selectedExecution = elements.executionSelect.value || null;
  const url = new URL(window.location.href);
  if (state.selectedExecution) url.searchParams.set("execution_id", state.selectedExecution);
  else url.searchParams.delete("execution_id");
  window.history.replaceState({}, "", url);
  state.outputKey = null;
  fetchDashboard();
});

elements.refreshControl.addEventListener("click", () => {
  state.refreshEnabled = !state.refreshEnabled;
  elements.refreshControl.setAttribute("aria-pressed", String(state.refreshEnabled));
  elements.refreshControl.classList.toggle("is-live", state.refreshEnabled);
  elements.refreshLabel.textContent = state.refreshEnabled ? "实时刷新" : "已暂停";
  if (state.refreshEnabled) fetchDashboard();
  else window.clearTimeout(state.refreshTimer);
});

document.querySelectorAll("[data-tab]").forEach((button) => {
  button.addEventListener("click", () => {
    state.activeTab = button.dataset.tab;
    document.querySelectorAll("[data-tab]").forEach((item) => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-selected", String(active));
    });
    if (state.data) renderContext(state.data);
  });
});

elements.logSearch.addEventListener("input", applyLogFilter);

elements.followLogButton.addEventListener("click", () => {
  state.followLog = !state.followLog;
  elements.followLogButton.setAttribute("aria-pressed", String(state.followLog));
  elements.followLogButton.textContent = state.followLog ? "跟随末尾" : "自由滚动";
  if (state.followLog) applyLogFilter();
});

elements.copyLogButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(elements.logContent.textContent || "");
    showToast("日志已复制到剪贴板");
  } catch {
    showToast("浏览器未允许复制，请手动选择日志");
  }
});

elements.historyBody.addEventListener("click", (event) => {
  const row = event.target.closest("tr[data-execution]");
  if (!row?.dataset.execution) return;
  state.selectedExecution = row.dataset.execution;
  elements.executionSelect.value = state.selectedExecution;
  state.outputKey = null;
  fetchDashboard();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

document.addEventListener("visibilitychange", scheduleRefresh);

const resizeObserver = new ResizeObserver(() => {
  drawChart(elements.systemChart);
  drawChart(elements.mpsChart);
});
resizeObserver.observe(elements.systemChart);
resizeObserver.observe(elements.mpsChart);
setupChartInteractions(elements.systemChart);
setupChartInteractions(elements.mpsChart);

updateClock();
window.setInterval(updateClock, 1000);
fetchDashboard();
