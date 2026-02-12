# Curso Git - Material de apoyo

Este repositorio contiene apuntes y guias rapidas para aprender y consultar Git, junto con una guia practica para trabajar con GitHub y GitLab en distintos sistemas operativos. La idea es que puedas usarlo como referencia en clase, en laboratorios o en proyectos personales.

## Objetivo

- Reunir en un solo lugar los comandos mas usados de Git con ejemplos claros.
- Explicar el flujo de trabajo habitual con repositorios remotos.
- Documentar configuracion inicial, autenticacion con SSH y herramientas de apoyo.

## Contenido del repositorio

- [guiaRapidaGit.md](guiaRapidaGit.md): guia rapida con los comandos mas usados de Git.
	- Configuracion inicial y verificacion.
	- Operaciones basicas (status, add, commit).
	- Ramas y fusiones.
	- Remotos, push/pull/fetch.
	- Historial y revision de cambios.
	- Deshacer cambios y revertir commits.
	- Stash y tags.
	- Flujos tipicos de trabajo.

- [github-gitlab-os.md](github-gitlab-os.md): guia para trabajar con GitHub y GitLab en distintos sistemas operativos.
	- Instalacion de Git y utilidades (man, less, tree).
	- Creacion y uso de llaves SSH.
	- Configuracion de SSH para GitHub y GitLab.
	- Uso de man y less para documentacion.
	- Flujos de PR/MR, forks y sincronizacion.
	- CLI oficiales (gh y glab).
	- Solucion de problemas comunes.

## Como usar este repo

1. Empieza por [guiaRapidaGit.md](guiaRapidaGit.md) para una vista general de Git.
2. Si necesitas trabajar con GitHub o GitLab, revisa [github-gitlab-os.md](github-gitlab-os.md).
3. Copia y adapta los comandos segun tu sistema operativo y tu flujo de trabajo.

## Flujo de estudio sugerido

1. Configura Git y verifica tu usuario y correo.
2. Practica con un repositorio local (init, add, commit).
3. Crea ramas, fusiona y revisa el historial.
4. Conecta un remoto y aprende a hacer push/pull.
5. Configura SSH y prueba la conexion.
6. Practica un flujo completo con PR/MR.

## Recomendaciones

- Mantener mensajes de commit claros y breves.
- Usar ramas para cambios grandes o experimentales.
- Sincronizar con el remoto antes de empezar a trabajar.
- Consultar `man git` y `git help <comando>` cuando tengas dudas.

## Notas

- Los comandos estan pensados como referencia rapida, no como sustituto de la documentacion oficial.
- Si estas en Windows, usa Git Bash para una experiencia mas cercana a Linux.
