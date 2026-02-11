# 📚 Curso de Git

Guía completa de comandos y configuración para trabajar con Git de forma eficiente.

---

## 📦 Instalación

### Instalar MAN para documentación
```bash
sudo pacman -S man-db man-pages less
```

### Instalar Git
```bash
sudo pacman -S git
```

---

## 🔧 Configuración Inicial

### Ver todos los comandos disponibles
```bash
git -h
```

### Obtener documentación de un comando
```bash
git help COMANDO
```

### Configurar usuario y email (GLOBAL)
```bash
git config --global user.name "NOMBRE"
git config --global user.email "EMAIL"
git config --list
```

---

## 🚀 Primeros Pasos

### Inicializar un repositorio
```bash
git init
git status
```

### Agregar archivos al staging area
```bash
git add FILE        # Agregar un archivo específico
git add .           # Agregar todos los cambios
```

### Crear el primer commit
```bash
git commit -m "MENSAJE"
```

---

## 📝 Gestión de Cambios

### Descartar cambios no commiteados en un archivo
```bash
git checkout -- FILE
```

### Descartar todos los cambios en el directorio actual
```bash
git checkout -- .
```

### Restaurar un archivo a un commit específico
```bash
git checkout HASH -- FILE
git checkout HEAD~n -- FILE
```

---

## 📋 Ver Historial de Commits

### Ver todos los commits con hashes completos
```bash
git log
```

### Ver en formato compacto
```bash
git log --oneline
```

### Ver últimos N commits
```bash
git log -3
git log --oneline -5
```

---

## 🔄 Moverse Entre Commits

### Ver todos los cambios (incluyendo eliminados)
```bash
git reflog
```

### Moverse entre commits (solo vista, retorna al último commit con el mismo comando)
```bash
git reset --mixed HASH
```

### Retornar a un commit anterior ⚠️ (ELIMINA cambios posteriores)
```bash
git reset --hard HASH
```

---

**⚡ Nota:** Siempre recuerda retornar al último commit después de navegarexplorando.
