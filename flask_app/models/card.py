from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash



class Card:

    def __init__(self, data):
        self.id = data['id']
        self.question = data['question']
        self.answer = data['answer']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None


    @classmethod
    def create_new_card(cls, data):
        query = "INSERT INTO cards (question, answer, user_id) VALUES (%(question)s, %(answer)s, %(user_id)s);"
        result = connectToMySQL('flashii_schema').query_db(query, data)
        return result
        print(result)

    @classmethod
    def get_all_cards(cls):

        query = "SELECT * FROM users JOIN cards ON user_id WHERE cards.user_id = users.id;"
        results = connectToMySQL('flashii_schema').query_db(query)
        # create list for db table dictionaries
        cards = []
        # for row in query results
        for row in results:
            new_card = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            card_user = User(user_data)
            new_card.user = card_user
            cards.append(new_card)
        return cards


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM cards WHERE id = %(id)s;"
        result = connectToMySQL('flashii_schema').query_db(query, data)
        one_card = cls(result[0])
        return one_card





    # @classmethod
    # # edit does not need to be returned
    #     # selecting update by id
    # def edit_single_recipe(cls, data):
    #     query = "UPDATE recipes SET name=%(name)s, description= %(description)s, instructions=%(instructions)s, date = %(date)s,under_30= %(under_30)s WHERE id = %(id)s;"
    #     connectToMySQL('recipes_schema').query_db(query, data)


    @classmethod
    #from id
    def delete_card(cls, data):
        query = "DELETE FROM cards WHERE id = %(id)s;"
        result = connectToMySQL('flashii_schema').query_db(query, data)


    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['question']) < 1:
            is_valid = False
            flash("This field cannot be empty, please add text or img for your question")

        if len(data['answer']) < 1:
            is_valid = False
            flash("This field cannot be empty, please add text or img for your answer")

        return is_valid