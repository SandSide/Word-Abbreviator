# Word-Abbreviator
 
This project is a word abbreviator. 

Given a file with lines of strings, for each line, it will try to find suitable 3 letter abbreviators.

For each line:
- Special characters are ignored
- Find all possible 3 letter abbreviations
- If the abbreviation can appear for any other line, it gets ignored
- Each abbreviation is scored, and only the ones sharing the same minium score are considered as a suitable abbreviation for the line

All suitable abbreviations are stored in a file
- If no suitable abbreviation was found, it appears blank


