# Problem:
What happens when you've got some company CIK's and you've got some 13F-HR's you want to throw into spreadsheets?

[Write code in Python that parses fund holdings pulled from EDGAR, given a ticker or CIK, and generates a .tsv file from them.]
# Solution: 
You use this code!

[Parses through the given CIK's and outputs the 13F-HR into a (CIK ACC No).tsv file.]

## Requirements
 - pandas
 - beautifulsoup
 - lxml
 - pytest (if you're curious)


## Usage
1. Obtain a valid CIK number from http://morningstar.com/
(Example CIK is 0001166559 and its subsequent 0001166559_13F-HR.tsv)
2. Pass your CIK into the script.
3. Let the magic happen and check the folder.


## Challenges
1. Some 13F files use different fields. This script checks for the fields first, adds them to the headers, and then populates those headers with the appropriate information. 

2. Parsing can take some time for larger 13-F.

3. Tests and program could use refactoring for me test-friendly methods.

####
When making changes; make sure to run pytest regularly.