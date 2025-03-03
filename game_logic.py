import random
import time

class Character:
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.level = 1
        self.exp = 0
        self.gold = 50
        self.inventory = {"Health Potion": 2, "Mana Potion": 2}
        self.weapons = {"Basic Sword": 8}
        self.current_weapon = "Basic Sword"
        self.abilities = {}
        self.status_effects = []
        self.armor = {"Basic Leather": 5}
        self.current_armor = "Basic Leather"
        self.tech_points = 0
        self.gadgets = {}
        
        # Initialize base abilities based on class
        self.update_abilities()
        
    def get_scaling_factor(self):
        """Calculate scaling factor based on level"""
        return 1 + (self.level - 1) * 0.15
        
    def update_abilities(self):
        """Update abilities based on level and class"""
        scaling = self.get_scaling_factor()
        
        if self.class_type.lower() in ["warrior", "1"]:
            self.health = 140 + (self.level - 1) * 25    # Increased health scaling
            self.max_health = self.health
            self.mana = 40 + (self.level - 1) * 8        # Reduced mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Rage": {"damage": int(25 * scaling), "mana_cost": 15, "description": "Strong attack with bonus damage"},
                "Shield Block": {"defense": int(15 * scaling), "duration": 2, "mana_cost": 10, "description": "Temporary defense boost"}
            }
            if self.level >= 3:
                base_abilities["Whirlwind"] = {
                    "damage": int(18 * scaling),
                    "area_damage": int(15 * scaling),
                    "hits": 3,
                    "mana_cost": 25,
                    "description": "Spin attack hitting multiple enemies"
                }
            if self.level >= 5:
                base_abilities["Berserk"] = {
                    "damage": int(40 * scaling),
                    "mana_cost": 30,
                    "description": "Powerful rage attack"
                }
                
        elif self.class_type.lower() in ["mage", "2"]:
            self.health = 80 + (self.level - 1) * 12     # Reduced health scaling
            self.max_health = self.health
            self.mana = 100 + (self.level - 1) * 20      # Increased mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Fireball": {
                    "damage": int(20 * scaling), 
                    "duration": 3, 
                    "mana_cost": 15, 
                    "description": "Fire damage over time",
                    "effect": "burn"
                },
                "Frost Bolt": {
                    "damage": int(25 * scaling), 
                    "mana_cost": 20, 
                    "description": "Direct magic damage",
                    "effect": "freeze"
                }
            }
            if self.level >= 3:
                base_abilities["Lightning Strike"] = {
                    "damage": int(35 * scaling),
                    "mana_cost": 25,
                    "description": "Powerful lightning attack",
                    "effect": "stun",
                    "duration": 1
                }
            if self.level >= 5:
                base_abilities["Meteor"] = {
                    "damage": int(35 * scaling),
                    "area_damage": int(25 * scaling),
                    "mana_cost": 40,
                    "description": "Massive area damage spell",
                    "effect": "burn",
                    "duration": 2
                }

        elif self.class_type.lower() in ["paladin", "3"]:
            self.health = 120 + (self.level - 1) * 20    # Balanced health scaling
            self.max_health = self.health
            self.mana = 60 + (self.level - 1) * 12       # Balanced mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Holy Strike": {"damage": int(20 * scaling), "heal": int(10 * scaling), "mana_cost": 15, "description": "Holy damage with healing"},
                "Divine Shield": {"defense": int(20 * scaling), "duration": 3, "mana_cost": 20, "description": "Strong defensive barrier"}
            }
            if self.level >= 3:
                base_abilities["Consecration"] = {
                    "damage": int(15 * scaling),
                    "area_damage": int(12 * scaling),
                    "heal": int(15 * scaling),
                    "mana_cost": 25,
                    "description": "Holy area damage and healing"
                }
            if self.level >= 5:
                base_abilities["Divine Storm"] = {
                    "damage": int(35 * scaling),
                    "heal": int(20 * scaling),
                    "mana_cost": 35,
                    "description": "Powerful holy attack with healing"
                }

        elif self.class_type.lower() in ["necromancer", "4"]:
            self.health = 90 + (self.level - 1) * 15     # Low health scaling
            self.max_health = self.health
            self.mana = 90 + (self.level - 1) * 18       # High mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Death Bolt": {"damage": int(22 * scaling), "mana_cost": 15, "description": "Dark magic damage"},
                "Life Drain": {"damage": int(18 * scaling), "heal": int(15 * scaling), "mana_cost": 20, "description": "Drain life from enemy"}
            }
            if self.level >= 3:
                base_abilities["Curse"] = {
                    "damage": int(12 * scaling),
                    "duration": 4,
                    "mana_cost": 25,
                    "description": "Strong damage over time"
                }
            if self.level >= 5:
                base_abilities["Death Nova"] = {
                    "damage": int(30 * scaling),
                    "area_damage": int(20 * scaling),
                    "mana_cost": 35,
                    "description": "Explosion of dark energy"
                }

        elif self.class_type.lower() in ["assassin", "5"]:
            self.health = 95 + (self.level - 1) * 14     # Medium-low health scaling
            self.max_health = self.health
            self.mana = 50 + (self.level - 1) * 10       # Medium mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Backstab": {"damage": int(30 * scaling), "mana_cost": 15, "description": "High damage from stealth"},
                "Poison Strike": {"damage": int(15 * scaling), "duration": 3, "mana_cost": 20, "description": "Poisoned weapon attack"}
            }
            if self.level >= 3:
                base_abilities["Shadow Step"] = {
                    "damage": int(25 * scaling),
                    "mana_cost": 25,
                    "description": "Teleport behind enemy and strike"
                }
            if self.level >= 5:
                base_abilities["Death Mark"] = {
                    "damage": int(45 * scaling),
                    "duration": 2,
                    "mana_cost": 35,
                    "description": "Mark target for death"
                }

        elif self.class_type.lower() in ["druid", "6"]:
            self.health = 110 + (self.level - 1) * 18    # Medium-high health scaling
            self.max_health = self.health
            self.mana = 70 + (self.level - 1) * 15       # Medium-high mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Nature's Wrath": {"damage": int(20 * scaling), "mana_cost": 15, "description": "Nature damage"},
                "Regrowth": {"heal": int(25 * scaling), "duration": 3, "mana_cost": 20, "description": "Strong healing over time"}
            }
            if self.level >= 3:
                base_abilities["Entangling Roots"] = {
                    "damage": int(18 * scaling), 
                    "duration": 2, 
                    "mana_cost": 25,
                    "description": "Root and damage over time",
                    "effect": "root"
                }
            if self.level >= 5:
                base_abilities["Hurricane"] = {
                    "damage": int(25 * scaling), 
                    "area_damage": int(18 * scaling),
                    "hits": 3, 
                    "mana_cost": 35,
                    "description": "Multiple nature damage hits in area",
                    "effect": "wind"
                }

        elif self.class_type.lower() in ["monk", "7"]:
            self.health = 100 + (self.level - 1) * 16
            self.max_health = self.health
            self.mana = 60 + (self.level - 1) * 12
            self.max_mana = self.mana
            base_abilities = {
                "Chi Strike": {"damage": int(25 * scaling), "mana_cost": 15, "description": "Powerful martial arts attack"},
                "Meditation": {"heal": int(20 * scaling), "duration": 2, "mana_cost": 20, "description": "Restore health over time"}
            }
            if self.level >= 3:
                base_abilities["Flying Kick"] = {
                    "damage": int(30 * scaling),
                    "effect": "stun",
                    "duration": 1,
                    "mana_cost": 25,
                    "description": "High damage leap attack with stun"
                }
            if self.level >= 5:
                base_abilities["Spirit Burst"] = {
                    "damage": int(35 * scaling),
                    "heal": int(20 * scaling),
                    "mana_cost": 35,
                    "description": "Damage and healing combo"
                }

        elif self.class_type.lower() in ["ranger", "8"]:
            self.health = 95 + (self.level - 1) * 15
            self.max_health = self.health
            self.mana = 65 + (self.level - 1) * 13
            self.max_mana = self.mana
            base_abilities = {
            "Precise Shot": {"damage": int(28 * scaling), "mana_cost": 15, "description": "Accurate ranged attack"},
            "Animal Bond": {"heal": int(18 * scaling), "damage": int(15 * scaling), "mana_cost": 20, "description": "Call animal companion"}
            }
            if self.level >= 3:
                base_abilities["Multi Shot"] = {
                    "damage": int(15 * scaling), 
                    "hits": 3, 
                    "mana_cost": 25, 
                    "description": "Fire multiple arrows"
                }
            if self.level >= 5:
                base_abilities["Hunter's Mark"] = {
                    "damage": int(35 * scaling), 
                    "duration": 3, 
                    "mana_cost": 30,
                    "description": "Mark target for extra damage"
                }

        elif self.class_type.lower() in ["warlock", "9"]:
            self.health = 85 + (self.level - 1) * 14
            self.max_health = self.health
            self.mana = 95 + (self.level - 1) * 19
            self.max_mana = self.mana
            base_abilities = {
                "Shadow Bolt": {"damage": int(27 * scaling), "mana_cost": 15, "description": "Dark energy attack"},
                "Soul Drain": {"damage": int(20 * scaling), "heal": int(10 * scaling), "mana_cost": 20, "description": "Drain enemy life force"}
            }
            if self.level >= 3:
                base_abilities["Demon Form"] = {
                    "damage": int(25 * scaling), 
                    "duration": 3, 
                    "mana_cost": 30,
                    "description": "Transform for enhanced damage"
                }
            if self.level >= 5:
                base_abilities["Chaos Blast"] = {
                    "damage": int(45 * scaling), 
                    "mana_cost": 40,
                    "description": "Powerful chaotic explosion"
                }

        elif self.class_type.lower() in ["berserker", "10"]:
            self.health = 130 + (self.level - 1) * 22
            self.max_health = self.health
            self.mana = 35 + (self.level - 1) * 7
            self.max_mana = self.mana
            base_abilities = {
                "Frenzy": {"damage": int(35 * scaling), "mana_cost": 15, "description": "Powerful rage attack"},
                "Battle Cry": {"damage": int(20 * scaling), "duration": 2, "mana_cost": 20, "description": "Intimidating shout"}
            }
            if self.level >= 3:
                base_abilities["Blood Rage"] = {
                    "damage": int(30 * scaling), 
                    "heal": int(15 * scaling), 
                    "mana_cost": 25,
                    "description": "Damage boost with life drain"
                }
            if self.level >= 5:
                base_abilities["Rampage"] = {
                    "damage": int(25 * scaling), 
                    "hits": 4, 
                    "mana_cost": 35,
                    "description": "Multiple savage attacks"
                }

        elif self.class_type.lower() in ["alchemist", "11"]:
            self.health = 90 + (self.level - 1) * 15
            self.max_health = self.health
            self.mana = 80 + (self.level - 1) * 16
            self.max_mana = self.mana
            base_abilities = {
                "Acid Splash": {"damage": int(23 * scaling), "duration": 2, "mana_cost": 15, "description": "Corrosive damage over time"},
                "Healing Elixir": {"heal": int(30 * scaling), "mana_cost": 20, "description": "Powerful healing potion"}
            }
            if self.level >= 3:
                base_abilities["Explosive Flask"] = {
                    "damage": int(25 * scaling), 
                    "area_damage": int(20 * scaling),
                    "mana_cost": 25, 
                    "description": "Area damage chemical explosion"
                }
            if self.level >= 5:
                base_abilities["Transmutation"] = {
                    "heal": int(25 * scaling), 
                    "damage": int(25 * scaling), 
                    "mana_cost": 35,
                    "description": "Convert damage to healing"
                }

        elif self.class_type.lower() in ["shaman", "12"]:
            self.health = 105 + (self.level - 1) * 17
            self.max_health = self.health
            self.mana = 75 + (self.level - 1) * 15
            self.max_mana = self.mana
            base_abilities = {
                "Lightning Chain": {"damage": int(22 * scaling), "hits": 2, "mana_cost": 15, "description": "Chain lightning attack"},
                "Ancestral Spirit": {"heal": int(25 * scaling), "duration": 2, "mana_cost": 20, "description": "Healing over time"}
            }
            if self.level >= 3:
                base_abilities["Earthquake"] = {
                    "damage": int(30 * scaling), 
                    "mana_cost": 25,
                    "description": "Ground-shaking attack"
                }
            if self.level >= 5:
                base_abilities["Spirit Wolves"] = {
                    "damage": int(20 * scaling), 
                    "hits": 3, 
                    "mana_cost": 35,
                    "description": "Summon spirit wolves to attack"
                }

        self.abilities = base_abilities

