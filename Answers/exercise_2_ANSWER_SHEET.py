"""
===============================================================================
ANSWER SHEET: EXERCISE 2 - CONTAINER BOOKING VALIDATOR
===============================================================================

This is the complete solution with detailed explanations.
Compare your implementation with this after attempting the exercise yourself.

===============================================================================
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

def get_completion(prompt, model="gpt-4o-mini"):
    """Helper function to call OpenAI API"""
    messages = [{"role": "user", "content": prompt}]
    response = client.responses.create(
        model=model,
        input=messages,
        temperature=0
    )
    return response.output_text

# ============================================================================
# VALIDATION RULES DATABASE
# ============================================================================

CONTAINER_RULES = """
CONTAINER TYPE REQUIREMENTS:
- Dry Container: General cargo, non-perishable goods, machinery, textiles
- Reefer Container: Pharmaceuticals, frozen foods, fresh produce, temperature-sensitive cargo
- Open Top: Oversized cargo, machinery exceeding standard height
- Flat Rack: Heavy machinery, vehicles, construction equipment
- Tank Container: Liquid chemicals, oils, hazardous liquids

CONTAINER SIZE CAPACITY:
- 20ft Standard: Max 28 cubic meters, Max 28 tons gross weight
- 40ft Standard: Max 67 cubic meters, Max 30 tons gross weight
- 40ft High Cube: Max 76 cubic meters, Max 30 tons gross weight

REQUIRED DOCUMENTS:
- Dry Cargo: Commercial Invoice, Packing List, Bill of Lading
- Reefer Cargo: Above + Temperature Control Certificate, Quality Certificate
- Hazardous Cargo: Above + MSDS (Material Safety Data Sheet), UN Classification
- Pharma Cargo: Above + GDP Certificate, Cold Chain Compliance Certificate

VALID ROUTES (Origin → Destination):
- JNPT Mumbai → Rotterdam (Netherlands)
- JNPT Mumbai → Hamburg (Germany)
- Chennai → Singapore
- Mundra → Dubai (UAE)
- JNPT Mumbai → New York (USA)
"""

# ============================================================================
# SAMPLE BOOKING REQUESTS FOR TESTING
# ============================================================================

sample_bookings = [
    {
        "booking_id": "BK-2024-001",
        "cargo_type": "Frozen Seafood Products",
        "cargo_volume": "45 cubic meters",
        "cargo_weight": "18 tons",
        "container_type": "40ft Dry Container",
        "origin": "JNPT Mumbai",
        "destination": "Rotterdam",
        "documents_submitted": ["Commercial Invoice", "Packing List"]
    },
    
    {
        "booking_id": "BK-2024-002",
        "cargo_type": "Textile Fabrics",
        "cargo_volume": "72 cubic meters",
        "cargo_weight": "12 tons",
        "container_type": "40ft Standard Container",
        "origin": "Chennai",
        "destination": "Singapore",
        "documents_submitted": ["Commercial Invoice", "Packing List", "Bill of Lading"]
    },
    
    {
        "booking_id": "BK-2024-003",
        "cargo_type": "Temperature-Controlled Vaccines",
        "cargo_volume": "15 cubic meters",
        "cargo_weight": "5 tons",
        "container_type": "20ft Reefer Container",
        "origin": "JNPT Mumbai",
        "destination": "Hamburg",
        "documents_submitted": [
            "Commercial Invoice", 
            "Packing List", 
            "Temperature Control Certificate",
            "GDP Certificate",
            "Bill of Lading",
            "Cold Chain Compliance Certificate"
        ]
    }
]

# ============================================================================
# COMPLETE SOLUTION
# ============================================================================

def validate_booking(booking_data):
    """
    Validate container booking using Chain-of-Thought reasoning.
    
    This solution demonstrates:
    1. Chain-of-Thought prompting with explicit step-by-step instructions
    2. Conditional logic checks (if-then rules)
    3. Using delimiters to separate rules from booking data
    4. Structured output with reasoning visible
    5. Actionable recommendations for error correction
    
    Args:
        booking_data (dict): Booking details including cargo, container, route, docs
    
    Returns:
        str: Validation report with step-by-step reasoning and recommendations
    """
    
    # Convert booking dict to readable format
    booking_text = json.dumps(booking_data, indent=2)
    
    prompt = f"""
You are a container booking validation system for Maersk shipping operations.

Your task is to validate a booking request by checking it against business rules.

