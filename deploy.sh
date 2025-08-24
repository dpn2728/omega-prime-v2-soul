#!/bin/bash

# Step 1: Get short commit SHA
export COMMIT_SHA=$(git rev-parse --short HEAD)
echo "Using commit SHA: $COMMIT_SHA"

# Step 2: Submit Cloud Build
gcloud builds submit --config cloudbuild.yaml .