# Add Gadget class
class Gadget:
    def __init__(self, name, rarity, effect, cost):
        self.name = name
        self.rarity = rarity  # common, rare, epic, legendary
        self.effect = effect
        self.cost = cost
        self.charges = self.get_charges()
        
    def get_charges(self):
        charges = {
            "common": 3,
            "rare": 2,
            "epic": 2,
            "legendary": 1
        }
        return charges.get(self.rarity, 1)

    def use(self, player, enemy):
        if self.charges > 0:
            self.charges -= 1
            return True
        return False

# Update Enemy class for better balance
class Enemy:
    def __init__(self, name, health, damage, exp_reward, gold_reward, level=1):
        self.name = name
        self.level = level
        # Scale stats based on level
        level_multiplier = 1 + (level - 1) * 0.2
        self.health = int(health * level_multiplier)
        self.max_health = self.health
        self.damage = int(damage * level_multiplier)
        self.exp_reward = int(exp_reward * level_multiplier)
        self.gold_reward = int(gold_reward * level_multiplier)
        self.status_effects = []
        self.abilities = {}
        self.is_boss = False
        
    def is_alive(self):
        """Check if enemy is still alive"""
        return self.health > 0
        
    def take_damage(self, amount):
        """Handle damage taken by enemy"""
        self.health = max(0, self.health - amount)
        return amount

