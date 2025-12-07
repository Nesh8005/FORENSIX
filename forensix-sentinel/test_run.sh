
# Create some dummy files
echo "Hello World" > test_file_1.txt
echo "This is a secret" > test_file_2.log

# Run the scanner
forensix scan . -r
