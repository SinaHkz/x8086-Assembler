from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/assembler', methods=['POST'])
def run_script():
    data = request.json
    input_data = data['input']
    # input_data = request.data.decode('utf-8')
    with open('inputs.txt', 'w') as f:
        f.write(input_data)

    # Execute your Python script with the input
    result = subprocess.check_output(['python', 'main.py', input_data], universal_newlines=True)
    return jsonify({'output': result})


if __name__ == '__main__':
    app.run(debug=True)
