# Guía 4 · Docker y Docker Compose

> **Propósito:** aprender Docker desde cero: teoría, instalación en Linux, comandos de referencia y una práctica final con imágenes, contenedores y Docker Compose.
>
> **Requisito:** una distribución Linux (Ubuntu/Debian, Fedora o Arch).

---

## Índice

1. [Teoría](#1-teoría)
2. [Mini guía de redes para Docker](#2-mini-guía-de-redes-para-docker)
3. [Instalación en Linux](#3-instalación-en-linux)
4. [Comandos de referencia](#4-comandos-de-referencia)
5. [Dockerfile](#5-dockerfile)
6. [Docker Compose](#6-docker-compose)
7. [Buenas prácticas](#7-buenas-prácticas)
8. [Práctica guiada](#8-práctica-guiada)
9. [Problemas frecuentes](#9-problemas-frecuentes)

---

## 1. Teoría

### 1.1 El problema que resuelve Docker

> "En mi máquina funciona."

Tu aplicación depende de una versión de Python, unas librerías, variables de entorno, un sistema operativo... Si cualquiera de esas cosas cambia en otra máquina, falla. Docker **empaqueta la aplicación con todo lo que necesita** para que funcione igual en cualquier lugar: tu PC, el de tu compañero, el servidor del CI, Render o tu propio servidor.

### 1.2 Contenedores vs máquinas virtuales

```
   MÁQUINA VIRTUAL                         CONTENEDORES
┌─────────┬─────────┐               ┌─────────┬─────────┐
│  App A  │  App B  │               │  App A  │  App B  │
│ Libs    │ Libs    │               │ Libs    │ Libs    │
│ SO inv. │ SO inv. │               ├─────────┴─────────┤
├─────────┴─────────┤               │   Docker Engine   │
│    Hipervisor     │               ├───────────────────┤
├───────────────────┤               │  Kernel del host  │
│   SO del host     │               ├───────────────────┤
├───────────────────┤               │     Hardware      │
│     Hardware      │               └───────────────────┘
└───────────────────┘
```

| | Máquina virtual | Contenedor |
|---|---|---|
| Qué virtualiza | Hardware completo | Solo el espacio de usuario (procesos) |
| Sistema operativo | Uno completo por VM | Comparten el kernel del host |
| Tamaño | Gigabytes | Megabytes |
| Arranque | Minutos | Segundos o menos |
| Aislamiento | Muy fuerte | Fuerte (namespaces y cgroups del kernel Linux) |

Docker funciona de forma nativa en Linux porque usa funciones del kernel: **namespaces** (cada contenedor ve sus propios procesos, red y archivos) y **cgroups** (limitan CPU y memoria).

### 1.3 Conceptos clave

| Concepto | Qué es | Analogía |
|---|---|---|
| **Imagen** | Plantilla de solo lectura con el sistema de archivos y la configuración para ejecutar una app | La **clase** en programación / el molde |
| **Contenedor** | Una instancia en ejecución de una imagen, con su propia capa escribible | El **objeto** / la galleta hecha con el molde |
| **Dockerfile** | Archivo de texto con las instrucciones para construir una imagen | La **receta** |
| **Capa (layer)** | Cada instrucción del Dockerfile crea una capa; se reutilizan (caché) | Hojas transparentes apiladas |
| **Registro (registry)** | Servidor que almacena imágenes: Docker Hub, GitHub Container Registry (GHCR) | GitHub, pero para imágenes |
| **Tag** | Versión o etiqueta de una imagen: `python:3.12-slim`, `miapp:1.0.0` | Un tag de Git |
| **Volumen** | Almacenamiento persistente fuera del contenedor | Un disco externo |
| **Red** | Red virtual que conecta contenedores entre sí | Un switch virtual |
| **Docker Compose** | Herramienta para definir y ejecutar varias imágenes con un archivo YAML | Un director de orquesta |

### 1.4 Ciclo de vida

```
Dockerfile --docker build--> Imagen --docker run--> Contenedor
                               |  ^
                   docker push |  | docker pull
                               v  |
                            Registro (Docker Hub / GHCR)
```

Estados de un contenedor: `created → running → paused → stopped (exited) → removed`.

> **Importante:** los contenedores son **efímeros**. Si borras un contenedor, se pierde todo lo que escribió dentro, salvo lo que esté en un **volumen**.

---

## 2. Mini guía de redes para Docker

Lo justo para entender los puertos y los despliegues de las Guías 6 y 7.

- **Dirección IP:** identifica a una máquina en una red. `127.0.0.1` (o `localhost`) es *la propia máquina*.
- **Puerto:** número (0–65535) que identifica a un programa dentro de una máquina. Una IP es el edificio; el puerto, el apartamento. Web: 80 (HTTP), 443 (HTTPS). Desarrollo: 3000, 5000, 8000, 8080.
- **Escuchar en `0.0.0.0`:** el programa acepta conexiones desde cualquier interfaz. **Dentro de un contenedor tu app debe escuchar en `0.0.0.0`**, no en `127.0.0.1`, o no será accesible desde fuera.
- **Mapeo de puertos (`-p 8080:80`):** `PUERTO_HOST:PUERTO_CONTENEDOR`. Lo que llegue al puerto 8080 de tu PC se reenvía al 80 del contenedor.
- **Red local vs internet:** tu PC tiene una IP privada (`192.168.x.x`) que el router traduce (NAT). Desde internet **no se puede llegar a tu PC** salvo que abras puertos en el router o uses un túnel. Por eso, en la Guía 7, el runner self-hosted es quien **se conecta a GitHub** (y no al revés).
- **DNS de Docker:** en una red de Docker Compose, los contenedores se encuentran **por el nombre del servicio**. El servicio `web` llega a Redis usando el host `redis`, no `localhost`.

```
   Tu navegador
        │  http://localhost:8080
        ▼
┌─────────────── Tu PC (host) ───────────────┐
│   puerto 8080 ──► ┌── contenedor web ───┐   │
│                   │ app en 0.0.0.0:8000 │   │
│                   └──────────┬──────────┘   │
│               red "appnet"   │ host: redis  │
│                   ┌──────────▼──────────┐   │
│                   │ contenedor redis    │   │
│                   │ 6379 (no expuesto)  │   │
│                   └─────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 3. Instalación en Linux

Se instala **Docker Engine** (no Docker Desktop) desde los repositorios oficiales de Docker. Documentación oficial: <https://docs.docker.com/engine/install/>

### 3.1 Ubuntu (22.04, 24.04 y posteriores)

```bash
# 1. Quitar paquetes no oficiales que puedan chocar
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
  sudo apt-get remove -y $pkg
done

# 2. Agregar la llave GPG oficial de Docker
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 3. Agregar el repositorio
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update

# 4. Instalar
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

> **Linux Mint, Pop!_OS, Zorin** (derivadas de Ubuntu): en el paso 3 la variable `UBUNTU_CODENAME` resuelve el nombre de la versión de Ubuntu base. Docker no las soporta oficialmente, pero suele funcionar.

### 3.2 Debian

Igual que Ubuntu, cambiando `ubuntu` por `debian` en las URL y usando `VERSION_CODENAME`:

```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3.3 Fedora

```bash
# 1. Quitar versiones antiguas
sudo dnf remove -y docker docker-client docker-client-latest docker-common \
  docker-latest docker-latest-logrotate docker-logrotate docker-selinux \
  docker-engine-selinux docker-engine

# 2. Agregar el repositorio (Fedora 41+ usa dnf5)
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
# En Fedora 40 o anterior: sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# 3. Instalar (acepta la huella GPG si la pregunta)
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 4. Fedora NO arranca el servicio solo
sudo systemctl enable --now docker
```

### 3.4 Arch Linux (y Manjaro, EndeavourOS)

Docker está en los repositorios oficiales de Arch:

```bash
sudo pacman -Syu
sudo pacman -S docker docker-compose docker-buildx
sudo systemctl enable --now docker.service
```

> En Arch, `docker-compose` del repositorio también instala el plugin, así que funcionan tanto `docker compose` como `docker-compose`.

### 3.5 Pasos posteriores (todas las distribuciones)

```bash
# Verificar que el servicio está activo
sudo systemctl status docker            # debe decir "active (running)"
sudo systemctl enable docker            # que arranque con el sistema

# Usar docker sin sudo: agregar tu usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker                           # o cierra sesión y vuelve a entrar

# Probar
docker run hello-world
docker version
docker compose version
```

> ⚠️ **Seguridad:** pertenecer al grupo `docker` equivale a tener permisos de root en la máquina. Es aceptable en tu PC de desarrollo; tenlo en cuenta en la Guía 7 (runner self-hosted).

---

## 4. Comandos de referencia

### 4.1 Imágenes

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `docker pull <imagen>[:tag]` | Descarga una imagen | `docker pull nginx:1.27-alpine` |
| `docker images` / `docker image ls` | Lista imágenes locales | `docker images` |
| `docker build -t <nombre>:<tag> <ruta>` | Construye una imagen desde un Dockerfile | `docker build -t miapp:1.0.0 .` |
| `docker build -f <archivo> ...` | Usa un Dockerfile con otro nombre | `docker build -f Dockerfile.prod -t miapp .` |
| `docker build --no-cache ...` | Construye sin usar caché | |
| `docker tag <origen> <destino>` | Crea otro nombre/tag para una imagen | `docker tag miapp:1.0.0 ana/miapp:1.0.0` |
| `docker push <imagen>` | Sube al registro | `docker push ana/miapp:1.0.0` |
| `docker rmi <imagen>` | Borra una imagen | `docker rmi miapp:1.0.0` |
| `docker image prune` | Borra imágenes "colgantes" (sin tag) | `docker image prune -f` |
| `docker image prune -a` | Borra todas las imágenes sin contenedores | |
| `docker history <imagen>` | Muestra las capas y su tamaño | `docker history miapp:1.0.0` |
| `docker image inspect <imagen>` | Detalles en JSON | |
| `docker search <término>` | Busca en Docker Hub | `docker search postgres` |
| `docker save -o <archivo>.tar <imagen>` | Exporta una imagen a archivo | |
| `docker load -i <archivo>.tar` | Importa desde archivo | |

### 4.2 Contenedores

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `docker run <imagen>` | Crea y ejecuta un contenedor | `docker run hello-world` |
| `docker run -d` | En segundo plano (*detached*) | `docker run -d nginx` |
| `docker run --name <n>` | Le da un nombre | `docker run -d --name web nginx` |
| `docker run -p H:C` | Mapea puertos host:contenedor | `docker run -d -p 8080:80 nginx` |
| `docker run -e VAR=valor` | Variable de entorno | `docker run -e DEBUG=1 miapp` |
| `docker run --env-file .env` | Variables desde archivo | |
| `docker run -v vol:/ruta` | Monta un volumen | `docker run -v datos:/var/lib/postgresql/data postgres` |
| `docker run -v $(pwd):/app` | Monta una carpeta del host (*bind mount*) | |
| `docker run -it <img> bash` | Interactivo con terminal | `docker run -it ubuntu bash` |
| `docker run --rm` | Se borra al terminar | `docker run --rm python:3.12 python -V` |
| `docker run --restart unless-stopped` | Se reinicia solo (también al encender el PC) | |
| `docker run --network <red>` | Lo conecta a una red | |
| `docker run -m 512m --cpus 1` | Limita memoria y CPU | |
| `docker ps` | Contenedores en ejecución | |
| `docker ps -a` | Todos, incluso detenidos | |
| `docker stop <c>` | Detiene (señal SIGTERM y espera) | `docker stop web` |
| `docker start <c>` | Arranca uno detenido | |
| `docker restart <c>` | Reinicia | |
| `docker kill <c>` | Detiene de inmediato (SIGKILL) | |
| `docker rm <c>` | Borra un contenedor detenido | `docker rm web` |
| `docker rm -f <c>` | Detiene y borra | |
| `docker logs <c>` | Muestra los logs | `docker logs web` |
| `docker logs -f --tail 50 <c>` | Sigue los últimos 50 logs en vivo | |
| `docker exec -it <c> sh` | Abre una terminal dentro del contenedor | `docker exec -it web sh` |
| `docker exec <c> <cmd>` | Ejecuta un comando dentro | `docker exec web ls /usr/share/nginx/html` |
| `docker cp <origen> <destino>` | Copia archivos host ↔ contenedor | `docker cp index.html web:/usr/share/nginx/html/` |
| `docker inspect <c>` | Detalles (IP, montajes, variables) | |
| `docker stats` | Uso de CPU y memoria en vivo | |
| `docker top <c>` | Procesos dentro del contenedor | |
| `docker port <c>` | Puertos mapeados | |
| `docker container prune` | Borra todos los contenedores detenidos | |

### 4.3 Volúmenes

| Comando | Qué hace |
|---|---|
| `docker volume create <v>` | Crea un volumen |
| `docker volume ls` | Lista volúmenes |
| `docker volume inspect <v>` | Detalles (dónde se guarda en el host) |
| `docker volume rm <v>` | Borra un volumen |
| `docker volume prune` | Borra los que no usa ningún contenedor |

**Volumen con nombre vs bind mount:**
- `-v datos:/data` → Docker gestiona dónde se guarda. Ideal para bases de datos.
- `-v $(pwd)/src:/app/src` → una carpeta tuya. Ideal en desarrollo para ver cambios sin reconstruir.

### 4.4 Redes

| Comando | Qué hace |
|---|---|
| `docker network ls` | Lista redes (`bridge`, `host`, `none` vienen por defecto) |
| `docker network create <red>` | Crea una red bridge propia (con DNS por nombre) |
| `docker network connect <red> <c>` | Conecta un contenedor a una red |
| `docker network inspect <red>` | Ver contenedores conectados |
| `docker network rm <red>` | Borra la red |

### 4.5 Registros (Docker Hub y GHCR)

```bash
# Docker Hub (crea cuenta en hub.docker.com)
docker login
docker tag miapp:1.0.0 <usuario-dockerhub>/miapp:1.0.0
docker push <usuario-dockerhub>/miapp:1.0.0

# GitHub Container Registry
# Crea un token: GitHub → Settings → Developer settings → Personal access tokens
#   → Tokens (classic) → scopes: write:packages, read:packages
echo "<TOKEN>" | docker login ghcr.io -u <usuario-github> --password-stdin
docker tag miapp:1.0.0 ghcr.io/<usuario-github>/miapp:1.0.0
docker push ghcr.io/<usuario-github>/miapp:1.0.0
```

> En GHCR el nombre debe ir **en minúsculas**. Las imágenes nuevas son privadas: para hacerlas públicas ve a tu perfil → **Packages** → la imagen → **Package settings → Change visibility**.

### 4.6 Sistema y limpieza

| Comando | Qué hace |
|---|---|
| `docker system df` | Espacio usado por imágenes, contenedores y volúmenes |
| `docker system prune` | Borra contenedores detenidos, redes sin uso e imágenes colgantes |
| `docker system prune -a --volumes` | Limpieza total ⚠️ (borra también volúmenes) |
| `docker info` | Información del motor |

---

## 5. Dockerfile

### 5.1 Instrucciones

| Instrucción | Para qué | Ejemplo |
|---|---|---|
| `FROM` | Imagen base (siempre la primera) | `FROM python:3.12-slim` |
| `WORKDIR` | Directorio de trabajo (lo crea si no existe) | `WORKDIR /app` |
| `COPY` | Copia archivos del proyecto a la imagen | `COPY requirements.txt .` |
| `ADD` | Como COPY, pero también descomprime y descarga URLs (preferir COPY) | |
| `RUN` | Ejecuta un comando **al construir** (crea una capa) | `RUN pip install -r requirements.txt` |
| `ENV` | Variable de entorno | `ENV PYTHONUNBUFFERED=1` |
| `ARG` | Variable solo durante la construcción | `ARG VERSION=dev` |
| `EXPOSE` | Documenta el puerto que usa la app (no lo publica) | `EXPOSE 8000` |
| `USER` | Usuario con el que corre el proceso | `USER appuser` |
| `CMD` | Comando por defecto **al ejecutar** el contenedor | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Ejecutable fijo; `CMD` pasa a ser sus argumentos | `ENTRYPOINT ["gunicorn"]` |
| `HEALTHCHECK` | Comando para saber si la app está sana | ver ejemplo |
| `LABEL` | Metadatos | `LABEL org.opencontainers.image.source="https://github.com/ana/repo"` |

**`RUN` vs `CMD`:** `RUN` ocurre al **construir** la imagen; `CMD` ocurre al **iniciar** el contenedor.

### 5.2 Ejemplo comentado (Python + Flask)

```dockerfile
# Imagen base pequeña y con versión fija
FROM python:3.12-slim

# Evita archivos .pyc y muestra los logs al instante
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1º las dependencias: esta capa se reutiliza mientras requirements.txt no cambie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2º el código (cambia seguido, va al final para aprovechar la caché)
COPY . .

# Usuario sin privilegios
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### 5.3 Multi-stage (imágenes más livianas)

Se construye en una etapa con todas las herramientas y se copia solo el resultado a una imagen final mínima. Ejemplo con un frontend Node:

```dockerfile
# Etapa 1: construcción
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Etapa 2: solo los archivos estáticos servidos por nginx
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

### 5.4 .dockerignore

Igual que `.gitignore`, pero para lo que **no** debe copiarse a la imagen:

```
.git
.github
.venv
__pycache__
*.pyc
.pytest_cache
htmlcov
.env
node_modules
Dockerfile
docker-compose*.yml
```

---

## 6. Docker Compose

Define **varios servicios** (app, base de datos, caché) en un archivo `compose.yaml` (o `docker-compose.yml`) y los maneja juntos.

### 6.1 Estructura

```yaml
services:
  web:
    build: .                       # construye desde el Dockerfile local
    # image: ghcr.io/ana/miapp:latest   # o usa una imagen ya publicada
    container_name: miapp-web
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
    env_file:
      - .env
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - appnet

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - appnet

volumes:
  redis-data:

networks:
  appnet:
```

### 6.2 Comandos de Compose

| Comando | Qué hace |
|---|---|
| `docker compose up` | Crea y arranca todos los servicios (logs en primer plano) |
| `docker compose up -d` | En segundo plano |
| `docker compose up -d --build` | Reconstruye las imágenes antes de arrancar |
| `docker compose up -d --force-recreate` | Recrea los contenedores aunque no hayan cambiado |
| `docker compose down` | Detiene y borra contenedores y redes (los volúmenes se conservan) |
| `docker compose down -v` | También borra los volúmenes ⚠️ |
| `docker compose ps` | Estado de los servicios |
| `docker compose logs -f <servicio>` | Logs en vivo |
| `docker compose exec <servicio> sh` | Terminal dentro de un servicio |
| `docker compose build` | Solo construye |
| `docker compose pull` | Descarga las versiones nuevas de las imágenes (**clave en la Guía 7**) |
| `docker compose restart <servicio>` | Reinicia un servicio |
| `docker compose stop` / `start` | Detiene / arranca sin borrar |
| `docker compose config` | Valida y muestra el archivo final |
| `docker compose up -d --scale web=3` | Varias réplicas (sin `container_name` ni puerto fijo) |
| `docker compose -f compose.prod.yaml up -d` | Usa otro archivo |

---

## 7. Buenas prácticas

1. **Fija versiones** de las imágenes base (`python:3.12-slim`, no `python:latest`).
2. **Imágenes pequeñas:** variantes `slim` o `alpine`, multi-stage.
3. **Ordena por frecuencia de cambio:** dependencias primero, código al final (aprovecha la caché).
4. **No corras como root:** usa `USER`.
5. **Nunca metas secretos en la imagen:** ni en el Dockerfile ni copiando el `.env`. Pásalos con variables de entorno en tiempo de ejecución.
6. **Un proceso por contenedor:** app y base de datos en contenedores separados.
7. **Usa `.dockerignore`.**
8. **Escucha en `0.0.0.0`** y lee el puerto desde una variable de entorno (Render lo necesita, Guía 7).
9. **Agrega un `HEALTHCHECK`** y un endpoint `/health`.
10. **Etiqueta con versión** (`1.2.0`) además de `latest`.

---

## 8. Práctica guiada

### Parte A · Imágenes y contenedores de terceros

```bash
# 1. Descargar imágenes
docker pull nginx:1.27-alpine
docker pull redis:7-alpine
docker images

# 2. Levantar nginx publicado en el puerto 8080
docker run -d --name mi-nginx -p 8080:80 nginx:1.27-alpine
docker ps
curl http://localhost:8080          # o ábrelo en el navegador

# 3. Modificar la página desde fuera y desde dentro
echo "<h1>Hola desde Docker</h1>" > index.html
docker cp index.html mi-nginx:/usr/share/nginx/html/index.html
curl http://localhost:8080
docker exec -it mi-nginx sh         # explora; sal con: exit

# 4. Logs, detener, arrancar, borrar
docker logs mi-nginx
docker stop mi-nginx
docker ps -a                        # aparece como Exited
docker start mi-nginx
docker rm -f mi-nginx

# 5. Comprobar que el cambio se perdió (los contenedores son efímeros)
docker run -d --name mi-nginx -p 8080:80 nginx:1.27-alpine
curl http://localhost:8080          # vuelve la página por defecto
docker rm -f mi-nginx

# 6. Ahora con bind mount: el cambio vive en tu carpeta
mkdir -p sitio && echo "<h1>Persistente</h1>" > sitio/index.html
docker run -d --name mi-nginx -p 8080:80 -v $(pwd)/sitio:/usr/share/nginx/html:ro nginx:1.27-alpine
curl http://localhost:8080
docker rm -f mi-nginx
```

**Preguntas de control:** ¿por qué se perdió el cambio del paso 5? ¿Qué significa `:ro`?

### Parte B · Construir, etiquetar, subir y bajar tu propia imagen

1. Crea la carpeta del proyecto:

```bash
mkdir contador-docker && cd contador-docker
```

2. `app.py`:

```python
import os
from flask import Flask
import redis

app = Flask(__name__)
cache = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)


@app.get("/")
def inicio():
    visitas = cache.incr("visitas")
    return f"<h1>Hola Docker</h1><p>Esta página se ha visitado {visitas} veces.</p>"


@app.get("/health")
def health():
    return {"status": "ok"}
```

3. `requirements.txt`:

```
flask==3.1.0
redis==5.2.1
gunicorn==23.0.0
```

4. Copia el `Dockerfile` de la [sección 5.2](#52-ejemplo-comentado-python--flask) y el `.dockerignore` de la [sección 5.4](#54-dockerignore).

5. Construye y prueba:

```bash
docker build -t contador:1.0.0 .
docker images contador
docker history contador:1.0.0

# Falla porque no hay Redis todavía: es esperado. Mira el error en los logs.
docker run -d --name contador -p 8000:8000 contador:1.0.0
curl http://localhost:8000
docker logs contador
docker rm -f contador
```

6. Súbela a un registro (Docker Hub o GHCR, ver [4.5](#45-registros-docker-hub-y-ghcr)):

```bash
docker tag contador:1.0.0 ghcr.io/<usuario>/contador:1.0.0
docker tag contador:1.0.0 ghcr.io/<usuario>/contador:latest
docker push ghcr.io/<usuario>/contador:1.0.0
docker push ghcr.io/<usuario>/contador:latest
```

7. Bórrala localmente y descárgala del registro:

```bash
docker rmi contador:1.0.0 ghcr.io/<usuario>/contador:1.0.0 ghcr.io/<usuario>/contador:latest
docker images | grep contador        # ya no está
docker pull ghcr.io/<usuario>/contador:1.0.0
docker images | grep contador        # volvió, desde el registro
```

### Parte C · Docker Compose: subir y bajar el sistema completo

1. `compose.yaml` en la misma carpeta:

```yaml
services:
  web:
    build: .
    image: ghcr.io/<usuario>/contador:latest
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5
    restart: unless-stopped

volumes:
  redis-data:
```

2. Ejecuta y observa:

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000           # 1 visita
curl http://localhost:8000           # 2 visitas
docker compose logs -f web           # Ctrl+C para salir

# Persistencia: bajar y subir
docker compose down
docker compose up -d
curl http://localhost:8000           # ¿3 visitas? El volumen conservó los datos

# Ahora borrando volúmenes
docker compose down -v
docker compose up -d
curl http://localhost:8000           # vuelve a 1
```

3. **Simular una actualización (lo que hará el CD de la Guía 7):**

```bash
# Cambia el texto "Hola Docker" por "Hola Docker v2" en app.py
docker compose build
docker push ghcr.io/<usuario>/contador:latest
# --- en "otro servidor" sería: ---
docker compose pull
docker compose up -d                 # solo recrea el servicio que cambió
curl http://localhost:8000
docker image prune -f                # limpia la imagen vieja
```

4. Limpieza final:

```bash
docker compose down -v
docker system df
```

### Entregable de la práctica (sugerido)

- Captura de `docker images` mostrando tu imagen con dos tags.
- Enlace a la imagen publicada en GHCR o Docker Hub.
- Captura de `docker compose ps` con ambos servicios en estado `healthy`.
- Respuesta: ¿qué diferencia hay entre `docker compose down` y `docker compose down -v`?

---

## 9. Problemas frecuentes

| Error | Causa | Solución |
|---|---|---|
| `permission denied while trying to connect to the Docker daemon socket` | Tu usuario no está en el grupo `docker` | `sudo usermod -aG docker $USER` y cerrar sesión |
| `Cannot connect to the Docker daemon` | El servicio no está corriendo | `sudo systemctl start docker` |
| `port is already allocated` | Otro programa usa ese puerto | Cambia el puerto del host (`-p 8081:80`) o detén el otro proceso (`sudo ss -tulpn \| grep 8080`) |
| La app no responde desde el navegador | Escucha en `127.0.0.1` dentro del contenedor | Haz que escuche en `0.0.0.0` |
| `Connection refused` a la base de datos | Usas `localhost` en vez del nombre del servicio | Usa el nombre del servicio (`redis`, `db`) |
| `no space left on device` | Imágenes viejas acumuladas | `docker system prune -a` |
| `denied: permission_denied` al hacer push a GHCR | Token sin `write:packages` o nombre en mayúsculas | Revisa el token y usa minúsculas |
| Los cambios del código no se ven | Imagen no reconstruida | `docker compose up -d --build` |
