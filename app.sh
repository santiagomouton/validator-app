#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./app.sh start [--testing|--produccion]
  ./app.sh stop [--testing|--produccion]
  ./app.sh build
  ./app.sh healthcheck

Options for start/stop:
  --testing       compose.yaml + .env.testing
  --produccion    compose.yaml + .env.production

Commands:
  start           Start local development
  stop            Stop local development
  build           Build development images
  healthcheck     Run health check http://127.0.0.1:8000/api/v1/health
EOF
}

require_docker_compose() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is not installed." >&2
    exit 1
  fi
}

run_healthcheck() {
  echo -e "Starting health checks every 5s.\n"
  while true; do
    if curl -fsS --max-time 3 "http://127.0.0.1:8000/api/v1/health" >/tmp/validator-health.out 2>/tmp/validator-health.err; then
      cat /tmp/validator-health.out
      echo -e "\nHealth check OK\n"
    else
      cat /tmp/validator-health.err 2>/dev/null || true
      echo -e "\nHealth check FAILED\n"
    fi
    sleep 5
  done
}

compose_file="compose.dev.yaml"
env_file=""

case "${1:-help}" in
  start)
    require_docker_compose
    if [[ "${2:-}" == "--testing" ]]; then
      compose_file="compose.yaml"
      env_file=".env.testing"
    elif [[ "${2:-}" == "--produccion" ]]; then
      compose_file="compose.yaml"
      env_file=".env.production"
    else
      compose_file="compose.dev.yaml"
      env_file=""
    fi
    docker compose -f project/"$compose_file" up --build -d
    ;;
  stop)
    require_docker_compose
    if [[ "${2:-}" == "--testing" || "${2:-}" == "--produccion" ]]; then
      docker compose -f project/compose.yaml down
    else
      docker compose -f project/compose.dev.yaml down
    fi
    ;;
  build)
    require_docker_compose
    docker compose -f project/compose.dev.yaml build
    ;;
  healthcheck)
    shift || true
    run_healthcheck
    ;;
  help)
    usage
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac
