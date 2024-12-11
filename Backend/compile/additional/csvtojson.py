
from django.http import JsonResponse
import json
import csv

def csv_to_json(csv_file, output_json_path):

    problems = []  # List to store the problems

    try:
        # Read the CSV file
        csvfile = csv_file.read().decode('utf-8').splitlines()  # Decode and split the CSV lines
        reader = csv.DictReader(csvfile)  # Use DictReader for easier column access

        # Validate CSV headers
        expected_headers = {'id', 'title', 'level', 'problem_statement',}
        if not expected_headers.issubset(reader.fieldnames):
            return JsonResponse({'error': 'CSV missing required headers'}, status=400)

        for row in reader:
            problem = {
                'id': int(row['id']),
                'title': row['title'],
                'level': row['level'],
                'problem_statement': row['problem_statement'],
                'samples': [],
                'hidden_samples': [],
                # 'marks':int(row['marks'])
            }

            # Append sample inputs and outputs
            for i in range(1, 5):  # Four sample inputs
                sample_input_key = f'sample_input_{i}'
                sample_output_key = f'sample_output_{i}'
                if sample_input_key in row and sample_output_key in row:
                    if row[sample_input_key] and row[sample_output_key]:
                        problem['samples'].append({
                            'input': row[sample_input_key].split(','),  # Split input on comma
                            'output': row[sample_output_key]
                        })

            # Append hidden sample inputs and outputs
            for i in range(1, 11):  # Ten hidden samples
                hidden_input_key = f'hidden_input_{i}'
                hidden_output_key = f'hidden_output_{i}'
                if hidden_input_key in row and hidden_output_key in row:
                    if row[hidden_input_key] and row[hidden_output_key]:
                        problem['hidden_samples'].append({
                            'input': row[hidden_input_key].split(','),  # Split input on comma
                            'output': row[hidden_output_key]
                        })

            problems.append(problem)  # Add the problem to the list

        # Write the output to JSON file
        with open(output_json_path, 'w') as jsonfile:
            json.dump({'problems': problems}, jsonfile, indent=4)  # Dump problems to JSON file

        return JsonResponse({'message': 'File processed successfully', 'output_file': output_json_path}, status=200)

    except csv.Error as e:
        return JsonResponse({'error': f'CSV error: {str(e)}'}, status=400)
    except IOError as e:
        return JsonResponse({'error': f'I/O error: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)