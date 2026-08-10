from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import imageio_ffmpeg

from pilot_project.catalog import PilotCatalog, PilotContractError, canonical_sha256, validate_project
from pilot_project.workspace import PilotOperationError, PilotWorkspace, file_sha256


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_PATH = REPO_ROOT / "projects" / "PILOT-RED-BOAT-30S-001.json"


class PilotProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.project = json.loads(PROJECT_PATH.read_text(encoding="utf-8"))

    def test_committed_project_is_exactly_thirty_seconds_and_six_shots(self) -> None:
        normalized = validate_project(self.project)

        self.assertEqual(normalized["target"]["duration_seconds"], 30)
        self.assertEqual(len(normalized["shots"]), 6)
        self.assertEqual(sum(item["duration_seconds"] for item in normalized["shots"]), 30)
        self.assertEqual([item["ordinal"] for item in normalized["shots"]], list(range(1, 7)))
        self.assertTrue(all("folded origami" in item["generation_prompt"] for item in normalized["shots"]))

    def test_duration_drift_is_fail_closed(self) -> None:
        invalid = deepcopy(self.project)
        invalid["shots"][0]["duration_seconds"] = 4

        with self.assertRaisesRegex(PilotContractError, "镜头总时长"):
            validate_project(invalid)

    def test_project_binding_requires_exact_contract_and_prompt(self) -> None:
        catalog = PilotCatalog(PROJECT_PATH.parent)
        project = catalog.project(self.project["project_id"])
        shot = project["shots"][0]
        request = {
            "prompt": shot["generation_prompt"],
            "project_binding": {
                "project_id": project["project_id"],
                "shot_id": shot["shot_id"],
                "project_contract_sha256": project["contract_sha256"],
                "prompt_sha256": canonical_sha256(shot["generation_prompt"]),
            },
        }

        passed, _, bound_shot = catalog.validate_binding(request)
        self.assertTrue(passed)
        self.assertEqual(bound_shot["shot_id"], "SHOT-001")

        request["prompt"] = "drifted prompt"
        passed, message, _ = catalog.validate_binding(request)
        self.assertFalse(passed)
        self.assertIn("完全一致", message)

    def test_overview_projects_jobs_without_creating_selection(self) -> None:
        catalog = PilotCatalog(PROJECT_PATH.parent)
        project = catalog.project(self.project["project_id"])
        shot = project["shots"][0]
        jobs = [
            {
                "job_id": "JOB-20260810T000000Z-A1B2C3D4",
                "state": "COMPLETED",
                "project_binding": {
                    "project_id": project["project_id"],
                    "shot_id": shot["shot_id"],
                },
            }
        ]

        overview = catalog.overview(jobs)[0]
        self.assertEqual(overview["shots"][0]["state"], "CANDIDATES_READY")
        self.assertEqual(overview["progress"]["shots_with_completed_candidates"], 1)
        self.assertEqual(overview["progress"]["selected_shot_count"], 0)
        self.assertFalse(overview["progress"]["assembled"])

    def test_six_explicit_selections_form_a_thirty_second_structural_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_root = Path(temporary_name)
            projects_root = temporary_root / "projects"
            state_root = temporary_root / "state"
            evidence_root = temporary_root / "evidence"
            projects_root.mkdir()
            evidence_root.mkdir()
            project = deepcopy(self.project)
            project["target"]["resolution"] = [320, 180]
            (projects_root / "project.json").write_text(
                json.dumps(project, ensure_ascii=False),
                encoding="utf-8",
            )
            source = temporary_root / "source.mp4"
            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
            subprocess.run(
                [
                    ffmpeg,
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "color=c=red:s=64x36:d=1:r=8",
                    "-pix_fmt",
                    "yuv420p",
                    str(source),
                ],
                check=True,
            )
            catalog = PilotCatalog(projects_root)
            workspace = PilotWorkspace(catalog, state_root, evidence_root, ffmpeg)
            jobs = {}
            for ordinal, shot in enumerate(project["shots"], start=1):
                execution_id = f"PILOT-TEST-{ordinal:03d}"
                job_id = f"JOB-20260810T0000{ordinal:02d}Z-A1B2C3D{ordinal}"
                evidence_dir = evidence_root / execution_id
                evidence_dir.mkdir()
                output = evidence_dir / "output.mp4"
                output.write_bytes(source.read_bytes())
                summary = {
                    "observation": "OBSERVED_OUTPUT_AVAILABLE",
                    "output_sha256": file_sha256(output),
                    "output_metadata": {"duration_seconds": 1.0},
                }
                (evidence_dir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
                job = {
                    "job_id": job_id,
                    "execution_id": execution_id,
                    "state": "COMPLETED",
                    "project_binding": {
                        "project_id": project["project_id"],
                        "shot_id": shot["shot_id"],
                    },
                }
                jobs[job_id] = job
                workspace.select_candidate(
                    project["project_id"],
                    shot["shot_id"],
                    job,
                    shot["shot_id"],
                )

            manifest = workspace.assemble(project["project_id"], project["project_id"], jobs.__getitem__)

            self.assertEqual(manifest["observation"], "STRUCTURAL_PREVIEW_ASSEMBLED")
            self.assertAlmostEqual(manifest["observed_duration_seconds"], 30.0, delta=0.2)
            self.assertEqual(len(manifest["segments"]), 6)
            self.assertTrue(all(item["duration_adaptation"] == "LOOP_THEN_TRIM" for item in manifest["segments"]))
            self.assertFalse(manifest["quality_acceptance_created"])

    def test_selection_requires_exact_human_confirmation(self) -> None:
        catalog = PilotCatalog(PROJECT_PATH.parent)
        workspace = PilotWorkspace(catalog, Path(tempfile.gettempdir()) / "unused-state", Path(tempfile.gettempdir()))
        with self.assertRaisesRegex(PilotOperationError, "完整输入"):
            workspace.select_candidate(
                self.project["project_id"],
                "SHOT-001",
                {"project_binding": {}, "state": "COMPLETED"},
                "SHOT-002",
            )


if __name__ == "__main__":
    unittest.main()