def combat(player, enemy):
    print(f"\nA {enemy.name} appears!")
    
    while enemy.health > 0 and player.health > 0:
        # Process status effects at start of turn
        process_status_effects(player)
        process_status_effects(enemy)
        
        # Display battle status
        print(f"\n{'-'*40}")
        print(f"Your HP: {player.health}/{player.max_health}")
        print(f"Your MP: {player.mana}/{player.max_mana}")
        print(f"Enemy HP: {enemy.health}")
        
        # Show active effects
        if player.status_effects:
            print("\nYour status effects:")
            for effect in player.status_effects:
                print(f"- {effect['name']} ({effect['duration']} turns)")
        
        # Combat options
        print("\nWhat would you like to do?")
        print("1. Attack")
        print("2. Use Ability")
        print("3. Use Item")
        print("4. Use Gadget")
        print("5. Run")
        
        choice = input("> ")
        
        # Process turn
        if choice == "1":
            damage = process_attack(player, enemy)
            enemy.health -= damage
            print(f"You deal {damage} damage to the {enemy.name}!")
            
        elif choice == "2":
            show_abilities(player)
            ability = input("Choose ability (or 'back'): ")
            if ability in player.abilities and player.mana >= player.abilities[ability]["mana_cost"]:
                process_ability(player, enemy, ability)
            else:
                print("Not enough mana or invalid ability!")
                continue

        elif choice == "3":
            print("\nAvailable items:")
            if player.inventory.get("Health Potion", 0) > 0:
                print("1. Health Potion")
            if player.inventory.get("Mana Potion", 0) > 0:
                print("2. Mana Potion")
            
            item_choice = input("Choose item to use (or 'back'): ")
            
            if item_choice == "1" and player.inventory.get("Health Potion", 0) > 0:
                player.health = min(player.max_health, player.health + 30)
                player.inventory["Health Potion"] -= 1
                print("You drink a health potion and recover 30 HP!")
            elif item_choice == "2" and player.inventory.get("Mana Potion", 0) > 0:
                player.mana = min(player.max_mana, player.mana + 25)
                player.inventory["Mana Potion"] -= 1
                print("You drink a mana potion and recover 25 MP!")
            elif item_choice.lower() == "back":
                continue
            else:
                print("Invalid item or not enough potions!")
                continue
                
        elif choice == "4":
            if player.gadgets:
                print("\nAvailable Gadgets:")
                for name, gadget in player.gadgets.items():
                    if gadget.charges > 0:
                        print(f"{name} ({gadget.charges} charges)")
                
                gadget_choice = input("Choose gadget (or 'back'): ").title()
                if gadget_choice in player.gadgets:
                    gadget = player.gadgets[gadget_choice]
                    if gadget.use(player, enemy):
                        process_gadget_effect(player, enemy, gadget.effect)
                    else:
                        print("No charges remaining!")
                        continue
            else:
                print("No gadgets available!")
                continue

        elif choice == "5":
            if random.random() < 0.5:
                print("You successfully fled from combat!")
                return "fled"  # Changed return value to indicate fled status
            else:
                print("You failed to run away!")
        
        # In combat function, replace enemy attack section
        if enemy.health > 0:
            damage_taken = process_enemy_attack(player, enemy)
            player.health -= damage_taken
            print(f"The {enemy.name} attacks you for {damage_taken} damage! (Reduced by armor)")
            
    if player.health <= 0:
        print("You have been defeated...")
        return False
    
    print(f"You defeated the {enemy.name}!")
    player.exp += enemy.exp_reward
    player.gold += enemy.gold_reward
    print(f"You gained {enemy.exp_reward} EXP and {enemy.gold_reward} gold!")
    
    # Add post-battle healing based on level
    heal_amount = int(player.max_health * (0.15 + (player.level * 0.01)))  # 15% + 1% per level
    mana_restore = int(player.max_mana * (0.1 + (player.level * 0.01)))   # 10% + 1% per level
    player.health = min(player.max_health, player.health + heal_amount)
    player.mana = min(player.max_mana, player.mana + mana_restore)
    print(f"Victory healing: Recovered {heal_amount} HP and {mana_restore} MP!")
    
    # In combat victory section
    tech_points_reward = int(10 * (1 + (enemy.level * 0.5)))
    player.tech_points += tech_points_reward
    print(f"Gained {tech_points_reward} Tech Points!")
    
    # In combat function, modify level up section
    if player.exp >= calculate_exp_requirement(player.level):  # Scaling exp requirement
        old_level = player.level
        player.level += 1
        player.exp = 0
        rewards = calculate_level_rewards(player.level)
        player.max_health += rewards["health"]
        player.health = player.max_health
        player.max_mana += rewards["mana"]
        player.mana = player.max_mana
        print(f"\nLevel up! You are now level {player.level}!")
        print(f"Max HP increased by {rewards['health']}!")
        print(f"Max MP increased by {rewards['mana']}!")
        
        # Show new abilities notification
        level_3_abilities = {
            "Whirlwind", "Lightning Strike", "Consecration", "Curse", 
            "Shadow Step", "Entangling Roots", "Flying Kick", "Multi Shot",
            "Demon Form", "Blood Rage", "Explosive Flask", "Earthquake"
        }
        # Add level 5 abilities set before updating abilities
        level_5_abilities = {
            "Berserk", "Meteor", "Divine Storm", "Death Nova", 
            "Death Mark", "Hurricane", "Spirit Burst", "Hunter's Mark",
            "Chaos Blast", "Rampage", "Transmutation", "Spirit Wolves"
        }
        
        player.update_abilities()  # Update abilities for new level
        if player.level == 3:
            print("\nNew level 3 ability unlocked!")
            for ability_name, ability in player.abilities.items():
                if ability_name not in level_3_abilities:
                    print(f"- {ability_name}: {ability['description']}")
        elif player.level == 5:
            print("\nNew level 5 ability unlocked!")
            for ability_name, ability in player.abilities.items():
                if ability_name in level_5_abilities:
                    print(f"- {ability_name}: {ability['description']}")
    
    return True

