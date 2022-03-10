from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.card import Card
from flask_app import app



@app.route('/create/card')
def render_create_card():
    return render_template('create_card.html')


@app.route('/create/card', methods=['POST'])
def create_new_card():
    if 'user_id' not in session:
        flash('This page only available if logged in')

    if Card.validate(request.form):
        data = {
            'question': request.form['question'],
            'answer': request.form['answer'],
            'user_id': session['user_id']

        }

        Card.create_new_card(data)
        return redirect('/dashboard')
    return redirect('/create/card')



@app.route('/dashboard')
def get_all_cards():
    if 'user_id' not in session:
        flash('This page only available if logged in')
        return redirect('/')
    else:
        cards = Card.get_all_cards()
        return render_template('/dashboard.html', cards=cards)



@app.route('/show/<int:id>')
def show_card(id):
    data = {
        'id': id
    }
    one_card = Card.get_one(data)
    return render_template('view.html', one_card=one_card)



# # view edit page
# @app.route('/edit/<int:id>/recipe')
# def view_edit(id):
#     # creating data dict to pass in key id that my query is looking for
#     data = {
#         'id': id
#     }
#     # calling my Recipe class using the get one method I made
#     # and putting that recipe into a variable to pass into my html
#     recipe = Recipe.get_one(data)
#     return render_template('edit.html', recipe=recipe)



# # edit
# @app.route('/edit/<int:id>', methods=["POST"])
# def edit_single_recipe(id):
#     if 'user_id' not in session:
#         flash('This page only available if logged in')

#     #check if Class.request.form information is valid
#     if Recipe.validate(request.form):
#     # create data dictionary from from to edit recipe
#         data = {
#             'name': request.form['name'],
#             'description': request.form['description'],
#             'instructions': request.form['instructions'],
#             'under_30': request.form['under_30'],
#             'date': request.form['date'],
#             'id': id
#         }
#         #call edit single method I just made on Recipe class
#         Recipe.edit_single_recipe(data)
#         print(Recipe)

#         return redirect('/dashboard')
#     # redirect to edit page if not in session (watch the indentaion!!) 
#     return redirect(f'/edit/{id}/recipe')


# @app.route('/delete/<int:id>')
# def delete(id):
#     data = {
#         'id': id
#     }
#     Card.delete_item(data)
#     return redirect('/dashboard')