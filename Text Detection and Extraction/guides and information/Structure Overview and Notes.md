# Structure Overview and Notes
## Steps of execution
1. Landing Page
2. 3 Options:
	a. Extract Text (OCR Only or Vision AI Only)
	b. Directly Extract Key-Value Pairs (Vision AI Only)
	c. Extract Text and then extract Key-Value Pairs (OCR + Vision AI models)
3. Stages in in 2a:
	a. Upload Image(s)
	b. Select Model(s)
	c. Processing (I/p = Images/documents, O/p: Plain extracted Text)
	d. Results
4. Stages in 2b:
	a. Upload Image(s)
	b. Select Model(s)
	c. Processing (I/p = Images/documents, O/p: Extracted Key-value pairs in CSV or JSON format)
	d. Results
5. Stages in 2c:
	a. Upload Image(s)
	b. Select OCR models and Select AI models 
	c. OCR Processing (I/p = Images / documents, O/p: Plain extracted Text)
	d. OCR Results
	e. AI Processing (I/p = Images/documents + Plain extracted Text, O/p: Extracted Key-value pairs in CSV or JSON format)
	f. Final Results
6. Profile Page - displaying all the previous jobs and thier results.

**Note:** CSVs can be displayed in table format on the website.