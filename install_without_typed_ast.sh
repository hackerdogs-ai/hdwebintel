#!/bin/bash
# Script to install Python packages while skipping typed-ast (incompatible with Python 3.13+)
# This script installs packages individually, skipping any that require typed-ast

REQUIREMENTS_FILE="${1:-requirements.txt}"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Error: $REQUIREMENTS_FILE not found"
    echo "Usage: $0 [requirements-file]"
    exit 1
fi

echo "Installing packages from $REQUIREMENTS_FILE..."
echo "Note: Packages requiring typed-ast will be skipped (incompatible with Python 3.13+)"
echo ""

# Track success/failure
SUCCESS_COUNT=0
SKIP_COUNT=0
FAIL_COUNT=0

# Install packages one by one
while IFS= read -r package || [ -n "$package" ]; do
    # Skip comments and empty lines
    [[ "$package" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${package// }" ]] && continue
    
    # Remove version specifiers for checking
    PACKAGE_NAME=$(echo "$package" | sed 's/[<>=!].*//' | xargs)
    
    echo -n "Installing $PACKAGE_NAME... "
    
    # Try to install and capture output
    INSTALL_OUTPUT=$(pip install "$package" 2>&1)
    INSTALL_EXIT=$?
    
    # Check if the error is related to typed-ast
    if echo "$INSTALL_OUTPUT" | grep -qi "typed-ast\|Failed building wheel for typed-ast"; then
        echo "⊘ SKIPPED (requires typed-ast)"
        SKIP_COUNT=$((SKIP_COUNT + 1))
    elif [ $INSTALL_EXIT -eq 0 ]; then
        echo "✓ SUCCESS"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "✗ FAILED"
        echo "  Error: $(echo "$INSTALL_OUTPUT" | tail -1)"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
done < "$REQUIREMENTS_FILE"

echo ""
echo "=========================================="
echo "Installation Summary:"
echo "  ✓ Successful: $SUCCESS_COUNT"
echo "  ⊘ Skipped (typed-ast): $SKIP_COUNT"
echo "  ✗ Failed: $FAIL_COUNT"
echo "=========================================="

if [ $SKIP_COUNT -gt 0 ]; then
    echo ""
    echo "Note: Some packages were skipped because they require typed-ast."
    echo "These packages are incompatible with Python 3.13+."
    echo "If you need these packages, consider:"
    echo "  1. Using Python 3.11 or 3.12"
    echo "  2. Finding alternative packages that don't require typed-ast"
    echo "  3. Waiting for package maintainers to update their dependencies"
fi

if [ $FAIL_COUNT -gt 0 ]; then
    echo ""
    echo "Warning: Some packages failed to install. Check the errors above."
    exit 1
fi

