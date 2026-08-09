"""验证模型无关的样片合同，并投影逐镜头候选状态。"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any


PROJECT_ID_PATTERN = re.compile(r"PILOT-[A-Z0-9][A-Z0-9-]{2,95}")
SHOT_ID_PATTERN = re.compile(r"SHOT-[0-9]{3}")
PROJECT_SCHEMA_VERSION = "pilot-project.v1"
REQUIRED_EXPECTATION_FIELDS = frozenset(
    {"owner", "purpose", "success", "observable", "evidence", "acceptable_gap", "authority"}
)


class PilotContractError(ValueError):
    """样片合同或作业绑定不满足固定约束。"""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class PilotCatalog:
    """从受版本控制的项目目录读取合同，不创建创意接受决定。"""

    def __init__(self, projects_root: Path) -> None:
        self.projects_root = projects_root.resolve()
        self._projects = self._load_projects()

    def _load_projects(self) -> dict[str, dict[str, Any]]:
        projects: dict[str, dict[str, Any]] = {}
        if not self.projects_root.is_dir():
            return projects
        for contract_path in sorted(self.projects_root.glob("*.json")):
            try:
                value = json.loads(contract_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise PilotContractError("PROJECT_FILE_INVALID", f"项目文件无法读取：{contract_path.name}") from exc
            normalized = validate_project(value)
            project_id = normalized["project_id"]
            if project_id in projects:
                raise PilotContractError("DUPLICATE_PROJECT_ID", f"项目标识重复：{project_id}")
            normalized["contract_sha256"] = canonical_sha256(normalized)
            projects[project_id] = normalized
        return projects

    def project(self, project_id: str) -> dict[str, Any]:
        project = self._projects.get(project_id)
        if project is None:
            raise PilotContractError("PROJECT_NOT_FOUND", "找不到对应样片项目。")
        return deepcopy(project)

    def validate_binding(self, request: dict[str, Any]) -> tuple[bool, str, dict[str, Any] | None]:
        binding = request.get("project_binding")
        if binding is None:
            return True, "当前作业未绑定样片镜头。", None
        if not isinstance(binding, dict):
            return False, "样片绑定必须是对象。", None
        project_id = str(binding.get("project_id", ""))
        shot_id = str(binding.get("shot_id", ""))
        project = self._projects.get(project_id)
        if project is None:
            return False, "样片项目不存在。", None
        shot = next((item for item in project["shots"] if item["shot_id"] == shot_id), None)
        if shot is None:
            return False, "镜头不属于该样片项目。", None
        if binding.get("project_contract_sha256") != project["contract_sha256"]:
            return False, "样片合同摘要已经变化，请重新载入镜头。", None
        if binding.get("prompt_sha256") != canonical_sha256(shot["generation_prompt"]):
            return False, "镜头提示词摘要与项目合同不一致。", None
        if request.get("prompt") != shot["generation_prompt"]:
            return False, "已绑定作业的提示词必须与镜头合同完全一致。", None
        return True, "作业已绑定到固定镜头合同。", deepcopy(shot)

    def overview(self, jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        values: list[dict[str, Any]] = []
        for project in self._projects.values():
            shots = []
            completed_count = 0
            for shot in project["shots"]:
                candidates = [
                    job
                    for job in jobs
                    if (job.get("project_binding") or {}).get("project_id") == project["project_id"]
                    and (job.get("project_binding") or {}).get("shot_id") == shot["shot_id"]
                ]
                completed = [job for job in candidates if job.get("state") == "COMPLETED"]
                active = [
                    job
                    for job in candidates
                    if job.get("state") in {"REGISTERED", "STARTING", "RUNNING", "STOP_REQUESTED"}
                ]
                if completed:
                    shot_state = "CANDIDATES_READY"
                    completed_count += 1
                elif active:
                    shot_state = "GENERATING"
                elif candidates:
                    shot_state = "RETRY_AVAILABLE"
                else:
                    shot_state = "PLANNED"
                shots.append(
                    {
                        **deepcopy(shot),
                        "prompt_sha256": canonical_sha256(shot["generation_prompt"]),
                        "state": shot_state,
                        "candidate_count": len(candidates),
                        "completed_candidate_count": len(completed),
                        "latest_job_id": candidates[0]["job_id"] if candidates else None,
                        "candidate_observations": [
                            candidate_observation(job, shot, project["target"])
                            for job in completed
                        ],
                    }
                )
            values.append(
                {
                    **deepcopy(project),
                    "shots": shots,
                    "progress": {
                        "planned_shot_count": len(shots),
                        "shots_with_completed_candidates": completed_count,
                        "selected_shot_count": 0,
                        "assembled": False,
                    },
                    "authority_notice": "生成作业只形成候选；当前项目尚无创意选择和发布授权接口。",
                }
            )
        return values


def validate_project(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PilotContractError("PROJECT_NOT_OBJECT", "样片合同必须是对象。")
    if value.get("schema_version") != PROJECT_SCHEMA_VERSION:
        raise PilotContractError("PROJECT_SCHEMA_UNSUPPORTED", "样片合同版本不受支持。")
    project_id = str(value.get("project_id", ""))
    if not PROJECT_ID_PATTERN.fullmatch(project_id):
        raise PilotContractError("PROJECT_ID_INVALID", "样片项目标识无效。")
    if value.get("status") != "DRAFT_NON_AUTHORITATIVE":
        raise PilotContractError("PROJECT_STATUS_INVALID", "首阶段样片只能登记为非权威草案。")

    target = value.get("target")
    if not isinstance(target, dict) or target.get("duration_seconds") != 30:
        raise PilotContractError("PROJECT_DURATION_INVALID", "当前阶段必须固定为 30 秒。")
    if target.get("aspect_ratio") != "16:9":
        raise PilotContractError("PROJECT_ASPECT_INVALID", "当前样片必须使用 16:9。")
    resolution = target.get("resolution")
    if (
        not isinstance(resolution, list)
        or len(resolution) != 2
        or not all(isinstance(item, int) and item > 0 for item in resolution)
    ):
        raise PilotContractError("PROJECT_RESOLUTION_INVALID", "目标分辨率无效。")
    if not isinstance(target.get("fps"), int) or target["fps"] <= 0:
        raise PilotContractError("PROJECT_FPS_INVALID", "目标帧率无效。")

    expectations = value.get("expectations")
    if not isinstance(expectations, list) or not expectations:
        raise PilotContractError("EXPECTATIONS_REQUIRED", "样片必须声明可核对的预期。")
    expectation_ids: set[str] = set()
    for expectation in expectations:
        if not isinstance(expectation, dict) or not REQUIRED_EXPECTATION_FIELDS.issubset(expectation):
            raise PilotContractError("EXPECTATION_INCOMPLETE", "每项预期必须声明责任、证据和权威边界。")
        expectation_id = str(expectation.get("expectation_id", ""))
        if not expectation_id or expectation_id in expectation_ids:
            raise PilotContractError("EXPECTATION_ID_INVALID", "预期标识缺失或重复。")
        expectation_ids.add(expectation_id)

    shots = value.get("shots")
    if not isinstance(shots, list) or len(shots) != 6:
        raise PilotContractError("SHOT_COUNT_INVALID", "30 秒首阶段必须拆分为六个镜头。")
    shot_ids: set[str] = set()
    duration_sum = 0
    for ordinal, shot in enumerate(shots, start=1):
        if not isinstance(shot, dict):
            raise PilotContractError("SHOT_INVALID", "镜头必须是对象。")
        shot_id = str(shot.get("shot_id", ""))
        if not SHOT_ID_PATTERN.fullmatch(shot_id) or shot_id in shot_ids:
            raise PilotContractError("SHOT_ID_INVALID", "镜头标识无效或重复。")
        if shot.get("ordinal") != ordinal:
            raise PilotContractError("SHOT_ORDER_INVALID", "镜头顺序必须连续且不可歧义。")
        duration = shot.get("duration_seconds")
        if not isinstance(duration, int) or duration <= 0:
            raise PilotContractError("SHOT_DURATION_INVALID", "镜头时长必须是正整数秒。")
        for field in ("title", "purpose", "generation_prompt", "continuity_in", "continuity_out"):
            if not isinstance(shot.get(field), str) or not shot[field].strip():
                raise PilotContractError("SHOT_FIELD_REQUIRED", f"镜头字段缺失：{field}")
        checks = shot.get("observable_checks")
        if not isinstance(checks, list) or not checks or not all(isinstance(item, str) and item for item in checks):
            raise PilotContractError("SHOT_CHECKS_REQUIRED", "每个镜头必须声明可观察检查。")
        shot_ids.add(shot_id)
        duration_sum += duration
    if duration_sum != target["duration_seconds"]:
        raise PilotContractError("SHOT_DURATION_SUM_MISMATCH", "镜头总时长必须精确等于项目时长。")
    return deepcopy(value)


def candidate_observation(
    job: dict[str, Any],
    shot: dict[str, Any],
    target: dict[str, Any],
) -> dict[str, Any]:
    metrics = job.get("evidence_metrics") or {}
    duration = metrics.get("duration_seconds")
    resolution = metrics.get("resolution")
    duration_coverage = (
        round(float(duration) / shot["duration_seconds"], 3)
        if isinstance(duration, (int, float)) and duration > 0
        else None
    )
    resolution_meets_target = (
        isinstance(resolution, list)
        and len(resolution) == 2
        and resolution[0] >= target["resolution"][0]
        and resolution[1] >= target["resolution"][1]
    )
    return {
        "job_id": job.get("job_id"),
        "execution_id": job.get("execution_id"),
        "source_duration_seconds": duration,
        "target_duration_seconds": shot["duration_seconds"],
        "duration_coverage": duration_coverage,
        "source_resolution": resolution,
        "target_resolution": target["resolution"],
        "resolution_meets_target": resolution_meets_target,
        "elapsed_seconds": metrics.get("elapsed_seconds"),
        "process_tree_peak_rss_bytes": metrics.get("process_tree_peak_rss_bytes"),
        "mps_peak_driver_allocated_bytes": metrics.get("mps_peak_driver_allocated_bytes"),
        "cash_cost_observation": metrics.get("cash_cost_observation"),
        "creative_review_required": True,
        "quality_acceptance_created": False,
    }
