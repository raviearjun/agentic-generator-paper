#!/bin/bash
# run_all_experiments.sh
# Runs the full prompt ablation experiment for all frameworks, prompts, and models.
#
# Prerequisites:
#   export OPENAI_API_KEY="sk-..."
#   export GEMINI_API_KEY="AIza..."
#   export ANTHROPIC_API_KEY="sk-ant-..."
#   pip install openai google-generativeai anthropic rdflib
#
# Usage:
#   bash Script/run_all_experiments.sh              # full run
#   bash Script/run_all_experiments.sh --dry-run    # preview without API calls

set -e
cd "$(dirname "$0")/.."   # repo root

DRY_RUN=""
FILTER_FRAMEWORK=""
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN="--dry-run"; echo "DRY RUN MODE — no API calls will be made" ;;
        --framework=*) FILTER_FRAMEWORK="${arg#--framework=}" ;;
    esac
done

ALL_FRAMEWORKS=("CrewAI" "LangGraph" "AutoGen" "Mastra AI")
if [[ -n "$FILTER_FRAMEWORK" ]]; then
    FRAMEWORKS=("$FILTER_FRAMEWORK")
else
    FRAMEWORKS=("${ALL_FRAMEWORKS[@]}")
fi
PROMPTS=("P0" "P1" "P2" "P3" "P4" "P5")
MODELS=("chatgpt" "gemini" "claude")

for FRAMEWORK in "${FRAMEWORKS[@]}"; do
    for PROMPT in "${PROMPTS[@]}"; do
        for MODEL in "${MODELS[@]}"; do
            echo "========================================="
            echo "Framework: $FRAMEWORK  Prompt: $PROMPT  Model: $MODEL"
            echo "========================================="
            python3 Script/run_experiment.py \
                --framework    "$FRAMEWORK" \
                --prompt       "$PROMPT" \
                --model        "$MODEL" \
                --max-examples 5 \
                $DRY_RUN
        done
    done
done

echo ""
echo "All experiments complete."
echo "Run evaluation with: python3 Script/evaluate_kg.py"
