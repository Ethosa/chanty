from enum import Enum

class Item(str, Enum):
    # Main blocks
    STONE = "minecraft:stone"
    COBBLESTONE = "minecraft:cobblestone"
    DIRT = "minecraft:dirt"
    GRASS_BLOCK = "minecraft:grass_block"
    SAND = "minecraft:sand"
    GRAVEL = "minecraft:gravel"
    CLAY = "minecraft:clay"
    BRICKS = "minecraft:bricks"
    GLASS = "minecraft:glass"
    OBSIDIAN = "minecraft:obsidian"
    DIAMOND_BLOCK = "minecraft:diamond_block"

    # Wood
    OAK_LOG = "minecraft:oak_log"
    BIRCH_LOG = "minecraft:birch_log"
    SPRUCE_LOG = "minecraft:spruce_log"
    OAK_PLANKS = "minecraft:oak_planks"
    STICK = "minecraft:stick"
    CRAFTING_TABLE = "minecraft:crafting_table"
    CHEST = "minecraft:chest"

    # Ores
    IRON_ORE = "minecraft:iron_ore"
    GOLD_ORE = "minecraft:gold_ore"
    COAL = "minecraft:coal"
    IRON_INGOT = "minecraft:iron_ingot"
    GOLD_INGOT = "minecraft:gold_ingot"
    COPPER_INGOT = "minecraft:copper_ingot"
    NETHERITE_INGOT = "minecraft:netherite_ingot"

    # Tools
    WOODEN_PICKAXE = "minecraft:wooden_pickaxe"
    STONE_PICKAXE = "minecraft:stone_pickaxe"
    IRON_PICKAXE = "minecraft:iron_pickaxe"
    DIAMOND_PICKAXE = "minecraft:diamond_pickaxe"
    WOODEN_SWORD = "minecraft:wooden_sword"
    IRON_SWORD = "minecraft:iron_sword"
    DIAMOND_SWORD = "minecraft:diamond_sword"

    # Food
    APPLE = "minecraft:apple"
    BREAD = "minecraft:bread"
    BEEF = "minecraft:beef"
    COOKED_BEEF = "minecraft:cooked_beef"
    PORKCHOP = "minecraft:porkchop"
    COOKED_PORKCHOP = "minecraft:cooked_porkchop"
    CHICKEN = "minecraft:chicken"
    COOKED_CHICKEN = "minecraft:cooked_chicken"
    POTATO = "minecraft:potato"
    BAKED_POTATO = "minecraft:baked_potato"

    # Other
    TORCH = "minecraft:torch"
    FURNACE = "minecraft:furnace"
    CAMPFIRE = "minecraft:campfire"
    BUCKET = "minecraft:bucket"
    WATER_BUCKET = "minecraft:water_bucket"
    LAVA_BUCKET = "minecraft:lava_bucket"

    def __str__(self) -> str:
        return self.value