# Add gadget effect processing
def process_gadget_effect(player, enemy, effect):
    if "damage" in effect:
        enemy.health -= effect["damage"]
        print(f"Gadget deals {effect['damage']} damage!")
        
    if "heal" in effect:
        heal = effect["heal"]
        player.health = min(player.max_health, player.health + heal)
        print(f"Gadget heals for {heal} HP!")
        
    if "flee" in effect:
        if random.random() < effect["chance"]:
            print("Gadget allows you to escape!")
            return "fled"
            
    if "defense" in effect:
        player.status_effects.append({
            "name": "Shield",
            "defense": effect["defense"],
            "duration": effect["duration"]
        })
        print(f"Shield activated for {effect['duration']} turns!")
        
    if "revive" in effect:
        if player.health <= 0:
            player.health = int(player.max_health * effect["health_percent"])
            print("Phoenix Protocol activates! You're revived!")

# Update experience and level scaling
def calculate_exp_requirement(level):
    """More balanced experience requirements"""
    return int(75 * (1 + (level * 0.4)))  # Reduced from 0.5 to 0.4

def calculate_level_rewards(level):
    """More balanced level-up rewards"""
    return {
        "health": 12 + (level * 2),  # Reduced from 15 + (level * 3)
        "mana": 6 + (level * 1.5),   # Reduced from 8 + (level * 2)
        "damage_bonus": int(level * 0.8),
        "defense_bonus": int(level * 0.7)
    }

