from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            size = int(request.form['size'])
            matrix_a = []
            matrix_b = []

            for i in range(size):
                row = [int(request.form[f'a{i}{j}']) for j in range(size)]
                matrix_a.append(row)

            for i in range(size):
                row = [int(request.form[f'b{i}{j}']) for j in range(size)]
                matrix_b.append(row)

            # Matrix multiplication
            result = []
            for i in range(size):
                row = []
                for j in range(size):
                    sum = 0
                    for k in range(size):
                        sum += matrix_a[i][k] * matrix_b[k][j]
                    row.append(sum)
                result.append(row)
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
