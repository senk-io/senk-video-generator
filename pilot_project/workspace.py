"""样片候选选择与可追溯结构组装。"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import subprocess
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

import imageio.v2 as imageio
import imageio_ffmpeg

from pilot_project.catalog import PilotCatalog, canonical_sha256


class PilotOperationError(ValueError):
    def __init__(self, code: str, message: str, details: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def file_sha256(file_path: Path) -> str:
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_write_json(file_path: Path, value: dict[str, Any]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = file_path.with_suffix(file_path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(file_path)


class PilotWorkspace:
    """保留选择历史，并只从当前人工选择形成结构样片。"""

    def __init__(
        self,
        catalog: PilotCatalog,
        state_root: Path,
        evidence_root: Path,
        ffmpeg_executable: str | None = None,
    ) -> None:
        self.catalog = catalog
        self.state_root = state_root.resolve()
        self.evidence_root = evidence_root.resolve()
        self.ffmpeg_executable = ffmpeg_executable or imageio_ffmpeg.get_ffmpeg_exe()

    def overview(self, jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        projects = self.catalog.overview(jobs)
        for project in projects:
            selections = self.current_selections(project["project_id"])
            selected_count = 0
            for shot in project["shots"]:
                selection = selections.get(shot["shot_id"])
                shot["selection"] = deepcopy(selection)
                if selection:
                    shot["state"] = "SELECTED"
                    selected_count += 1
            project["progress"]["selected_shot_count"] = selected_count
            assembly = self._latest_assembly(project["project_id"])
            project["progress"]["assembled"] = assembly is not None
            project["latest_assembly"] = assembly
        return projects

    def select_candidate(
        self,
        project_id: str,
        shot_id: str,
        job: dict[str, Any],
        confirmation_shot_id: str,
    ) -> dict[str, Any]:
        project = self.catalog.project(project_id)
        shot = next((item for item in project["shots"] if item["shot_id"] == shot_id), None)
        if shot is None:
            raise PilotOperationError("SHOT_NOT_FOUND", "找不到对应镜头。")
        if confirmation_shot_id != shot_id:
            raise PilotOperationError("SELECTION_CONFIRMATION_MISMATCH", "必须完整输入镜头标识确认选择。")
        binding = job.get("project_binding") or {}
        if binding.get("project_id") != project_id or binding.get("shot_id") != shot_id:
            raise PilotOperationError("CANDIDATE_BINDING_MISMATCH", "作业没有绑定到当前镜头。")
        if job.get("state") != "COMPLETED":
            raise PilotOperationError("CANDIDATE_NOT_COMPLETE", "只有已形成输出的作业可以被选择。")
        evidence = self._validated_candidate_evidence(job)
        event = self._append_selection_event(
            project_id,
            "CANDIDATE_SELECTED",
            {
                "shot_id": shot_id,
                "job_id": job["job_id"],
                "execution_id": job["execution_id"],
                "output_sha256": evidence["output_sha256"],
                "source_duration_seconds": evidence["duration_seconds"],
                "target_duration_seconds": shot["duration_seconds"],
                "selected_by": "LOCAL_HUMAN_OPERATOR",
                "quality_acceptance_created": False,
                "publication_authority_created": False,
            },
        )
        return {
            "project_id": project_id,
            "shot_id": shot_id,
            "selection": event["payload"],
            "notice": "候选已进入当前结构时间线；这不是质量通过或发布决定。",
        }

    def current_selections(self, project_id: str) -> dict[str, dict[str, Any]]:
        selections: dict[str, dict[str, Any]] = {}
        for event in self._read_selection_events(project_id):
            payload = event["payload"]
            if event["event_type"] == "CANDIDATE_SELECTED":
                selections[payload["shot_id"]] = deepcopy(payload)
            elif event["event_type"] == "SELECTION_REVOKED":
                selections.pop(payload["shot_id"], None)
        return selections

    def assemble(
        self,
        project_id: str,
        confirmation_project_id: str,
        job_lookup: Callable[[str], dict[str, Any]],
    ) -> dict[str, Any]:
        project = self.catalog.project(project_id)
        if confirmation_project_id != project_id:
            raise PilotOperationError("ASSEMBLY_CONFIRMATION_MISMATCH", "必须完整输入项目标识确认组装。")
        selections = self.current_selections(project_id)
        missing = [shot["shot_id"] for shot in project["shots"] if shot["shot_id"] not in selections]
        if missing:
            raise PilotOperationError("SELECTIONS_INCOMPLETE", "六个镜头必须全部完成人工选择后才能组装。", {"missing": missing})

        assembly_id = datetime.now(UTC).strftime("ASSEMBLY-%Y%m%dT%H%M%SZ-") + secrets.token_hex(3).upper()
        assembly_root = self.state_root / "pilots" / project_id / "assemblies" / assembly_id
        segments_root = assembly_root / "segments"
        segments_root.mkdir(parents=True)
        segment_records = []
        for shot in project["shots"]:
            selection = selections[shot["shot_id"]]
            job = job_lookup(selection["job_id"])
            evidence = self._validated_candidate_evidence(job)
            if evidence["output_sha256"] != selection["output_sha256"]:
                raise PilotOperationError("SELECTED_OUTPUT_DRIFT", "已选候选的文件摘要已经变化。")
            segment_path = segments_root / f"{shot['shot_id']}.mp4"
            self._normalize_segment(evidence["output_path"], segment_path, shot, project["target"])
            segment_records.append(
                {
                    "shot_id": shot["shot_id"],
                    "job_id": job["job_id"],
                    "execution_id": job["execution_id"],
                    "source_sha256": evidence["output_sha256"],
                    "source_duration_seconds": evidence["duration_seconds"],
                    "target_duration_seconds": shot["duration_seconds"],
                    "duration_adaptation": "LOOP_THEN_TRIM" if evidence["duration_seconds"] < shot["duration_seconds"] else "TRIM",
                    "resolution_adaptation": "SCALE_AND_PAD",
                    "segment_sha256": file_sha256(segment_path),
                }
            )

        concat_path = assembly_root / "concat.txt"
        concat_path.write_text(
            "".join(f"file '{(segments_root / f'{shot['shot_id']}.mp4').as_posix()}'\n" for shot in project["shots"]),
            encoding="utf-8",
        )
        output_path = assembly_root / "output.mp4"
        self._run_ffmpeg(
            ["-f", "concat", "-safe", "0", "-i", str(concat_path), "-c", "copy", "-movflags", "+faststart", str(output_path)]
        )
        metadata = imageio.get_reader(output_path).get_meta_data()
        duration = float(metadata.get("duration", 0.0))
        manifest = {
            "schema_version": "pilot-assembly.v1",
            "assembly_id": assembly_id,
            "project_id": project_id,
            "project_contract_sha256": project["contract_sha256"],
            "created_at": utc_now(),
            "output_path": str(output_path),
            "output_sha256": file_sha256(output_path),
            "output_bytes": output_path.stat().st_size,
            "observed_duration_seconds": duration,
            "target_duration_seconds": project["target"]["duration_seconds"],
            "segments": segment_records,
            "quality_acceptance_created": False,
            "publication_authority_created": False,
            "observation": "STRUCTURAL_PREVIEW_ASSEMBLED",
            "warning": "短候选可能被循环，低分辨率候选可能被升采样；结构完成不等于清晰度通过。",
        }
        atomic_write_json(assembly_root / "manifest.json", manifest)
        atomic_write_json(self.state_root / "pilots" / project_id / "latest_assembly.json", manifest)
        return manifest

    def _validated_candidate_evidence(self, job: dict[str, Any]) -> dict[str, Any]:
        execution_id = str(job.get("execution_id", ""))
        evidence_root = (self.evidence_root / execution_id).resolve()
        if not evidence_root.is_relative_to(self.evidence_root):
            raise PilotOperationError("EVIDENCE_PATH_INVALID", "候选证据路径无效。")
        try:
            summary = json.loads((evidence_root / "summary.json").read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PilotOperationError("CANDIDATE_EVIDENCE_MISSING", "候选证据摘要缺失或损坏。") from exc
        output_path = evidence_root / "output.mp4"
        if summary.get("observation") != "OBSERVED_OUTPUT_AVAILABLE" or not output_path.is_file():
            raise PilotOperationError("CANDIDATE_OUTPUT_MISSING", "候选没有可用输出文件。")
        digest = file_sha256(output_path)
        if summary.get("output_sha256") != digest:
            raise PilotOperationError("CANDIDATE_OUTPUT_DIGEST_MISMATCH", "候选输出摘要不匹配。")
        metadata = summary.get("output_metadata") or {}
        duration = metadata.get("duration_seconds")
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise PilotOperationError("CANDIDATE_DURATION_INVALID", "候选时长观察无效。")
        return {"output_path": output_path, "output_sha256": digest, "duration_seconds": float(duration)}

    def _selection_events_path(self, project_id: str) -> Path:
        self.catalog.project(project_id)
        return self.state_root / "pilots" / project_id / "selections.jsonl"

    def _append_selection_event(self, project_id: str, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        events = self._read_selection_events(project_id)
        event = {
            "sequence": len(events) + 1,
            "event_type": event_type,
            "recorded_at": utc_now(),
            "previous_record_sha256": events[-1]["record_sha256"] if events else None,
            "payload": payload,
        }
        event["record_sha256"] = canonical_sha256(event)
        events_path = self._selection_events_path(project_id)
        events_path.parent.mkdir(parents=True, exist_ok=True)
        with events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return event

    def _read_selection_events(self, project_id: str) -> list[dict[str, Any]]:
        events_path = self._selection_events_path(project_id)
        if not events_path.is_file():
            return []
        values = []
        previous = None
        try:
            for sequence, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), start=1):
                value = json.loads(line)
                digest = value.get("record_sha256")
                unsigned = {key: item for key, item in value.items() if key != "record_sha256"}
                if (
                    value.get("sequence") != sequence
                    or value.get("previous_record_sha256") != previous
                    or not isinstance(digest, str)
                    or not secrets.compare_digest(digest, canonical_sha256(unsigned))
                ):
                    raise ValueError("selection event chain mismatch")
                values.append(value)
                previous = digest
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise PilotOperationError("SELECTION_CHAIN_INVALID", "候选选择历史摘要链无效。") from exc
        return values

    def _normalize_segment(
        self,
        source_path: Path,
        segment_path: Path,
        shot: dict[str, Any],
        target: dict[str, Any],
    ) -> None:
        width, height = target["resolution"]
        filters = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"fps={target['fps']},format=yuv420p"
        )
        self._run_ffmpeg(
            [
                "-stream_loop", "-1", "-i", str(source_path), "-t", str(shot["duration_seconds"]),
                "-vf", filters, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-movflags", "+faststart", str(segment_path),
            ]
        )

    def _run_ffmpeg(self, arguments: list[str]) -> None:
        result = subprocess.run(
            [self.ffmpeg_executable, "-hide_banner", "-loglevel", "error", "-y", *arguments],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        if result.returncode != 0:
            raise PilotOperationError(
                "ASSEMBLY_FFMPEG_FAILED",
                "视频结构组装失败。",
                {"return_code": result.returncode, "stderr": result.stderr[-2000:]},
            )

    def _latest_assembly(self, project_id: str) -> dict[str, Any] | None:
        latest_path = self.state_root / "pilots" / project_id / "latest_assembly.json"
        try:
            value = json.loads(latest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None
