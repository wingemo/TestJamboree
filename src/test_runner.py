import unittest
import subprocess
import json
from jsonschema import validate, ValidationError
from your_module_name import create_stylish_table

class TestWholeProgram(unittest.TestCase):

    def setUp(self):
        # Läs in testdata från JSON-konfigurationsfilen
        with open('test_config.json', 'r') as config_file:
            self.test_data = json.load(config_file)

        # Läs in JSON-schema för validering
        with open('test_config_schema.json', 'r') as schema_file:
            self.schema = json.load(schema_file)

        # Validera JSON-filen mot schemat
        try:
            validate(self.test_data, self.schema)
        except ValidationError as e:
            raise Exception(f"Invalid test configuration file: {e.message}")

    def run_test(self, test_data):
        test_name = test_data["name"]
        input_data = test_data["input_data"]

        if "expected_output" in test_data:
            expected_output = test_data["expected_output"]
            result = subprocess.check_output(['python', 'your_script_name.py'] + input_data.split(), universal_newlines=True)
            self.assertEqual(result, expected_output, f"{test_name} output does not match expected output.")
        elif "error_message" in test_data:
            error_message = test_data["error_message"]
            with self.assertRaises(ValueError) as context:
                create_stylish_table(input_data)
            self.assertEqual(str(context.exception), error_message, f"{test_name} error message does not match expected error message.")
        elif "log_message" in test_data:
            log_message = test_data["log_message"]
            with self.assertLogs() as log:
                create_stylish_table(input_data)
                self.assertIn(log_message, log.output, f"{test_name} log message not found.")

    def test_all_tests(self):
        for test_data in self.test_data["tests"]:
            with self.subTest(test_name=test_data["name"]):
                self.run_test(test_data)

if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=unittest.TextTestResult, stream=open('test_result/test_results.txt', 'w')))
