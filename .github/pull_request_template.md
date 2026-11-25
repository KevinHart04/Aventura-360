## Qué cambia y por qué

<!-- 2-4 líneas. Qué problema resuelve. -->

## Cómo se probó

<!-- Pasos manuales + tests agregados. Qué falla si revierto el cambio. -->

## ¿Generado con IA?

- [ ] Sí, herramienta/modelo: \_\_\_
- [ ] No

## Checklist del autor (obligatorio)

- [ ] Leí TODO el diff línea por línea y entiendo qué hace
- [ ] Los tests nuevos fallan si revierto el cambio
- [ ] No agregué dependencias, o las justifiqué en "Justificaciones"
- [ ] No toqué configs de calidad ni CI, o lo justifiqué en "Justificaciones"
- [ ] Revisé casos borde: vacío, null, concurrencia, permisos
- [ ] Todo endpoint nuevo tiene permisos explícitos y tests de acceso denegado

## ¿Toca áreas críticas?

- [ ] Precios, pagos o checkout
- [ ] Autenticación o permisos
- [ ] Migraciones o modelos de datos
- [ ] Ninguna

## Checklist del revisor

- [ ] Probé la rama en local o entiendo el flujo completo
- [ ] Entiendo la lógica; no solo vi que los checks están en verde
- [ ] Revisé qué pasa si falla (errores, timeouts, datos inválidos)

## Justificaciones (dependencias, cambios de config, excepciones)

<!-- Si dejaste esta sección vacía, confirma que no aplica. -->

## Capturas o video (si hay cambios de
