---
name: Andina Dashboard Deployment
description: Instrucciones para el despliegue automatizado, mantenimiento del servidor y acceso SSH para el Dashboard de Piping de Andina.
---

# Andina Dashboard Deployment (CI/CD)

Este skill documenta la arquitectura de despliegue y los procedimientos de mantenimiento del servidor Ubuntu (`lukeserver`) para el proyecto Andina.

## Acceso SSH
- **Alias**: `ssh luke-ssh` (Configurado en `~/.ssh/config` del host local).
- **Usuario**: `cristian`
- **Mecanismo**: Autenticación por llave pública (RSA 4096). No requiere contraseña para SSH.
- **Sudo Pass**: `0174`

## Estructura del Proyecto
- **Ruta Local**: `D:\Github\Andina\Dashboard`
- **Ruta Servidor**: `/home/cristian/andina-dashboard`
- **Repositorio**: `https://github.com/Crisvalpo/andina-dashboard`

## Flujo de Automatización (Push-to-Deploy)
El despliegue es 100% automático al hacer push a GitHub:
1.  **Local**: `git push origin main`
2.  **Webhook**: GitHub notifica al servicio `deploy-webhook` en el puerto 9000.
3.  **Deploy Script**: El servidor ejecuta `/home/cristian/deploy/deploy-andina.sh`.
4.  **Acción**: El script hace `git pull`, `npm install` y reinicia el proceso PM2.

### Comandos de Control (PM2)
Debido al entorno NVM, usa la ruta completa si falla el comando `pm2` directo:
```bash
# Ver estado
/home/cristian/.nvm/versions/node/v20.20.0/bin/pm2 list

# Reiniciar manualmente
/home/cristian/.nvm/versions/node/v20.20.0/bin/pm2 restart andina-dashboard

# Ver logs de despliegue
/home/cristian/.nvm/versions/node/v20.20.0/bin/pm2 logs deploy-webhook
```

## Mantenimiento del Servidor
- **Actualizaciones**: `sudo apt update && sudo apt upgrade -y`
- **Zombies**: En caso de procesos zombie, realizar un `sudo reboot`.
- **Ubicación de Scripts**: `/home/cristian/deploy/`

## Llave de Despliegue (Deploy Key)
El servidor utiliza e identifíca la llave `~/.ssh/id_rsa_github` para autenticarse con GitHub. Esta llave debe estar registrada como **Deploy Key** (solo lectura) en el repositorio de GitHub.