# Update shop function's item handling
def shop(player):
    items = {
        # Basic items (always available)
        "Health Potion": {"cost": 20, "effect": "Restore 35 HP", "min_level": 1},
        "Mana Potion": {"cost": 25, "effect": "Restore 30 MP", "min_level": 1},
        
        # Tier 1 Equipment (level 1-2)
        "Iron Sword": {"cost": 60, "damage": 10, "min_level": 1},
        "Wooden Staff": {"cost": 55, "damage": 8, "mana_bonus": 12, "min_level": 1},
        "Leather Armor": {"cost": 70, "defense": 6, "min_level": 1},
        
        # Tier 2 Equipment (level 3-4)
        "Steel Sword": {"cost": 140, "damage": 16, "min_level": 3},
        "Magic Staff": {"cost": 160, "damage": 14, "mana_bonus": 20, "min_level": 3},
        "Chain Mail": {"cost": 170, "defense": 12, "min_level": 3},
        
        # Tier 3 Equipment (level 5+)
        "Flame Sword": {"cost": 280, "damage": 28, "min_level": 5},
        "Frost Staff": {"cost": 290, "damage": 25, "mana_bonus": 35, "min_level": 5},
        "Plate Armor": {"cost": 300, "defense": 20, "min_level": 5}
    }
    
    while True:
        print("\nWelcome to the shop!")
        print(f"Your gold: {player.gold}")
        print("\nAvailable items:")
        for item, details in items.items():
            desc = details.get('effect', 'Equipment')
            if 'damage' in details:
                desc = f"Damage: {details['damage']}"
            if 'defense' in details:
                desc = f"Defense: {details['defense']}"
            if 'mana_bonus' in details:
                desc += f", Mana Bonus: {details['mana_bonus']}"
            print(f"{item}: {details['cost']} gold - {desc}")
        print("\nEnter item name to buy (or 'exit' to leave):")
        
        choice = input("> ").title()
        if choice.lower() == "exit":
            break
        
        if choice in items:
            if player.gold >= items[choice]["cost"]:
                player.gold -= items[choice]["cost"]
                if "damage" in items[choice]:
                    player.weapons[choice] = items[choice]["damage"]
                elif "defense" in items[choice]:
                    player.armor[choice] = items[choice]["defense"]
                else:
                    player.inventory[choice] = player.inventory.get(choice, 0) + 1
                print(f"Bought {choice}!")
            else:
                print("Not enough gold!")
        else:
            print("Invalid item!")