CRITICAL INSTRUCTION: You MUST perform validation in the exact order specified below.
Show your reasoning for EACH step before moving to the next step.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION RULES DATABASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
{CONTAINER_RULES}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOOKING REQUEST TO VALIDATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
{booking_text}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION PROCESS - FOLLOW THESE STEPS IN ORDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: CONTAINER TYPE VALIDATION
──────────────────────────────────
Question: Does the container type match the cargo requirements?

Instructions:
1. Look at the cargo_type in the booking
2. Determine what type of cargo this is (perishable/general/hazardous/etc.)
3. Check the CONTAINER TYPE REQUIREMENTS rules
4. Compare: Does the requested container_type match what's required for this cargo?
5. State your reasoning clearly
6. Mark as: ✅ PASS or ❌ FAIL

Show your work:
- Cargo Type: [state what it is]
- Required Container: [based on rules]
- Requested Container: [what customer asked for]
- Match: [yes/no]
- Result: [PASS/FAIL]


STEP 2: CONTAINER SIZE VALIDATION
──────────────────────────────────
Question: Is the container size sufficient for the cargo volume and weight?

Instructions:
1. Look at cargo_volume and cargo_weight in the booking
2. Look at container_type to determine container size
3. Check CONTAINER SIZE CAPACITY rules for this container size
4. Compare cargo volume vs max capacity
5. Compare cargo weight vs max weight
6. BOTH must be within limits to pass

Show your work:
- Container Size: [20ft/40ft/40ft HC]
- Max Capacity: [cubic meters from rules]
- Cargo Volume: [from booking]
- Volume Check: [cargo < max? yes/no]
- Max Weight: [tons from rules]
- Cargo Weight: [from booking]
- Weight Check: [cargo < max? yes/no]
- Result: [PASS if both checks pass, FAIL if either fails]


STEP 3: ROUTE VALIDATION
─────────────────────────
Question: Is the origin → destination route valid?

Instructions:
1. Extract origin and destination from booking
2. Format as "Origin → Destination"
3. Check if this exact route exists in VALID ROUTES list
4. Be precise - route must match exactly

Show your work:
- Requested Route: [origin → destination]
- Checking against valid routes list...
- Found in list: [yes/no]
- Result: [PASS/FAIL]


STEP 4: DOCUMENT VALIDATION
────────────────────────────
Question: Are all required documents submitted?

Instructions:
1. Determine cargo type (Dry/Reefer/Hazardous/Pharma)
2. Look up required documents for this cargo type in REQUIRED DOCUMENTS rules
3. List all required documents
4. Check which documents were submitted
5. Identify any missing documents
6. Count total missing

Show your work:
- Cargo Category: [Dry/Reefer/Hazardous/Pharma]
- Required Documents: [list all required]
- Submitted Documents: [list what was provided]
- Missing Documents: [list any missing, or "None"]
- Result: [PASS if none missing, FAIL if any missing]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL VALIDATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After completing all 4 steps above, provide:

OVERALL VERDICT: [✅ APPROVED or ❌ REJECTED]

If REJECTED, list:
ERRORS FOUND:
1. [Specific error from failed step]
2. [Another error if multiple failures]

RECOMMENDED ACTIONS:
1. [Specific fix with details]
2. [Another fix if needed]

If APPROVED:
State: "All validation checks passed. Booking approved for processing."


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPORTANT REMINDERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Show your reasoning for EVERY step
- Complete all 4 steps even if early steps fail
- Be specific in error descriptions
- Provide actionable corrections, not vague suggestions
- Use the exact format shown above for consistency
"""
    
    # Get validation response
    response = get_completion(prompt)
    return response

# ============================================================================
# TEST THE SOLUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("CONTAINER BOOKING VALIDATOR - COMPLETE SOLUTION")
    print("="*80)
    
    for i, booking in enumerate(sample_bookings, 1):
        print(f"\n📦 BOOKING {i}: {booking['booking_id']}")
        print("-" * 80)
        print(f"Cargo: {booking['cargo_type']}")
        print(f"Container: {booking['container_type']}")
        print(f"Route: {booking['origin']} → {booking['destination']}")
        print(f"Volume: {booking['cargo_volume']}, Weight: {booking['cargo_weight']}")
        print("-" * 80)
        
        # Validate the booking
        validation_report = validate_booking(booking)
        
        print("\n🔍 VALIDATION REPORT:")
        print(validation_report)
        print("\n" + "="*80)
        
        # Wait for user to read before next booking
        if i < len(sample_bookings):
            print("\nPress Enter to continue to next booking...")
            input()

# ============================================================================
# EXPLANATION OF KEY TECHNIQUES USED
# ============================================================================
"""
1. CHAIN-OF-THOUGHT (CoT) PROMPTING:
   - Explicit step-by-step instructions (4 steps)
   - Each step has clear sub-instructions
   - Model must "show work" before concluding
   - Prevents rushing to judgment
   - Forces systematic reasoning
   
   Why it matters: Complex validation has many failure modes. Without CoT,
   the model might check one thing, see an error, and stop. CoT ensures
   ALL checks are performed and documented.

