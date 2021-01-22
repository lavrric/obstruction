class Repository:
    def __init__(self):
        self.__database = {}

    # Create
    def create_item(self, item):
        if item.id in self.__database:
            raise AttributeError("Item id already exists!")
        self.__database[item.id] = item

    # Read
    def item_by_id(self, item_id):
        if item_id not in self.__database:
            raise AttributeError("Not valid id (repo)!")
        return self.__database[item_id]

    def all_items(self):
        return list(self.__database.values())

    def __len__(self):
        return len(self.__database)

    # Update
    def update_item(self, item):
        if item.id not in self.__database:
            raise AttributeError("No item with such id!")
        self.__database[item.id] = item

    # Delete
    def delete_item_by_id(self, item_id):
        del self.__database[item_id]
