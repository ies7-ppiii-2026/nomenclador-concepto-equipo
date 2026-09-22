"""Tests de la verificación de entradas requeridas del experimento."""

from pathlib import Path

import pytest

from nomenclador_concepto_equipo.inputs import (
    INFERENCE_INPUTS,
    VALIDATION_INPUTS,
    check_required_inputs,
)


def _make_files(tmp_path: Path, inputs: tuple[str, ...]) -> Path:
    for rel in inputs:
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("dummy")
    return tmp_path


def test_inference_and_validation_inputs_are_disjoint() -> None:
    # La validación agrega el mapping; no debe quitar archivos de inferencia.
    assert set(INFERENCE_INPUTS).isdisjoint(set(VALIDATION_INPUTS))


def test_check_required_inputs_returns_existing_files(tmp_path: Path) -> None:
    root = _make_files(tmp_path, INFERENCE_INPUTS)
    resolved = check_required_inputs(stage="inference", data_root=root)
    assert len(resolved) == len(INFERENCE_INPUTS)
    assert all(path.is_file() for path in resolved)


def test_check_required_inputs_raises_on_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Faltan archivos requeridos"):
        check_required_inputs(stage="inference", data_root=tmp_path)


def test_check_required_inputs_unknown_stage(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Etapa desconocida"):
        check_required_inputs(stage="no-existe", data_root=tmp_path)


def test_check_required_inputs_validation_needs_mapping(tmp_path: Path) -> None:
    root = _make_files(tmp_path, INFERENCE_INPUTS)
    with pytest.raises(FileNotFoundError, match="mapping"):
        check_required_inputs(stage="validation", data_root=root)
