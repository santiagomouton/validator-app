# validator-app

Validator API es una API REST desarrollada con FastAPI para validar si un MD5 corresponde al contenido de un payload JSON enviado por el cliente.

La solución está pensada para ser sencilla de levantar con la posibilidad de seguir su desarrollo de manera local, y que actue el Github Action para desplegarlo en ambientes remotos.

La API sigue una arquitectura por capas para mantener una separación de responsabilidades, favorecer la reutilización del codigo y permitir escalar la solucion con mayor facilidad si en el futuro se agregan nuevos endpoints o reglas de negocio.

## Estructura del proyecto

```text
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── README.md
├── .gitignore
├── app.sh                                 # script para start/stop/build/healthcheck
└── project/
    ├── backend/                           # aplicación FastAPI
    │   ├── api/
    │   │   └── v1/
    │   │       ├── endpoints.py
    │   │       ├── schemas/
    │   │       │   └── validator.py
    │   │       ├── services/
    │   │       │   └── validator.py
    │   │       └── utils/
    │   │           └── error_handling.py
    │   ├── config/                       # configuracion de logger y environments
    │   │   ├── default.py
    │   │   ├── logger.py
    │   │   ├── production.py
    │   │   └── test.py
    │   ├── Dockerfile
    │   ├── main.py
    │   └── requirements.txt
    ├── nginx/                             # proxy reverso
    │   ├── Dockerfile
    │   └── nginx.conf
    ├── .dockerignore
    ├── .env.production
    ├── .env.testing
    ├── compose.dev.yaml                   # compose para desarrollo local con reload
    └── compose.yaml                       # compose para despliegue/testing/producción
```

## Levantar el entorno

### Entorno local de desarrollo

Para desarrollo local se utiliza Docker Compose con configuración para reload. En este modo se ejecuta Uvicorn con `reload` y se monta la carpeta de desarrollo para que los cambios se reflejen en tiempo real sin reiniciar manualmente el contenedor.

```bash
chmod +x app.sh
./app.sh start
```

Esto levantará la API en http://localhost:8000

### Entorno de despliegue / testing / producción

El archivo [compose.yaml](compose.yaml) está pensado para despliegue en ambientes remotos de testing o producción. La aplicación se levanta usando la imagen del registry y se utiliza las variables de entorno .env.\<testing-prodction\> respectivamente, estos comandos estan preparados para utilizarse con **GitHub Actions unicamente**.

```bash
./app.sh start --testing
./app.sh start --production
```

## Detener el entorno

```bash
./app.sh stop
```

## Verificar salud del servicio

```bash
./app.sh healthcheck
```

## Endpoints

### GET /api/v1/health

Retorna el estado del servicio.

#### Ejemplo en local

```bash
curl http://localhost:8000/api/v1/health
```

Respuesta esperada:

```json
{
  "status": "healthy",
  "service": "Validator API",
  "environment": "development",
  "version": "1.0.0"
}
```

### POST /api/v1/validate-md5

Recibe un payload JSON y un MD5. El servicio calcula el MD5 del payload completo y compara el resultado con el hash recibido.

#### Request válido

```bash
curl -X POST http://localhost:8000/api/v1/validate-md5 \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": {"name": "Carlitos", "age": 66, "active": True},
    "md5": "dd0670cdfe8bb81517e561d22ad9c236"
  }'
```

#### Ejemplo válido con MD5 calculado localmente

```bash
python3 - <<'PY'
import hashlib, json
payload = {"name": "Carlitos", "age": 66, "active": True}
normalized = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
print(hashlib.md5(normalized.encode('utf-8')).hexdigest())
PY
```

#### Respuesta exitosa

```json
{
  "valid": true,
  "md5": "dd0670cdfe8bb81517e561d22ad9c236"
}
```

#### Request inválido

```bash
curl -X POST http://localhost:8000/api/v1/validate-md5 \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": {"name": "Carlitos", "age": 66, "active": True},
    "md5": "dd0670cdfe8bb81517e561d22ad00000"
  }'
```

Respuesta esperada:

```json
{
  "detail": {
    "message": "MD5 does not match the provided payload"
  }
}
```

## Documentacion Swagger/OpenAPI

La API incluye documentación automática en:

- http://localhost:8000/docs
- http://localhost:8000/redoc

Ademas, se incluye un endpoint del standard OpenApi en forma JSON:

- http://localhost:8000/docs-json

## Calculo del MD5

El algoritmo implementado:

1. Se toma el payload JSON recibido.
2. Se lo normaliza:
   - claves ordenadas (`sort_keys=True`)
   - separadores compactos (`separators=(",", ":")`)
   - codificación UTF-8
3. Se aplica MD5.
4. Se compara con el valor enviado por el cliente.

## Decisiones tecnicas

- Se utilizo FastAPI para construir una API REST simple, rapida y bien documentada.
- La solución sigue una arquitectura por capas para separar responsabilidades y facilitar la evolución del sistema:
  - endpoints: definición de rutas y contratos HTTP
  - services: logica de negocio
  - schemas: validación de requests/responses
  - utils: utilidades comunes
- Para el entorno local de desarrollo se utiliza `docker compose.dev` con Uvicorn en modo `reload` y bind a la carpeta de desarrollo para reflejar cambios en tiempo real.
- El `docker compose` principal esta pensado para despliegue en ambientes de testing o produccion, utilizando imagenes de algun registry, en este caso se uso el personal de Docker HUB santlink.
- Para que el calculo sea determinista, se normaliza el JSON antes de tomar el hash.

## Supuestos y limitaciones

- El endpoint acepta cualquier JSON valido como payload.
- El MD5 esperado debe ser un hash hexadecimal de 32 caracteres.
- Si bien la solucion proteje los datos sensibles como tokens, keys, hosts, entre otros... no incluye otros apartados como la autenticaciion, persistencia, y conexion TLS.
- Los logs estan orientados a desarrollo basica y no incluyen integracion con sistemas de observabilidad.

## Que mejoraria para produccion

- **Despliegue**:
  - usar un orchestrador como Kubernetes o Docker Swarm.
- **Auth**: 
  - se podria utilizar una herramienta que maneje tokens temporales como Keycloak.
- **Rollback**:
  - cambiaria el versionado de imagenes por tags mas sofisticado (`latest`, `stable`, `sha-...`) de manera que facilite el rollback.
- **Observabilidad**:
  - agregar agentes como Cadvisor para obtener metricas.
- **Notificaciones y alertas**:
  - configurar notificaciones y/o alertas por despliegues, latencia, errores,...
- **Secrets**:
  - se puede utilizar otros secrets managers como Vault 
- **Escalabilidad**:
  - agregar replicas en caso de Swarm, vpa o hpa en caso de Kubernetes.
- **Seguridad**:
  - crear keys y habilitar HTTPS.
- **Registry**:
  - publicar imagenes en un registry privado.
- **Recursos**:
  - definir limites de CPU y memoria para un QoS garantizado.

## Links

- https://github.com/santiagomouton/validator-app
- https://github.com/marketplace/actions/docker-metadata-action
