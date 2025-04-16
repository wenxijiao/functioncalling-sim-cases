import pygame


class Room:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.items = []

    def __str__(self):
        return f"Room: {self.name} ({self.description})"

    def add_item(self, item_name):
        """add item to room"""
        if item_name not in self.items:
            self.items.append(item_name)
            print(f"'{item_name}' has been added to {self.name}.")
        else:
            print(f"'{item_name}' has benn already in {self.name}.")

    def remove_item(self, item_name):
        """remove item from room"""
        if item_name in self.items:
            self.items.remove(item_name)
            print(f"{self.name} has been removed from '{item_name}'。")
        else:
            print(f"'{item_name}' is not in {self.name}.")

    def list_items(self):
        """list items in room"""
        if not self.items:
            print(f"{self.name} is empty.")
        else:
            print(f"{self.name} has: {', '.join(self.items)}")


class House:
    def __init__(self, rooms=[], name="my house"):
        """initialize house with a name"""
        self.name = name
        self.light = True
        self.rooms = {room.name: room for room in rooms}

    def add_room(self, room):
        """add room to house"""
        if isinstance(room, Room) and room.name not in self.rooms:
            self.rooms[room.name] = room
            print(f"Room '{room.name}' has been added to {self.name}.")
        elif room.name in self.rooms:
             print(f"Room '{room.name}' has been already in {self.name}.")
        else:
             print("room has to be a Room object.")

    def get_room(self, room_name):
        """get room by name"""
        return self.rooms.get(room_name, None)

    def list_rooms(self):
        """list all rooms in house"""
        if not self.rooms:
            print(f"{self.name} is still empty.")
        else:
            print(f"{self.name} includes: {', '.join(self.rooms.keys())}")
    
    def switch_light(self):
        """switch light on/off"""
        self.light = not self.light


class HouseEnvironment:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("House Environment")
        self.clock = pygame.time.Clock()
        self.running = True
        self.house = House([Room("living room"), Room("bedroom"), Room("kitchen")])

    def __str__(self):
        return str(self.house)

    def get_room(self, room_name):
        """get room by name"""
        return self.house.get_room(room_name)
    
    def draw(self):
        """draw house environment"""
        font = pygame.font.SysFont(None, 24)

        for i, item in enumerate(self.house.rooms.values()):
            pygame.draw.rect(self.screen, (200, 200, 250), pygame.Rect(50 + i * 200, 50, 190, 400))
            name_text = font.render(item.name, True, (0, 0, 0))
            self.screen.blit(name_text, (55 + i * 200, 55))
            for j, item in enumerate(item.items):
                item_text = font.render(f"- {item}", True, (0, 0, 0))
                self.screen.blit(item_text, (60 + i * 200, 80 + j * 20))

    def play(self):
        """start the game"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    env.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        env.running = False
                    if event.key == pygame.K_SPACE:
                        self.switch_light()
                    if event.key == pygame.K_l:
                        self.house.list_rooms()
                    if event.key == pygame.K_a:
                        room_name = input("Enter room name: ")
                        item_name = input("Enter item name: ")
                        self.add_item(room_name, item_name)
                    if event.key == pygame.K_r:
                        room_name = input("Enter room name: ")
                        item_name = input("Enter item name: ")
                        self.remove_item(room_name, item_name)
            
            if self.house.light:
                env.screen.fill((255, 255, 255))
            else:
                env.screen.fill((0, 0, 0))
            env.draw()
            pygame.display.flip()
            env.clock.tick(60)
        pygame.quit()

    def add_room(self, room):
        """add room to house"""
        self.house.add_room(room)

    def remove_room(self, room_name):
        """remove room from house"""
        if room_name in self.house.rooms:
            del self.house.rooms[room_name]
        else:
            print(f"'{room_name}' is not in {self.house.name}.")
    
    def add_item(self, room_name, item_name):
        """add item to room"""
        room = self.get_room(room_name)
        if room:
            room.add_item(item_name)
        else:
            print(f"'{room_name}' is not in {self.house.name}.")

    def remove_item(self, room_name, item_name):
        """remove item from room"""
        room = self.get_room(room_name)
        if room:
            room.remove_item(item_name)
        else:
            print(f"'{room_name}' is not in {self.house.name}.")

    def switch_light(self):
        """switch light on/off"""
        self.house.switch_light()


if __name__ == "__main__":
    env = HouseEnvironment()
    env.play()
