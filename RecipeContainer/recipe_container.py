import random

class MetaBase:
    def __init__(self):
        self.is_full = False  # メタデータとしてアイテムが全て揃ったかどうかを管理


class Base(MetaBase):
    def __init__(self):
        super().__init__()
        self.containers = []    # 子クラスのデータリスト
    
    def add_item(self, item_id, quantity):
        if not self.is_full:
            for container in self._get_containers_in_order():  # 順序を決定するメソッド
                quantity = container.add_item(item_id, quantity)
            if quantity:  # まだ収納しきれていないアイテムがある場合
                self.is_full = True
        return quantity  # 収納しきれなかった残量を返す

    def add_container(self, container): #順序が関係ないコンテナにのみ使用する
        self.containers.append(container)
        self._check_is_full()

    def add_container_by_index(self, index, container):
        self.containers[index] = container
        self._check_is_full()

    def remove_container(self, container):  #順序が関係ないコンテナにのみ使用する
        if container in self.containers:
            self.containers.remove(container)
        self._check_is_full()

    def remove_container_by_index(self, index): #順序に意味があるコンテナに使用する
        self.containers[index] = None
        self._check_is_full()


    def _get_containers_in_order(self):
        return []
    
    def _check_is_full(self):
        if all(child.is_full for child in self.containers):
            self.is_full = True
        else:
            self.is_full = False
    
    def get_container(self, index):
        return self.containers[index]

    def search_container(self, arg1=0, arg2=0, arg3=0, arg4=0, arg5=0):
        if arg2:
            self.containers[arg1].search_container(arg2, arg3, arg4, arg5)
        else:
            return self.containers[arg1]

class IndexOrder(Base):
    def _get_containers_in_order(self):
        return self.containers

class RandomOrder(Base):
    def _get_containers_in_order(self):
        containers = self.containers
        random.shuffle(containers)  # ランダムに順序をシャッフル
        return containers
    
class FreeRecipe(MetaBase):
    def __init__(self, num_items):
        super().__init__()
        self.supplied_items = [0.0] * num_items

    def add_item(self, item_id, quantity):
        if item_id not in self.required_items:
            self.supplied_items[item_id] = quantity
        else:
            self.supplied_items[item_id] += quantity

    def absorb_recipe(self, recipe):
        for item_id, quantity in recipe.supplied_items.items():
            self.add_item(item_id, quantity)

class RestrictedRecipe(FreeRecipe):
    def __init__(self, num_items):
        super().__init__(num_items)
        self.required_items = [0.0] * num_items

    def add_require_item(self, item_id, quantity):
        if item_id not in self.required_items:
            self.required_items[item_id] = quantity
            self.supplied_items[item_id] = 0
            self.is_full = False

    def add_item(self, item_id, quantity):
        """
        調達したアイテムにアイテムIDのアイテムを指定された量だけ追加します。
        必要アイテム数を超える場合、超過分を返します。
        
        :param item_id: アイテムID
        :param quantity: 追加するアイテムの量
        :return: 必要アイテム数を超えた分の量（超過分がない場合は0）
        """
        if self.is_full:
            return quantity
        else:
            # item_id が required_items に存在しない場合、そのまま quantity を返す
            if item_id not in self.required_items:
                return quantity

            max_quantity = self.required_items[item_id]
            current_quantity = self.supplied_items[item_id]
            new_quantity = current_quantity + quantity

            if new_quantity > max_quantity:
                self.supplied_items[item_id] = max_quantity
                self._check_if_full()
                return new_quantity - max_quantity
            elif new_quantity == max_quantity:
                self._check_if_full()
                return 0
            else:
                self.supplied_items[item_id] = new_quantity
                return 0
            
    def _check_if_full(self):
        """
        全アイテムが必要数に達したかどうかを確認します。
        """
        self.is_full = all(
            supplied >= required for supplied, required in zip(self.supplied_items, self.required_items)
        )



class ManufacturingRecipe(RestrictedRecipe):
    def __init__(self, output_item_id = 0, output_quantity = 0):
        """
        :param output_item_id: 加工後アイテムID
        :param output_quantity: 加工後アイテム量
        """
        super().__init__()
        self.output_item_id = output_item_id
        self.output_quantity = output_quantity

class Category(IndexOrder):
    pass

class Completeness(RandomOrder):
    pass

class Priority(RandomOrder):
    pass

class Data(IndexOrder):
    pass