2. STRUCTURED REASONING FORMAT:
   - "Show your work" section for each step
   - Predefined format: Question → Instructions → Show Work → Result
   - Consistent structure makes output parseable
   - Easy to audit and debug
   
3. CONDITIONAL LOGIC:
   - "If both checks pass → PASS, else → FAIL"
   - "If route exists in list → PASS"
   - "If any documents missing → FAIL"
   - Models can follow if-then rules reliably
   
4. DELIMITERS:
   - Rules database in ``` blocks
   - Booking data in ``` blocks
   - Separates instructions from data
   - Prevents contamination between sections
   
5. EXPLICIT ORDERING:
   - "MUST perform validation in exact order"
   - "Complete all 4 steps even if early steps fail"
   - Ensures comprehensive validation
   - No shortcuts or early termination
   
6. ACTIONABLE OUTPUTS:
   - Don't just say "wrong container"
   - Say "Change from 40ft Dry to 40ft Reefer"
   - List specific missing documents
   - Provide exact corrections needed

7. VISUAL FORMATTING:
   - Unicode box drawing characters (━, ─)
   - Emoji indicators (✅, ❌)
   - Clear section headers
   - Makes output human-readable
"""

# ============================================================================
# REFLECTION QUESTIONS - ANSWERS
# ============================================================================
"""
1. Why is step-by-step reasoning important for complex validation tasks?
   
   ANSWER: Complex validation has multiple independent checks that can fail
   in different combinations. Step-by-step reasoning ensures:
   - ALL checks are performed (no shortcuts)
   - Errors are caught at the right level
   - Reasoning is auditable (compliance/debugging)
   - Multiple errors are all identified (not just first one)
   - Clear traceability of WHY something failed
   
   Without steps, model might see "frozen seafood" + "dry container" and
   immediately say "rejected" without checking size, route, or documents.
   With steps, you get a complete diagnostic report.

2. How does Chain-of-Thought help the model avoid rushing to conclusions?
   
   ANSWER: CoT breaks the task into smaller, manageable pieces. Each piece
   requires explicit reasoning before moving forward. This prevents:
   - Pattern matching errors (e.g., "seafood = reefer" without checking)
   - Confirmation bias (finding one error and stopping)
   - Skipping validation steps
   - Missing edge cases
   
   By forcing "show your work" at each step, the model can't jump to
   conclusions. It must build up evidence systematically.

3. What happens if you skip providing the rules database to the model?
   
   ANSWER: Without rules database:
   - Model relies on general knowledge (may be outdated or wrong)
   - Container capacities could be guessed incorrectly
   - Route validation would be based on geography, not actual service routes
   - Document requirements might be generic customs rules, not company policy
   - No consistency across validations (different assumptions each time)
   
   The rules database ensures:
   - Consistent, company-specific validation
   - Accurate capacity/weight limits
   - Only approved routes are validated
   - Correct document requirements per cargo type

4. How would you extend this to validate pricing or customs regulations?
   
   ANSWER: Add new validation steps:
   
   STEP 5: PRICING VALIDATION
   - Add pricing rules database (per route, container type, cargo type)
   - Check if quoted price matches pricing matrix
   - Validate discounts are within authorized limits
   - Check for surcharges (fuel, peak season, hazardous)
   
   STEP 6: CUSTOMS COMPLIANCE
   - Add customs regulations database per destination country
   - Check HS code validity
   - Verify restricted/prohibited goods rules
   - Validate import license requirements
   - Check if special permits are needed
   
   STEP 7: INSURANCE REQUIREMENTS
   - Check if cargo value requires insurance
   - Validate insurance coverage type matches cargo
   - Verify insurance limits are sufficient
   
   Each step follows same CoT format: Question → Instructions → Reasoning → Result
"""

# ============================================================================
# PRODUCTION TIPS
# ============================================================================
"""
For production deployment, consider:

1. PERFORMANCE OPTIMIZATION:
   - Pre-validation: Check basic fields before calling LLM
   - Caching: Store validation results for identical bookings
   - Parallel processing: Validate multiple bookings concurrently
   - Streaming: Stream validation results step-by-step for UX

