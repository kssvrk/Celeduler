import psutil
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/ram')
def free_ram():
    # get the memory details
    svmem = psutil.virtual_memory()
    free=svmem.available
    return jsonify({'ram':free})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4431, debug=True)