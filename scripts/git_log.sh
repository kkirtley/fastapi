#!/bin/bash
echo "=== February 2025 Git Summary ==="
echo "Commits:"
git log --since="2025-03-24" --until="2025-03-31" --pretty=format:"%h - %an, %ad : %s"
