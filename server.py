from flask import Flask, render_template, send_from_directory, url_for, request, redirect
import os
import csv
app = Flask(__name__) #We are creating an instance of a Flask app
print(__name__) #returns __main__


@app.route('/') #this decorator gives us extra tools to build the server, here it says that every time / is typed, this function will be run
def my_home(): #defaults to None
    return render_template('index.html')

@app.route('/<string:page_name>') #this decorator gives us extra tools to build the server, here it says that every time / is typed, this function will be run
def html_page(page_name): #defaults to None
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode='a') as database: #a is append mode (adding to the file)
        email=data['email']
        subject=data['subject']
        message = data['message']
        file=database.write(f'\n{email}, {subject}, {message}')

def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2: #a is append mode (adding to the file)
        email=data['email']
        subject=data['subject']
        message = data['message']
        csv_writer=csv.writer(database2, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

"""
@app.route('/<username>/<int:post_id>') #if the route is /anyGivenName/anyGivenNumber
def hello_world2(username=None, post_id=None): #defaults to None (if these values are not given in the html)
    return render_template('index.html', name=username, post_id=post_id) #means that the index.html will look for {{name}} and {{post_id}} values in the html body when this route is accessed
"""

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method=='POST':
        try:
            data=request.form.to_dict() #turns the form data into a dictionary
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'Error: save to database failed'
    else:
        return 'something went wrong, try again'

@app.route('/favicon.ico')
def favicon():
    print('Test me: ', app.root_path)
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


"""
Example code from internet
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
"""