import pyspigot as ps
from org.bukkit import Bukkit
from org.bukkit import Material
from org.bukkit.entity import Player
from org.bukkit import Location
from org.bukkit.event.player import PlayerInteractEvent
from org.bukkit.event.block import Action

class Builder:
    def __init__(self, world=None):
        self.world = world if world is not None else Bukkit.getWorld("world")
        self.start = None
        self.end = None
        self.items = []
        self.__build_task = None
    

    def reset(self):
        self.start = None
        self.end = None
    

    def clear_items(self):
        self.items = []


    def copy(self):
        if self.start is not None and self.end is not None:
            item = []
            sy, ey = min(self.start[1], self.end[1]), max(self.start[1], self.end[1])
            sx, ex = min(self.start[0], self.end[0]), max(self.start[0], self.end[0])
            sz, ez = min(self.start[2], self.end[2]), max(self.start[2], self.end[2])
            for iy, y in enumerate(range(sy, ey + 1)):
                for ix, x in enumerate(range(sx, ex + 1)):
                    for iz, z in enumerate(range(sz, ez + 1)):
                        block = self.world.getBlockAt(x, y, z).getType()
                        item.append([ix, iy, iz, block])
            self.items.append(item)
            self.reset()
    

    def print_items(self, sender):
        for build_id, item in enumerate(self.items):
            message = "Item id " + str(build_id) + " = " + str(len(item)) + " blocks"
            sender.sendMessage(message)
    

    def build(self, build_id, position):
        position = Location(self.world, *position)
        item = self.items[build_id]
        item = sorted(item, key=lambda x: x[1])
        for block in item:
            self.world.getBlockAt(int(position.getX()) + block[0], int(position.getY()) + block[1], int(position.getZ()) + block[2]).setType(block[3])                


builder = Builder()


def bcopy(sender, label, args):
    if isinstance(sender, Player):
        if args:
            builder.start = [int(x) for x in args[:3]]
            builder.end = [int(x) for x in args[3:6]]
        builder.copy()
    return True


def onclick(event):
    if event.getMaterial() == Material.WOODEN_SWORD:
        block = event.getClickedBlock()
        player = event.getPlayer()
        world = player.getWorld()
        x, y, z = block.getX(), block.getY(), block.getZ()
        if event.getAction() == Action.LEFT_CLICK_BLOCK:
            builder.start = [x, y, z]
            msg = "First position set to " + str([x, y, z])
            player.sendMessage(msg)

        if event.getAction() == Action.RIGHT_CLICK_BLOCK:
            builder.end = [x, y, z]
            msg = "Second position set to " + str([x, y, z])
            player.sendMessage(msg)



def build(sender, label, args):
    if isinstance(sender, Player):
        build_id = int(args[0])
        position = [int(x) for x in args[1:4]]
        builder.build(build_id, position)
    return True


def print_items(sender, label, args):
    if isinstance(sender, Player):
        builder.print_items(sender)
    return True


ps.command.registerCommand(bcopy, 'copy')
ps.command.registerCommand(print_items, 'get_builds')
ps.command.registerCommand(build, 'build')

ps.listener.registerListener(onclick, PlayerInteractEvent)
