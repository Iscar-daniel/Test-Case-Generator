from flask import Flask, render_template, request, jsonify
import openai
import os
from datetime import datetime
import json

app = Flask(__name__)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_test_cases(prompt):
    """Generate test cases using OpenAI API"""
    try:
        system_prompt = """You are a QA expert. Generate test cases based on the user's prompt. 
        Return the response in JSON format with the following structure:
        {
            "test_cases": [
                {
                    "no": 1,
                    "scenario_name": "Test scenario name",
                    "steps_to_reproduce": "Step 1. Step 2. Step 3.",
                    "expected_result": "Expected outcome"
                }
            ]
        }
        
        Make sure to:
        1. Create realistic and comprehensive test scenarios
        2. Include positive and negative test cases
        3. Make steps clear and actionable
        4. Ensure expected results are specific and measurable
        5. Generate 3-5 test cases per prompt"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate test cases for: {prompt}"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Parse the response
        content = response.choices[0].message.content
        try:
            # Try to parse as JSON
            return json.loads(content)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a fallback structure
            return {
                "test_cases": [
                    {
                        "no": 1,
                        "scenario_name": "Basic functionality test",
                        "steps_to_reproduce": "1. Enter the provided prompt\n2. Click generate\n3. Review results",
                        "expected_result": "Test cases are generated successfully"
                    }
                ]
            }
            
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    result = generate_test_cases(prompt)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)