# Add Gadget Shop function
def gadget_shop(player):
    gadgets = {
        # Common gadgets
        "Smoke Bomb": Gadget("Smoke Bomb", "common", 
            {"effect": "flee", "chance": 0.8}, 50),
        "Health Generator": Gadget("Health Generator", "common",
            {"heal": 50}, 50),
        
        # Rare gadgets
        "Lightning Rod": Gadget("Lightning Rod", "rare",
            {"damage": 80, "stun": 1}, 100),
        "Shield Generator": Gadget("Shield Generator", "rare",
            {"defense": 30, "duration": 3}, 100),
            
        # Epic gadgets
        "Time Distorter": Gadget("Time Distorter", "epic",
            {"extra_turns": 1}, 200),
        "Damage Amplifier": Gadget("Damage Amplifier", "epic",
            {"damage_boost": 1.5, "duration": 2}, 200),
            
        # Legendary gadgets
        "Ultimate Nullifier": Gadget("Ultimate Nullifier", "legendary",
            {"damage": 200}, 500),
        "Phoenix Protocol": Gadget("Phoenix Protocol", "legendary",
            {"revive": True, "health_percent": 0.5}, 500)
    }
    
    while True:
        print("\n=== Gadget Shop ===")
        print(f"Tech Points: {player.tech_points}")
        print("\nAvailable Gadgets:")
        
        for name, gadget in gadgets.items():
            if name not in player.gadgets:
                print(f"{name} ({gadget.rarity.title()}) - {gadget.cost} TP")
                print(f"  Effect: {gadget.effect}")
                print(f"  Charges: {gadget.get_charges()}")
        
        print("\nEnter gadget name to buy (or 'exit' to leave):")
        choice = input("> ").title()
        
        if choice.lower() == "exit":
            break
            
        if choice in gadgets and choice not in player.gadgets:
            if player.tech_points >= gadgets[choice].cost:
                player.tech_points -= gadgets[choice].cost
                player.gadgets[choice] = gadgets[choice]
                print(f"Bought {choice}!")
            else:
                print("Not enough Tech Points!")
        else:
            print("Invalid gadget or already owned!")

def show_abilities(player):
    """Display available abilities and their descriptions"""
    print("\nAvailable Abilities:")
    for ability, details in player.abilities.items():
        print(f"{ability}: {details['description']} (Mana cost: {details['mana_cost']})")

def process_attack(player, enemy):
    """More balanced attack damage calculation"""
    base_damage = player.weapons[player.current_weapon]
    level_bonus = int(player.level * 1.5)  # Reduced from level * 2
    variation = random.randint(-2, 2)      # Reduced variation range
    return max(1, base_damage + level_bonus + variation)

def process_enemy_attack(player, enemy):
    """More balanced enemy damage calculation"""
    base_damage = enemy.damage
    armor_value = player.armor[player.current_armor]
    defense_reduction = int(armor_value * (0.3 + (player.level * 0.015)))  # Reduced scaling
    final_damage = max(1, base_damage - defense_reduction)
    return final_damage

def process_ability(player, enemy, ability_name):
    """Process the use of a special ability"""
    ability = player.abilities[ability_name]
    player.mana -= ability["mana_cost"]
    total_damage = 0
    
    # Add area damage handling
    if "area_damage" in ability:
        base_damage = ability["area_damage"]
        num_targets = random.randint(2, 4)  # Hit 2-4 targets
        for i in range(num_targets):
            hit_damage = int(base_damage * (0.7 + random.random() * 0.6))  # 70-130% variance
            enemy.health -= hit_damage
            total_damage += hit_damage
            print(f"Area Hit {i+1}: {hit_damage} damage!")
        print(f"Total area damage: {total_damage}")
    
    # Existing ability processing code...
    if "effect" in ability:
        if ability["effect"] == "burn":
            # Apply burn effect
            enemy.status_effects.append({
                "name": "Burned",
                "damage": int(ability["damage"] * 0.3), # 30% of initial damage as burn
                "duration": ability["duration"]
            })
            print(f"{enemy.name} is burned for {ability['duration']} turns!")
            
        elif ability["effect"] == "freeze":
            # Apply freeze effect
            enemy.status_effects.append({
                "name": "Frozen",
                "damage": int(ability["damage"] * 0.2),  # 20% of initial damage as freeze
                "duration": 2,  # Fixed 2 turn duration
                "damage_reduction": 0.5  # Reduces enemy damage by 50%
            })
            print(f"{enemy.name} is frozen for 2 turns! Their damage is reduced!")
            
        elif ability["effect"] == "root":
            # Apply root effect
            enemy.status_effects.append({
                "name": "Rooted",
                "damage": int(ability["damage"] * 0.5),
                "duration": ability["duration"],
                "movement_blocked": True
            })
            print(f"{enemy.name} is rooted for {ability['duration']} turns!")
            
        elif ability["effect"] == "wind":
            # Process hurricane hits
            for i in range(ability["hits"]):
                hit_damage = int(ability["damage"] * (0.8 + random.random() * 0.4))  # 80-120% damage per hit
                enemy.health -= hit_damage
                total_damage += hit_damage
                print(f"Hurricane hit {i+1}: {hit_damage} damage!")
            print(f"Total hurricane damage: {total_damage}")
            
        elif ability["effect"] == "stun":
            # Apply stun effect
            enemy.status_effects.append({
                "name": "Stunned",
                "duration": ability["duration"],
                "skip_turn": True
            })
            print(f"{enemy.name} is stunned for {ability['duration']} turns!")
    
    if "damage" in ability:
        damage = ability["damage"]
        if "hits" in ability:  # For multi-hit abilities
            for hit in range(ability["hits"]):
                hit_damage = damage + random.randint(-2, 2)  # Add variation per hit
                enemy.health -= hit_damage
                total_damage += hit_damage
                print(f"Hit {hit + 1}: {hit_damage} damage!")
            print(f"Total damage: {total_damage}")
        else:
            damage = damage + random.randint(-5, 5)  # Add variation for single hit
            enemy.health -= damage
            print(f"You use {ability_name} and deal {damage} damage!")
    
    if "heal" in ability:
        heal = ability["heal"]
        original_health = player.health
        player.health = min(player.max_health, player.health + heal)
        actual_heal = player.health - original_health
        print(f"You heal for {actual_heal} HP!")
    
    if "defense" in ability:
        defense_boost = {
            "name": ability_name,
            "defense": ability["defense"],
            "duration": ability["duration"]
        }
        # Remove any existing defense boost
        player.status_effects = [effect for effect in player.status_effects 
                               if effect["name"] != ability_name]
        player.status_effects.append(defense_boost)
        print(f"Gained {ability['defense']} defense for {ability['duration']} turns!")
    
    if "duration" in ability and "damage" in ability:  # For damage over time effects
        effect_name = ability_name.lower()
        # Remove existing effect of same type
        enemy.status_effects = [effect for effect in enemy.status_effects 
                              if effect["name"] != effect_name]
        enemy.status_effects.append({
            "name": effect_name,
            "damage": int(ability["damage"] / 2),  # DoT deals half damage per tick
            "duration": ability["duration"]
        })
        print(f"Applied {effect_name} effect for {ability['duration']} turns!")

