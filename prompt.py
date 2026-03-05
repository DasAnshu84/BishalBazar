REFINED_LEDGER_PROMPT="""
**Task:** Analyze the attached handwritten ledger image and extract numerical data into a structured format.
**Data Structure:** 
> * Each line typically has a **Number** on the left and a **Unique ID** (often in brackets like (S.) or (V)) on the right.
**Extraction Logic (The "Bracket Rule"):** 
1. **Single Entries:** If an entry is not bracketed, record the Unique ID and the Amount. 
2. **Bracketed Pairs:** If two entries are connected by a closing square bracket ( ] ), generate **three distinct data points**: 
- **The Sum:** Add the second number to the first and assign it to the first ID (e.g., "Combined 1st + 2nd"). 
- **Original 1:** The first individual ID and its original number. 
- **Original 2:** The second individual ID and its original number.
**Output Requirements:** 
- Provide a **Markdown Table** with columns: [Unique ID | Entry Type | Amount]. 
- Provide a **Summary Table** totaling all amounts by Unique ID. 
- **Verification:** Ensure the sum of all "Original" entries matches the total written at the bottom of the page.
"""