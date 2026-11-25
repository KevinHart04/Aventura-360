# Reglas del proyecto (obligatorias para humanos y para IA)

Ecommerce: React + TypeScript + Vite (`frontend/`), Django REST Framework + PostgreSQL (`backend/`).
Estas reglas las hace cumplir el CI. Si tu cambio las rompe, el PR no se puede mergear.

## Antes de dar una tarea por terminada

Ejecuta todo y corrige hasta que pase. No digas "listo" sin haberlo corrido.

Backend (desde `backend/`, con Postgres arriba: `docker compose up -d db`):

    uv run ruff format --check .
    uv run ruff check .
    uv run mypy .
    uv run vulture
    uv run python manage.py makemigrations --check --dry-run
    uv run pytest

Frontend (desde `frontend/`):

    npm run format:check
    npm run lint
    npm run typecheck
    npm run knip
    npm test
    npm run build

Raíz: `./scripts/check-no-bypass.sh`

## Prohibido (sin excepciones)

- Silenciar reglas: `eslint-disable`, `@ts-ignore`, `@ts-nocheck`, `# noqa`, `# type: ignore`, `# pragma: no cover`. Arregla el código.
- `any` en TypeScript y `Any` en Python salvo justificación en el PR.
- `test.skip`, `test.only`, `test.fixme`, `pytest.mark.skip`, `xfail` para esconder un fallo.
- Borrar o debilitar un test para que pase. Si un test falla, el código o el test tiene un bug real: entiéndelo.
- Modificar configuración de calidad para que algo pase: `eslint.config.js`, `tsconfig*.json`, `pyproject.toml` (ruff, mypy, vulture), `knip.json`, `.pre-commit-config.yaml`, `scripts/`, `.github/`. Si crees que hace falta, **detente y pregunta**.
- Saltarse hooks (`git commit --no-verify`, `git push --no-verify`) o forzar pushes.
- Commitear a `main` directamente, o secretos, `.env` y claves reales.
- Agregar dependencias sin permiso (ver abajo).

## Dependencias

- No agregues ninguna sin que una persona lo apruebe antes.
- Antes de proponerla, verifica que el paquete exista, esté mantenido y sea el correcto (cuidado con nombres inventados o parecidos a paquetes conocidos).
- Justifica cada una en la sección "Justificaciones" del PR.
- Usa `uv add` / `npm install` para que los lockfiles se actualicen, y commitea el lockfile.
- Prefiere la librería estándar o lo que ya está instalado.

## Tests

- Todo cambio de comportamiento lleva tests que **fallen sin el cambio**.
- Prueba comportamiento, no implementación. No mockees la unidad bajo prueba.
- Todo test debe tener asserts reales (nada de `assert True` ni tests vacíos).
- Bugs: primero un test que lo reproduzca, luego el arreglo.
- Backend: pytest con base de datos real, no la reemplaces por mocks.

## Backend (Django / DRF)

- El permiso por defecto es `IsAuthenticated`. Abrir un endpoint (`AllowAny`) requiere justificarlo en el PR y un test.
- Todo endpoint nuevo: permisos explícitos, serializer con validación, y tests de acceso denegado.
- Un usuario solo puede ver y modificar **sus** recursos: filtra el queryset por usuario.
- Dinero: enteros en centavos o `Decimal`. Nunca `float`.
- Nunca confíes en precios, totales ni descuentos que vengan del cliente: se recalculan en el servidor.
- Cambios de modelo = migración commiteada. Revisa que sea reversible y no pierda datos.
- Prohibido SQL armado con strings. Usa el ORM o parámetros.
- No dejes `print`, `DEBUG=True` ni credenciales en el código. Configuración por variables de entorno.

## Frontend (React / TypeScript)

- TypeScript estricto, sin `any`. Valida con tipos lo que viene de la API.
- Un componente por archivo, funciones pequeñas (el linter limita complejidad y tamaño).
- Nada de `console.log`. Maneja errores y estados de carga.
- Accesibilidad básica: etiquetas, roles y texto alternativo (jsx-a11y está activo).
- El frontend no es una frontera de seguridad: las validaciones reales viven en el backend.

## Git y PRs

- Una rama por cambio: `feature/...`, `fix/...`, `chore/...`, `ci/...`.
- Commits y título del PR en Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:`, `perf:`, `build:`.
- PRs pequeños: máximo 500 líneas cambiadas (sin lockfiles ni migraciones). Si es más grande, divídelo.
- Un PR = un propósito. No mezcles refactors con funcionalidades.
- Completa la plantilla del PR de forma honesta y marca "Generado con IA".
- El autor es responsable de cada línea, la haya escrito una IA o no.

## Áreas críticas: avisa antes de tocarlas

Pagos, checkout, precios, autenticación, permisos, migraciones y `settings.py`.
Explica el plan y espera confirmación humana. Estos cambios los revisa una persona con atención especial.

## Si no estás seguro

Pregunta en vez de asumir. No inventes APIs, funciones ni paquetes: lee el código existente o la documentación. Si no puedes cumplir una regla, dilo explícitamente en lugar de esquivarla.