def process_status_effects(entity):
    """Process status effects at the start of turn"""
    is_stunned = False
    damage_multiplier = 1.0
    
    for effect in entity.status_effects[:]:  # Create a copy to modify during iteration
        if effect["name"] == "Poison":
            damage = effect["damage"]
            entity.health -= damage
            print(f"{entity.name} takes {damage} poison damage!")
        elif effect["name"] == "Burned":
            damage = effect["damage"]
            entity.health -= damage
            print(f"{entity.name} takes {damage} burn damage!")
        elif effect["name"] == "Frozen":
            damage = effect["damage"]
            entity.health -= damage
            damage_multiplier *= effect.get("damage_reduction", 1.0)
            print(f"{entity.name} takes {damage} frost damage and has reduced damage!")
        elif effect["name"] == "Regeneration":
            heal = effect["heal"]
            entity.health = min(entity.max_health, entity.health + heal)
            print(f"{entity.name} regenerates {heal} health!")
        elif effect["name"] == "Stunned":
            is_stunned = True
            print(f"{entity.name} is stunned and skips their turn!")
            
        effect["duration"] -= 1
        if effect["duration"] <= 0:
            entity.status_effects.remove(effect)
            print(f"{effect['name']} effect has worn off!")
            
    return is_stunned, damage_multiplier


# Update show_inventory_menu function
def show_inventory_menu(player):
    """Show inventory menu with weapon and armor switching options"""
    while True:
        print("\n=== Inventory Menu ===")
        print("1. View Items")
        print("2. Change Weapon")
        print("3. Change Armor")
        print("4. Back")
        
        choice = input("> ")
        
        if choice == "1":
            print("\nInventory:")
            for item, quantity in player.inventory.items():
                print(f"{item}: {quantity}")
            print("\nWeapons:")
            for weapon, damage in player.weapons.items():
                print(f"{weapon} (Damage: {damage})")
            print(f"Currently equipped weapon: {player.current_weapon}")
            print("\nArmor:")
            for armor, defense in player.armor.items():
                print(f"{armor} (Defense: {defense})")
            print(f"Currently equipped armor: {player.current_armor}")
            
        elif choice == "2":
            print("\nAvailable Weapons:")
            weapons = list(player.weapons.keys())
            for i, weapon in enumerate(weapons, 1):
                damage = player.weapons[weapon]
                print(f"{i}. {weapon} (Damage: {damage})")
                if weapon == player.current_weapon:
                    print("   *Currently Equipped*")
            
            try:
                weapon_choice = int(input("\nChoose weapon number (0 to cancel): "))
                if 0 < weapon_choice <= len(weapons):
                    new_weapon = weapons[weapon_choice - 1]
                    if new_weapon != player.current_weapon:
                        player.current_weapon = new_weapon
                        print(f"Equipped {new_weapon}!")
                    else:
                        print("That weapon is already equipped!")
                elif weapon_choice != 0:
                    print("Invalid weapon number!")
            except ValueError:
                print("Invalid input!")
                
        elif choice == "3":
            print("\nAvailable Armor:")
            armors = list(player.armor.keys())
            for i, armor in enumerate(armors, 1):
                defense = player.armor[armor]
                print(f"{i}. {armor} (Defense: {defense})")
                if armor == player.current_armor:
                    print("   *Currently Equipped*")
            
            try:
                armor_choice = int(input("\nChoose armor number (0 to cancel): "))
                if 0 < armor_choice <= len(armors):
                    new_armor = armors[armor_choice - 1]
                    if new_armor != player.current_armor:
                        player.current_armor = new_armor
                        print(f"Equipped {new_armor}!")
                    else:
                        print("That armor is already equipped!")
                elif armor_choice != 0:
                    print("Invalid armor number!")
            except ValueError:
                print("Invalid input!")
                
        elif choice == "4":
            break

