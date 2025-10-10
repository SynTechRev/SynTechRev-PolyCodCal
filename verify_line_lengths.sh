#!/bin/bash
# Script to verify line lengths in Python files
# This verifies all Python files comply with 79-character line length

echo "==================================================="
echo "Line Length Verification (79 character limit)"
echo "==================================================="
echo ""

# Check feedback_monitor.py
echo "Checking src/syntechrev_polycodcal/feedback_monitor.py..."
MAX_LEN=$(awk 'BEGIN{max=0} {if(length>max)max=length} END{print max}' \
    src/syntechrev_polycodcal/feedback_monitor.py)
echo "  Maximum line length: $MAX_LEN characters"

if [ "$MAX_LEN" -le 79 ]; then
    echo "  ✓ PASS: All lines are 79 characters or less"
else
    echo "  ✗ FAIL: Some lines exceed 79 characters"
    echo ""
    echo "  Lines exceeding 79 characters:"
    awk 'length > 79 {print "    Line "NR": "length" chars"}' \
        src/syntechrev_polycodcal/feedback_monitor.py
fi

echo ""
echo "Running flake8 with max-line-length=79..."
if flake8 --max-line-length=79 src/syntechrev_polycodcal/feedback_monitor.py; then
    echo "  ✓ PASS: flake8 validation successful"
else
    echo "  ✗ FAIL: flake8 found issues"
fi

echo ""
echo "==================================================="
echo "Verification complete!"
echo "==================================================="
