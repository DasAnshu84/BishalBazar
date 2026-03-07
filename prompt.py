REFINED_LEDGER_PROMPT="""
**Task:** Analyze the attached handwritten ledger image and extract the numerical data into the provided strict JSON structure.

**Data Structure & Layout:** * Each line typically features a **Number** on the left and a **Unique ID** (usually enclosed in brackets like `(S.)`, `(V)`) on the right.

**Extraction Logic (The "Bracket Rule"):** Scan the document line by line and apply the following rules:

1. **Single Entries (No Bracket):** * **unique_id:** Record the ID.
   * **breakdown:** Write the original number as a string (e.g., "50").
   * **total_amount:** Output the exact same number.

2. **Bracketed Pairs (The Addition Rule):** If two entries (ID_1 and ID_2) are linked by a closing square bracket `]`:
   * **For ID_1 (The Top Entry):** * **breakdown:** Write the exact addition formula combining its original number and the second entry's number (e.g., "50 + 20").
     * **total_amount:** Calculate and output the mathematical sum of that breakdown (e.g., 70).
   * **For ID_2 (The Bottom Entry):** * **breakdown:** Write its original number as a string (e.g., "20").
     * **total_amount:** Output that same original number (e.g., 20).

**Calculation Order:**
You MUST populate the `breakdown` string first, and then calculate the `total_amount` strictly based on the numbers you just wrote in the breakdown. 

**Page Verification:**
After processing all individual entries, look for the grand total handwritten at the bottom of the page. Record this in `written_page_total`. Then, independently add up all the original individual numbers and record the result in `calculated_page_total` to verify accuracy.
"""