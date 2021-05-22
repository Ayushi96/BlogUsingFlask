from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    user = 'Ayushi'
    return render_template('index.html', name=user)

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/armstrong/<int:n>')
def armstrong(n):
    # n = int(input("Enter the number "))
    sum = 0 
    order = len(str(n))
    copy_n = n
    
    while(n > 0):
        d = n%10
        sum += d ** order
        n = n//10
    print(f"sum = {sum}")
    if copy_n == sum:
        print(f"{copy_n} is an armstrong number")
        result = {
            "Number": copy_n, 
            "Armstrong": True,
            "Author": "Ayushi"
        }
    else:
        print(f"{copy_n} is not an armstrong number")
        result = {
            "Number": copy_n, 
            "Armstrong": False,
            "Author": "Ayushi"
        }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


