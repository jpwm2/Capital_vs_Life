

from RecipeContainer import recipe_container

META_INDEX = 0
DATA_INDEX = 1
PRIORITY_HIGH = 1
PRIORITY_LOW = 2
PRIORITY_FREE = 3
COMPLETENESS_TRUE = 1
COMPLETENESS_FALSE = 2
CLASSIFICATION_FUEL = 1
CLASSIFICATION_MANUFACT = 2
CLASSIFICATION_INVESTMENT = 3
CLASSIFICATION_CONSUMING_UTILITY = 4
CLASSIFICATION_UTILITY_INVESTMENT = 5



class Human:
    def __init__(self, utility):
        self.scheduled_recipe = recipe_container.FreeRecipe()
        self.hold_recipe = recipe_container.FreeRecipe()
        self.dividend_recipe = recipe_container.FreeRecipe()
        self.utility = utility

    def run_lifecycle(self, recipe_container, market_info):
        def respond_fuel():                 #緊迫燃料レシピに応答する
            complete_container = recipe_container.search_container(PRIORITY_HIGH, COMPLETENESS_FALSE)
            fuel_container = complete_container.get_container(CLASSIFICATION_FUEL)

        def respond_manufacturing():        #緊急製造レシピに応答する
            manufact_container = recipe_container.search_container(PRIORITY_HIGH, COMPLETENESS_TRUE, CLASSIFICATION_MANUFACT)
            for recipe in manufact_container.containers:
                is_full = recipe.is_full
                if is_full:
                    available_item_id = recipe.output_item_id
                    available_item_quantity = recipe.output_item_quantity
                    self.scheduled_recipe.add_item(available_item_id, available_item_quantity)
                else:
                    self.hold_recipe.absorb_recipe(recipe)

        def respond_investment():           #緊迫運用レシピに応答する
            investment_container = recipe_container.search_container(PRIORITY_HIGH, COMPLETENESS_FALSE,CLASSIFICATION_INVESTMENT)
            investment_recipe = investment_container.containers[0]
            for item_id, quantity in investment_recipe.items():
                self.hold_recipe.add_item(item_id, quantity)

        def respond_consuming_utility():    #緊迫効用消化レシピに応答する
            consuming_container = recipe_container.search_container(PRIORITY_HIGH, COMPLETENESS_FALSE, CLASSIFICATION_CONSUMING_UTILITY)
            consuming_recipe = consuming_container.containers[0]
            for item_id, quantity in consuming_recipe.supplied_items.items():
                self.utility.consume(item_id, quantity)
            self.utility.update()

        def respond_utility_investment():   #緊迫効用運用レシピに応答する
            utility_investment_container = recipe_container.search_container(PRIORITY_HIGH, COMPLETENESS_FALSE, CLASSIFICATION_CONSUMING_UTILITY)
            for recipe in utility_investment_container.containers:
                is_full = recipe.is_full
                if is_full:
                    baby = recipe.output_item_id
                    quantity = recipe.output_item_quantity
                    self.dividend_recipe.add_item(baby, quantity)
                else:
                    self.hold_recipe.absorb_recipe(recipe)

        def migrate_recipes():              #レシピ移行する
            priority_high_container = recipe_container.get_container(PRIORITY_HIGH)
            recipe_container.remove_container(priority_high_container)
            priority_low_container = recipe_container.get_container(PRIORITY_LOW)
            recipe_container.add_container_by_index(PRIORITY_LOW, priority_low_container)
            recipe_container.remvoe_container_by_index(PRIORITY_LOW)
        
        def predict_dividends():            #配当を予測する
            pass

        def ensure_respond_fuel1():         #緊迫燃料レシピを調達確実にする1
            pass
        def decide_fuel():                  #燃料アイテムを算出する
            pass
        def decide_consuming_utility():     #効用消化の意思決定をする（緊急事態以外）
            pass
        def decide_utility_investment():    #効用運用の意思決定をする（緊急事態以外）
            pass
        def decide_manufacturing():         #製造の意思決定をする（緊急事態以外）
            pass
        def decide_investment():            #運用の意思決定をする
            pass
        def ensure_respond_fuel2():         #緊迫燃料レシピを調達確実にする2
            pass

        respond_fuel()
        respond_manufacturing()
        respond_investment()
        respond_consuming_utility()
        respond_utility_investment()
        migrate_recipes()
        predict_dividends()
        ensure_respond_fuel1()
        decide_fuel()
        out_of_order_decisions = [decide_consuming_utility,decide_utility_investment,decide_manufacturing,decide_investment]
        for decision in out_of_order_decisions:
            decision() 
        ensure_respond_fuel2()