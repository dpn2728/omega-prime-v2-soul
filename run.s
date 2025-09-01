#!/bin/bash
docker run --rm \
  --env-file <(grep -v '^#' .env | xargs) \
  omega-prime "$@"
