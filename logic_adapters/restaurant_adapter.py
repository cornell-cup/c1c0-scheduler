from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from r2_chatterbot.util import keywords
from r2_chatterbot.util import make_response
from r2_chatterbot.util.api import restaurant

class RestaurantAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.data = None

    def can_process(self, statement):
        self.data = keywords.get_topic(statement.text,
                parse_location=False)

        if "name" in self.data.keys():
            return self.data["name"] == "restaurant"
        
        return False

    def get_default_response(self, input_statement):
        statement = Statement(text="no answer")
        
        return statement

    def process(self, statement, additional_response_selection, selection_parameters=None):
        keywords.modify_topic_data(self.data, parse_location=True)
        api_data = restaurant.lookup_restaurant_city(self.data["info"]["location"]["name"])
        response = make_response.make_response_api(self.data, api_data)
        statement = Statement(text=response, confidence=1)
        
        return statement

