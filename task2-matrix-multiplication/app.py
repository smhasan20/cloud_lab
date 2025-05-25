from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    size = None

    if request.method == 'POST':
        if 'size' in request.form and 'submit_size' in request.form:
            # Step 1: user just submitted the size of matrix
            try:
                size = int(request.form['size'])
                if size < 1:
                    error = "Matrix size must be at least 1."
            except:
                error = "Invalid matrix size."
        
        elif 'submit_matrices' in request.form:
            # Step 2: user submitted the matrix elements for multiplication
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
                        s = 0
                        for k in range(size):
                            s += matrix_a[i][k] * matrix_b[k][j]
                        row.append(s)
                    result.append(row)
            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template('index.html', size=size, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
