#!/usr/bin/env bash
# Validate that the provisioning issue is closed within the time-out window
# Args: 1 = issue URL (or number), 2 = <owner>/<repo> that hosts the issue

set -e
issue_detail="$1"
sq_repo="$2"

issue_number=$(basename "$issue_detail")
issue_state=$(gh issue view "$issue_number" -R "$sq_repo" --json state -q .state)

time_limit=420      # 7 minutes
while [[ "$issue_state" != "CLOSED" && $time_limit -gt 0 ]]; do
  sleep 10
  time_limit=$((time_limit-10))
  issue_state=$(gh issue view "$issue_number" -R "$sq_repo" --json state -q .state)
done

if [[ "$issue_state" != "CLOSED" ]]; then
  echo "info=sqfailure" >> "$GITHUB_OUTPUT"
  exit 1
fi
