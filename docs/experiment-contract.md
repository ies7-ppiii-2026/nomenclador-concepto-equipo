# Contrato del experimento — ICD-10 → ICD-11

**Versión del contrato:** 1.0.0

## Quick path

1. Leer [docs/data-origins.md](data-origins.md) para orígenes y hashes de los crudos.
2. Antes de cualquier etapa, validar entradas con `check_required_inputs`.
3. Verificar la separación inferencia / validación (sección 8).

## Details

### 1. Objetivo

Mapear códigos ICD-10 (`source`) a códigos ICD-11 (`target`) produciendo, para
cada entrada, una **lista ordenada de candidatos** con su ranking, score y
probabilidad relativa. El matcher puede **abstenerse** cuando no encuentra
candidatos confiables.

### 2. Entradas permitidas

La **inferencia** solo puede consumir los archivos ICD-10 e ICD-11 de
`data/raw/`:

- `data/raw/icd10/icd102019en.xml/icd102019en.xml`
- `data/raw/icd11/SimpleTabulation-ICD-11-MMS-en/SimpleTabulation-ICD-11-MMS-en.txt`
- `data/raw/icd11/SimpleTabulation-ICD-11-MMS-en/SimpleTabulation-ICD-11-MMS-en.xlsx`

`data/raw/mapping/` (el mapping oficial) queda **excluida de la inferencia**:
es ground truth y solo se consume en la etapa de validación/evaluación.

El origen y los hashes SHA-256 de estas fuentes están en
[docs/data-origins.md](data-origins.md).

### 3. Salida multivaluada

La salida de una ejecución es una tabla con **una fila por candidato**. Un
mismo `source_code` puede repetirse en varias filas, una por cada `target_code`
candidato.

| Campo          | Tipo    | Descripción                                                        |
| -------------- | ------- | ------------------------------------------------------------------ |
| `source_code`  | string  | Código ICD-10 de entrada (por ej. `A00.0`).                        |
| `target_code`  | string  | Código ICD-11 candidato. Vacío (`""`) si `abstain` es `true`.      |
| `rank`         | int     | Posición del candidato en el ranking, de `1` a `k`.                |
| `score`        | float   | Score crudo del matcher para este candidato.                       |
| `probability`  | float   | Probabilidad relativa normalizada sobre el top-k del mismo source. |
| `abstain`      | bool    | `true` si la entrada no genera predicción.                         |

Reglas de la salida:

- **No se fuerza un mapeo 1:1.** Un `source_code` puede tener `0..k`
  candidatos; dos sources distintos pueden apuntar al mismo `target_code`.
- Si `abstain` es `true`, la fila tiene `target_code = ""`, `rank = 0`,
  `score = None` y `probability = None`.

### 4. Scores y probabilidades relativas

- `score` es la salida **cruda** del algoritmo de matching (por ejemplo
  similitud de strings, coincidencia de tokens). No tiene una escala fija:
  solo es comparable entre candidatos del mismo `source_code`.
- `probability` es la **probabilidad relativa** obtenida normalizando los
  scores del top-k de un mismo `source_code` (por ejemplo softmax o división
  por la suma), de modo que suman `1.0` por entrada. No son probabilidades
  calibradas salvo que el experimento lo declare explícitamente.

### 5. Abstenciones

Una entrada se abstiene cuando:

1. No se encontró ningún candidato, o
2. El mejor candidato no supera el umbral mínimo de score configurado.

El umbral es un parámetro de configuración (`min_score`, default `0.0`).
Cuando `abstain` es `true`, el resto de los campos sigue la regla de la
sección 3.

### 6. Top-k

La salida se limita a `k` candidatos por `source_code`, ordenados por ranking
(mejor score primero). `k` es un parámetro de configuración (`top_k`, default
`10`, mínimo `1`). Si hay menos de `k` candidatos, se devuelven los que existan.

### 7. Versiones

- **Contrato:** cada cambio en los campos, reglas o alcance del experimento
  requiere bump de la versión de este documento (semver) y actualizar el
  registro de issues (`docs/issues.md`).
- **Datos:** el experimento declara con qué versiones de ICD se ejecuta.
  Ver hashes y release en [docs/data-origins.md](data-origins.md). Cambiar de
  versión de datos exige re-ejecutar el experimento completo y registrar el
  nuevo hash.

### 8. Separación entre inferencia y validación

| Etapa        | Archivos que consume                                     | Propósito                   |
| ------------ | -------------------------------------------------------- | --------------------------- |
| Inferencia   | Solo ICD-10 + ICD-11 (ver sección 2)                     | Generar predicciones        |
| Validación   | ICD-10 + ICD-11 + `data/raw/mapping/` (ground truth)     | Evaluar contra el oficial   |

La etapa de inferencia **no debe leer** ningún archivo de `data/raw/mapping/`.
Las transformaciones y reportes se escriben en `data/processed/` y `reports/`,
nunca sobre los datos crudos.

### 9. Verificación de entradas faltantes

Antes de ejecutar cualquier etapa se verifica la existencia de sus archivos de
entrada. Si falta alguno, la ejecución **aborta con un error descriptivo** que
lista las rutas faltantes.

Implementación en
`src/nomenclador_concepto_equipo/inputs.py`:

```python
from nomenclador_concepto_equipo.inputs import check_required_inputs

check_required_inputs(stage="inference")   # data/raw/icd10 + icd11
check_required_inputs(stage="validation")  # + data/raw/mapping
```

## Checklist

- [x] Contrato versionado (semver).
- [x] Definidos `source_code`, `target_code`, `rank`, `score`, `probability`, `abstain`.
- [x] Aclara que no se fuerza un mapeo 1:1.
- [x] Define qué archivos lee cada etapa.
- [x] Verificación de entradas faltantes con error descriptivo.

## Next step

Abrir el PR de la issue #2 y actualizar `docs/issues.md` con rama y número de PR.
