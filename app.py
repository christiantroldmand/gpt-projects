from flask import Flask, render_template, request, redirect, url_for, send_file
import subprocess
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    username = request.form['username']
    result_file = f"results_{time.time()}.txt"
    run_sherlock(username, result_file)
    return redirect(url_for('results', filename=result_file))

@app.route('/results/<filename>')
def results(filename):
    try:
        with open(filename, 'r') as f:
            output = f.read()
        return render_template('results.html', output=output)
    except FileNotFoundError:
        return render_template('results.html', output="Results not found")
        
@app.route('/download_csv/<filename>')
def download_csv(filename):
    return send_file(filename, as_attachment=True)

def run_sherlock(username, result_file):
    try:
        command = ['sherlock', username, '--output', result_file]
        subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        with open(result_file, 'w') as f:
            f.write(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