def main():
    print("Welcome to the Text RPG!")
    print("\nChoose your class:")
    print("1. Warrior - High HP and defense, strong melee attacks")
    print("2. Mage - Powerful spells and high mana")
    print("3. Paladin - Balanced stats with healing abilities") 
    print("4. Necromancer - Dark magic and life drain")
    print("5. Assassin - High damage and critical strikes")
    print("6. Druid - Nature magic and versatile abilities")
    print("7. Monk - Martial arts and meditation")
    print("8. Ranger - Skilled archer and animal companion")
    print("9. Warlock - Demonic powers and curses")
    print("10. Berserker - Rage and powerful attacks")
    print("11. Alchemist - Potions and explosives")
    print("12. Shaman - Elemental and spiritual magic")
    
    name = input("\nEnter your character's name: ")
    while True:
        class_choice = input("Choose your class (1-12): ")
        if class_choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
            break
        print("Invalid choice!")
    
    player = Character(name, class_choice)
    print(f"\nWelcome, {player.name} the {player.class_type}!")
    
    while True:
        # Status display
        print(f"\n{'='*50}")
        print(f"{player.name} - Level {player.level}")
        print(f"HP: {player.health}/{player.max_health}")
        print(f"MP: {player.mana}/{player.max_mana}")
        print(f"EXP: {player.exp}/{calculate_exp_requirement(player.level)}")
        print(f"Gold: {player.gold}")
        print(f"Current Weapon: {player.current_weapon}")
        print(f"Current Armor: {player.current_armor}")
        print(f"{'='*50}")
        
        # Main menu
        print("\nWhat would you like to do?")
        print("1. Fight monsters")
        print("2. Visit shop")
        print("3. Check inventory")
        print("4. Rest (Heal 50% HP/MP for 20 gold)")
        print("5. Show abilities")
        print("6. Visit gadget shop")
        print("7. Quit")
        
        choice = input("> ")
        
        if choice == "1":
            # Enemy selection based on player level
            enemies = []
            spawn_table = [
                (Enemy("Rat", 12, 2, 8, 5, 1), 40, 1),
                (Enemy("Goblin", 25, 4, 20, 15, 1), 30, 1),
                (Enemy("Wolf", 35, 6, 30, 25, 2), 15, 2),
                (Enemy("Bandit", 45, 8, 40, 35, 3), 10, 3),
                (Enemy("Troll", 80, 10, 50, 45, 4), 5, 4),
                # Boss enemies (rare spawn)
                (Enemy("Dragon", 200, 20, 100, 100, 5), 1, 5)
            ]
            
            roll = random.uniform(0, 100)
            cumulative = 0
            for enemy, chance, min_level in spawn_table:
                if player.level >= min_level:
                    cumulative += chance
                    if roll <= cumulative:
                        enemies = [enemy]
                        break
            
            if enemies:
                enemy = random.choice(enemies)
                result = combat(player, enemy)
                if result == "fled":
                    continue
                elif not result:
                    print(f"\nGame Over! Final Level: {player.level}")
                    print(f"Gold collected: {player.gold}")
                    break
            else:
                print("No suitable enemies found!")
                
        elif choice == "2":
            shop(player)
            
        elif choice == "3":
            show_inventory_menu(player)
            
        elif choice == "4":
            if player.gold >= 20:
                heal_amount = player.max_health // 2
                mana_amount = player.max_mana // 2
                player.health = min(player.max_health, player.health + heal_amount)
                player.mana = min(player.max_mana, player.mana + mana_amount)
                player.gold -= 20
                print(f"Rested and recovered {heal_amount} HP and {mana_amount} MP!")
            else:
                print("Not enough gold to rest!")
                
        elif choice == "5":
            show_abilities(player)
        
        elif choice == "6":
            gadget_shop(player)
            
        elif choice == "7":
            confirm = input("Are you sure you want to quit? (y/n): ").lower()
            if confirm == 'y':
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Game terminated.")