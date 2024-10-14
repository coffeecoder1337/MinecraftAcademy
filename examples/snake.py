import pyspigot as ps
from org.bukkit import Bukkit
from org.bukkit import Material
from org.bukkit.entity import Player

class Snake:
    def __init__(self, x=None, y=None, z=None, where_looking=None, world=None, length=1, material=Material.COBBLESTONE):
        self.x = x
        self.y = y
        self.z = z
        self.head = [self.x, self.y, self.z]
        self.body = []
        self.world = world if world else Bukkit.getWorld("world")
        self.length = length
        self.material = material
        self.direction = 'F'
        self.__move_task = None

        if where_looking:
            self.x, self.y, self.z = where_looking.getX(), where_looking.getY() + 1, where_looking.getZ()

        for x in range(self.length + 1):
            self.body.append([self.x - x, self.y, self.z])


    def place(self, clear=False):
        mat = self.material
        if clear:
            mat = Material.AIR

        for block in self.body:
            self.world.getBlockAt(*block).setType(mat)


    def update(self):
        self.head = [self.x, self.y, self.z]
        self.body.insert(0, list(self.head))
        self.body.pop()

    
    def move(self, step=None):
        if self.__move_task is None:
            self.__move_task = ps.scheduler.scheduleRepeatingTask(Snake.__update_position, 20, 5, self, step)
    

    def stop(self):
        if self.__move_task is not None:
            self.__move_task = ps.scheduler.stopTask(self.__move_task)
            self.__move_task = None

    
    @staticmethod
    def __update_position(snake, step):
        snake.place(clear=True)
        if snake.direction == 'F':
            snake.x += 1
        if snake.direction == 'B':
            snake.x -= 1
        if snake.direction == 'R':
            snake.z += 1
        if snake.direction == 'L':
            snake.z -= 1

        snake.update()
        snake.place()
        if step is not None:
            step -= 1
            if step < 0:
                snake.stop()


snake = None
def make_snake(sender, label, args):
    if isinstance(sender, Player):
        global snake
        length = 7
        if args:
            spawn_location = [int(x) for x in args[:3]]
            x, y, z = spawn_location
            snake = Snake(x, y, z, length=length)
        else:
            snake = Snake(where_looking=sender.getTargetBlock(None, 5), length=length)
        
        if snake:
            snake.place()
    return True


def move(sender, label, args):
    if isinstance(sender, Player):
        global snake
        if snake:
            d = args[0]
            if d in "FLRB":
                snake.direction = d
            if d == 'STOP':
                snake.stop()
            if d == 'MOVE':
                snake.move()
    return True


ps.command.registerCommand(make_snake, 'snake')
ps.command.registerCommand(move, 'move')