2. ERROR RECOVERY:
   - Retry logic for API failures
   - Fallback to rule-based validation if LLM unavailable
   - Queue failed validations for manual review
   - Log all validations for audit trail

3. VALIDATION ACCURACY:
   - Track validation accuracy vs human review
   - A/B test different prompt versions
   - Maintain golden test set of bookings
   - Regularly update rules database
   - Version control prompts and rules

4. USER EXPERIENCE:
   - Return validation results within 2 seconds
   - Highlight errors in booking form UI
   - Provide "auto-fix" suggestions where possible
   - Allow override with manager approval

5. INTEGRATION:
   - API endpoint for validation service
   - Webhook for async validation results
   - Database logging of all validations
   - Dashboard for validation metrics
   - Alert on unusual validation patterns

6. COMPLIANCE & AUDIT:
   - Log full prompt + response for each validation
   - Store reasoning trail for regulatory compliance
   - Version tracking for rules changes
   - Audit reports showing why bookings were rejected
   - Explainability for customer disputes

7. CONTINUOUS IMPROVEMENT:
   - Collect feedback on false positives/negatives
   - Update few-shot examples based on edge cases
   - Add new validation rules as business evolves
   - Monitor validation step failure rates
   - Optimize prompt for cost and latency
"""

# ============================================================================
# BONUS CHALLENGE - ADVANCED VALIDATIONS
# ============================================================================
"""
Here are implementations for the bonus challenges:

CHALLENGE 1: Weight Distribution
Add to prompt:
"STEP 5: WEIGHT DISTRIBUTION VALIDATION
- Calculate weight per cubic meter (cargo_weight / cargo_volume)
- For seafood/produce: density should be 0.3-0.6 tons/m³
- For textiles: density should be 0.1-0.3 tons/m³
- For machinery: density can be 0.8-2.0 tons/m³
- Flag if density is unusual (may indicate mis-measurement)"

CHALLENGE 2: Temperature Range for Reefer
Add temperature field to booking:
"required_temperature": "-20°C"

Add to rules:
"TEMPERATURE REQUIREMENTS:
- Vaccines: -20°C to -80°C
- Frozen seafood: -18°C to -25°C
- Fresh produce: +2°C to +8°C
- Pharmaceuticals: +2°C to +8°C or -20°C (depends on product)"

Add validation step:
"STEP 6: TEMPERATURE VALIDATION (if Reefer)
- Check if required_temperature matches cargo type requirements
- Verify container can achieve required temperature
- Flag if temperature is outside typical range"

CHALLENGE 3: Hazardous Cargo UN Codes
Add to booking:
"un_code": "UN1203" (if hazardous)
"hazard_class": "3" (flammable liquids)

Add validation:
"STEP 7: HAZMAT VALIDATION
- If cargo is hazardous, verify UN code is provided
- Check UN code format (UN + 4 digits)
- Verify hazard class matches UN code
- Check if MSDS document is submitted
- Verify container type allows hazmat (tank/special)"

CHALLENGE 4: Customs by Destination
Add to rules database:
"DESTINATION CUSTOMS RULES:
- Netherlands (Rotterdam):
  * Requires EUR1 certificate for preferential tariff
  * Phytosanitary cert for agricultural products
  * CE marking for electronics
  
- Germany (Hamburg):
  * Same as Netherlands (EU rules)
  
- Singapore:
  * Strategic goods permit for tech/electronics
  * Halal certificate for food products
  * No import license for most general cargo"

Add validation step:
"STEP 8: DESTINATION CUSTOMS CHECK
- Identify destination country
- Check cargo type against country-specific rules
- Verify required certificates are submitted
- Flag missing destination-specific documents"

CHALLENGE 5: Transit Time vs Deadline
Add to booking:
"customer_required_date": "2024-12-01"

Add to rules:
"TRANSIT TIMES:
- JNPT Mumbai → Rotterdam: 18-22 days
- JNPT Mumbai → Hamburg: 20-24 days
- Chennai → Singapore: 5-7 days
- Mundra → Dubai: 7-10 days"

Add validation:
"STEP 9: DELIVERY DEADLINE CHECK
- Calculate: loading_date + transit_time = estimated_arrival
- Compare estimated_arrival vs customer_required_date
- Add 2 days buffer for customs clearance
- Flag if deadline cannot be met
- Suggest air freight if significant delay"

Each challenge adds a new validation dimension while maintaining the
Chain-of-Thought structure. The key is keeping each step focused on
ONE specific check with clear pass/fail criteria.
"""
