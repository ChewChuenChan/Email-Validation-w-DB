from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.email import Email

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/email/create', methods=['POST'])
def create_email():
    if not Email.validate_email(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    data={
        "email_address" : request.form['email_address']
    }
    Email.create(data)
    return redirect('/success')

@app.route('/success')
def success():
    show_result = Email.get_all()
    print(show_result)
    return render_template("success.html", all_emails = show_result)

@app.route('/remove/<int:id>')
def remove_email(id):
    data={
        'id':id
    }
    Email.remove(data)
    return redirect('/success')