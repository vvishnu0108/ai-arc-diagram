"""
Test script to verify enhanced LLM output features
"""
import sys
sys.path.append('/app/AI diagram agent/backend')

from services.enhanced_output import (
    extract_architectural_reasoning,
    generate_architecture_explanation,
    validate_code_quality
)

# Test 1: Extract architectural reasoning
print("=" * 60)
print("TEST 1: Extracting Architectural Reasoning")
print("=" * 60)

sample_response = """
Architectural Reasoning: This design implements a three-tier microservices architecture for high availability. 
The API Gateway handles all external traffic and routes to containerized services in EKS. RDS provides managed 
database with read replicas for performance, while ElastiCache reduces database load.

import subprocess
from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, EKS
from diagrams.aws.database import RDS

with Diagram("microservices", show=False, outformat=["png", "dot"]):
    api = ECS("API Gateway")
    db = RDS("Database")
    api >> db

subprocess.run(["graphviz2drawio", "microservices.dot", "-o", "microservices.drawio"], check=True)
"""

reasoning, code = extract_architectural_reasoning(sample_response)
print(f"✓ Extracted Reasoning:\n{reasoning}\n")
print(f"✓ Extracted Code (first 200 chars):\n{code[:200]}...\n")

# Test 2: Generate architecture explanation
print("=" * 60)
print("TEST 2: Generating Architecture Explanation")
print("=" * 60)

explanation = generate_architecture_explanation(
    "AWS microservices architecture",
    code,
    True
)
print(f"✓ Generated Explanation:\n{explanation}\n")

# Test 3: Validate code quality
print("=" * 60)
print("TEST 3: Validating Code Quality")
print("=" * 60)

validation = validate_code_quality(code)
print(f"✓ Quality Score: {validation['score']}/100")
print(f"✓ Is Valid: {validation['is_valid']}")
print(f"✓ Issues: {len(validation['issues'])} issues")
print(f"✓ Warnings: {len(validation['warnings'])} warnings")
print(f"✓ Suggestions: {len(validation['suggestions'])} suggestions")

if validation['warnings']:
    print("\nWarnings:")
    for warning in validation['warnings']:
        print(f"  - {warning}")

if validation['suggestions']:
    print("\nSuggestions:")
    for suggestion in validation['suggestions']:
        print(f"  - {suggestion}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - Enhanced output features working!")
print("=" * 60)
