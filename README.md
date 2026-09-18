# agentes-config-lab

Laboratorio aislado para comparar agentes/modelos de desarrollo con una metodología reproducible, sin tocar repositorios productivos.

## Objetivo

Medir calidad técnica, cumplimiento de alcance, seguridad, evidencia, costo operativo y necesidad de intervención humana en tareas de desarrollo comparables.

El laboratorio es deliberadamente **vendor-neutral**: puede utilizarse con OpenAI, Anthropic u otros agentes sin cambiar la rúbrica.

## Principios

- Repositorio aislado. Ninguna prueba debe modificar proyectos productivos.
- Baseline estricto: una discrepancia material invalida la ejecución hasta reconstruir el estado real.
- Cada ejecución debe trabajar sobre una rama o worktree limpio y desechable.
- La evaluación separa evidencia declarada de evidencia observada.
- No se premia una solución solamente por compilar o pasar tests parciales.
- Se registran tiempo, costo y cantidad de intervenciones humanas además del resultado técnico.

## Desafíos

1. `repo-triage`: inspección del estado real, identificación de riesgos y plan de cambio.
2. `defect-remediation`: corrección acotada de un defecto con pruebas y preservación de invariantes.
3. `delivery-review`: revisión integral de una entrega, diff, pruebas, seguridad, UX y handoff.

Cada desafío vale 100 puntos antes de penalizaciones.

## Evidencia E0-E4

- **E0**: no inspeccionado.
- **E1**: reporte recibido.
- **E2**: archivo, diff o artefacto inspeccionado.
- **E3**: comando, test o log observado.
- **E4**: flujo funcional o visual reproducido.

## Ejecución local

Requiere Python 3.11+ y no tiene dependencias de terceros.

```bash
python -m unittest discover -s tests -v
python -m lab validate
python -m lab simulate
```

`simulate` valida el pipeline con datos sintéticos. Las ejecuciones reales contra agentes requieren proporcionar sus resultados y métricas; no hay claves ni sesiones embebidas en el repositorio.

## Métricas

Cada run registra como mínimo:

- puntaje técnico bruto;
- penalizaciones;
- puntaje final;
- evidencia máxima alcanzada;
- duración en segundos;
- costo monetario informado;
- cantidad de intervenciones humanas;
- tests ejecutados/pasados;
- violaciones de alcance o seguridad.

## Aislamiento recomendado

Para pruebas reales, crear un worktree por agente y ejecución:

```bash
git worktree add ../runs/<agent>-<run-id> -b lab/<agent>-<run-id>
```

Nunca reutilizar un worktree contaminado entre competidores.

## CI

GitHub Actions ejecuta las 8 pruebas unitarias y valida las definiciones de los tres desafíos.

## Estado

La estructura actual reconstruye el laboratorio validado previamente en Work a partir de sus decisiones canónicas conocidas: tres desafíos, rúbrica de 100 puntos, penalizaciones, métricas de costo/tiempo/intervenciones, evidencia E0-E4, baseline estricto, worktrees aislados y CI.

El commit local original de Work (`c321eca`) no está disponible en este entorno, por lo que este repositorio no pretende falsificar identidad binaria con aquel árbol: conserva su alcance y metodología verificables.
