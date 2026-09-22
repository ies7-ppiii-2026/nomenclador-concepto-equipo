"""Verificación de entradas requeridas para las etapas del experimento.

Las rutas son relativas a ``data/raw`` y siguen el contrato definido en
``docs/experiment-contract.md``.
"""

from __future__ import annotations

from pathlib import Path

# Archivos que consume la inferencia: SOLO ICD-10 e ICD-11.
# data/raw/mapping/ queda excluida hasta la validación (es ground truth).
INFERENCE_INPUTS: tuple[str, ...] = (
    "icd10/icd102019en.xml/icd102019en.xml",
    "icd11/SimpleTabulation-ICD-11-MMS-en/SimpleTabulation-ICD-11-MMS-en.txt",
    "icd11/SimpleTabulation-ICD-11-MMS-en/SimpleTabulation-ICD-11-MMS-en.xlsx",
)

# Archivos extra que consume la validación (ground truth oficial).
VALIDATION_INPUTS: tuple[str, ...] = (
    "mapping/mapping/10To11MapToOneCategory.txt",
    "mapping/mapping/10To11MapToOneCategory.xlsx",
    "mapping/mapping/10To11MapToMultipleCategories.txt",
    "mapping/mapping/10To11MapToMultipleCategories.xlsx",
    "mapping/mapping/11To10MapToOneCategory.txt",
    "mapping/mapping/11To10MapToOneCategory.xlsx",
)

STAGES: dict[str, tuple[str, ...]] = {
    "inference": INFERENCE_INPUTS,
    "validation": VALIDATION_INPUTS,
}


def check_required_inputs(stage: str = "inference", data_root: str | Path = "data/raw") -> list[Path]:
    """Verifica que existan los archivos requeridos para una etapa.

    Args:
        stage: nombre de la etapa, ``"inference"`` o ``"validation"``.
        data_root: ruta a la carpeta ``data/raw`` del proyecto.

    Returns:
        Lista de rutas resueltas de los archivos presentes.

    Raises:
        ValueError: si ``stage`` no es una etapa conocida.
        FileNotFoundError: si falta algún archivo requerido.
    """
    if stage not in STAGES:
        raise ValueError(f"Etapa desconocida: {stage!r}. Válidas: {sorted(STAGES)}")

    root = Path(data_root)
    missing = [str(root / rel) for rel in STAGES[stage] if not (root / rel).is_file()]
    if missing:
        detail = "; ".join(missing)
        raise FileNotFoundError(f"Faltan archivos requeridos para la etapa {stage!r}: {detail}")

    return [root / rel for rel in STAGES[stage]]
