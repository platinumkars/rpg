import random
import time

def level_up_display(player, old_level, rewards):
    """Display level up information with visual effects"""
    print("\n" + "="*50)
    print(f"╔{'═'*48}╗")
    print(f"║{' '*17}LEVEL UP!{' '*22}║")
    print(f"║{' '*16}Level {old_level} → {player.level}{' '*21}║")
    print(f"╚{'═'*48}╝")
    print("\nStats increased:")
    print(f"♥ Max HP: {player.max_health - rewards['health']} → {player.max_health}")
    print(f"✧ Max MP: {player.max_mana - rewards['mana']} → {player.max_mana}")
    
    # Show new abilities if unlocked
    if player.level in [3, 5]:
        print("\n⚔ New Abilities Unlocked!")
        new_abilities = {name: ability for name, ability in player.abilities.items() 
                        if name not in ["Basic Attack"]}
        for name, ability in new_abilities.items():
            print(f"- {name}: {ability['description']}")
    
    print("="*50)
    time.sleep(1)  # Pause for effect

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
        self.gold = 100  # Increased starting gold
        self.inventory = {"Health Potion": 2, "Mana Potion": 2}
        self.weapons = {"Basic Sword": 8}
        self.current_weapon = "Basic Sword"
        self.abilities = {}
        self.status_effects = []
        self.armor = {"Basic Leather": 5}
        self.current_armor = "Basic Leather"
        self.tech_points = 0
        self.gadgets = {}
        self.powers = {}  # Dictionary to store unlocked powers
        
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
            if self.level >= 7:
                base_abilities["Battle Shout"] = {
                    "damage_boost": int(15 * scaling),
                    "duration": 3,
                    "mana_cost": 25,
                    "description": "Increase damage for 3 turns"
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
            if self.level >= 7:
                base_abilities["Chain Lightning"] = {
                    "damage": int(20 * scaling),
                    "hits": 3,
                    "effect": "stun",
                    "duration": 1,
                    "mana_cost": 45,
                    "description": "Lightning jumps between targets"
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
            if self.level >= 7:
                base_abilities["Holy Nova"] = {
                    "damage": int(30 * scaling),
                    "area_damage": int(20 * scaling),
                    "heal": int(25 * scaling),
                    "mana_cost": 40,
                    "description": "Area damage and group healing"
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
            if self.level >= 7:
                base_abilities["Soul Harvest"] = {
                    "damage": int(25 * scaling),
                    "heal": int(15 * scaling),
                    "hits": 3,
                    "mana_cost": 45,
                    "description": "Multiple life drains"
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
            if self.level >= 7:
                base_abilities["Shadow Dance"] = {
                    "damage": int(20 * scaling),
                    "hits": 5,
                    "mana_cost": 40,
                    "description": "Rapid strikes from shadows"
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
            if self.level >= 7:
                base_abilities["Nature's Fury"] = {
                    "damage": int(35 * scaling),
                    "area_damage": int(20 * scaling),
                    "effect": "root",
                    "duration": 2,
                    "mana_cost": 45,
                    "description": "Massive nature damage and root"
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
            if self.level >= 7:
                base_abilities["Chakra Burst"] = {
                    "damage": int(40 * scaling),
                    "hits": 3,
                    "heal": int(15 * scaling),
                    "mana_cost": 35,
                    "description": "Energy strikes with healing"
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
            if self.level >= 7:
                base_abilities["Arrow Storm"] = {
                    "damage": int(15 * scaling),
                    "hits": 6,
                    "area_damage": int(10 * scaling),
                    "mana_cost": 45,
                    "description": "Rain of arrows"
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
            if self.level >= 7:
                base_abilities["Soul Fire"] = {
                    "damage": int(50 * scaling),
                    "effect": "burn",
                    "duration": 3,
                    "mana_cost": 50,
                    "description": "Massive fire damage with burn"
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
            if self.level >= 7:
                base_abilities["Unstoppable"] = {
                    "damage": int(45 * scaling),
                    "heal": int(20 * scaling),
                    "effect": "rage",
                    "duration": 2,
                    "mana_cost": 40,
                    "description": "Powerful attack with healing rage"
                }

        elif self.class_type.lower() in ["alchemist", "11"]:
            self.health = 90 + (self.level - 1) * 15
            self.max_health = self.health
            self.mana = 80 + (self.level - 1) * 16
            self.max_mana = self.mana
            base_abilities = {
                "Acid Splash": {"damage": int(23 * scaling), "hits": 2, "mana_cost": 15, "description": "Corrosive damage over time"},
                "Healing Elixir": {"heal": int(30 * scaling), "mana_cost": 20, "description": "Powerful healing potion"}
            }
            if self.level >= 3:
                base_abilities["Explosive Flask"] = {
                    "damage": int(25 * scaling), 
                    "area_damage": int(20 * scaling),
                    "mana_cost": 25, 
                    "description": "Area damage chemical explosion"
                }
                base_abilities["Acid Flask"] = {
                    "damage": int(20 * scaling),
                    "effect": "acid",
                    "duration": 3,
                    "mana_cost": 25,
                    "description": "Throw corrosive acid that reduces defense"
                }
            if self.level >= 5:
                base_abilities["Transmutation"] = {
                    "heal": int(25 * scaling), 
                    "damage": int(25 * scaling), 
                    "mana_cost": 35,
                    "description": "Convert damage to healing"
                }
            if self.level >= 7:
                base_abilities["Chain Reaction"] = {
                    "damage": int(30 * scaling),
                    "area_damage": int(25 * scaling),
                    "effect": "acid",
                    "duration": 3,
                    "mana_cost": 45,
                    "description": "Explosive chain of reactions"
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
                    "area_damage": int(25 * scaling),
                    "effect": "stun",
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
            if self.level >= 7:
                base_abilities["Elemental Fury"] = {
                    "damage": int(25 * scaling),
                    "hits": 4,
                    "effect": "stun",
                    "duration": 1,
                    "mana_cost": 45,
                    "description": "Multiple elemental strikes"
                }

        self.abilities = base_abilities

    def unlock_power(self, power_name):
        """Unlock a new power if player has enough tech points"""
        if power_name in AVAILABLE_POWERS and power_name not in self.powers:
            power = AVAILABLE_POWERS[power_name]
            if self.tech_points >= power.cost:
                self.tech_points -= power.cost
                self.powers[power_name] = power
                print(f"Unlocked power: {power_name}!")
                print(f"Effect: {power.description}")
                return True
        return False

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

    def use(self):
        if self.charges > 0:
            self.charges -= 1
            return True
        return False

# Add Power class to define available powers
class Power:
    def __init__(self, name, effect, description, cost):
        self.name = name
        self.effect = effect
        self.description = description
        self.cost = cost  # Cost in tech points to unlock

# Add available powers dictionary
AVAILABLE_POWERS = {
    "Life Link": Power(
        "Life Link",
        {"heal_percent": 0.15, "cooldown": 3},
        "Heal 15% of damage dealt",
        100
    ),
    "Critical Strike": Power(
        "Critical Strike",
        {"crit_chance": 0.2, "crit_multiplier": 2.0},
        "20% chance to deal double damage",
        150
    ),
    "Mana Shield": Power(
        "Mana Shield",
        {"damage_to_mana": 0.3, "threshold": 0.5},
        "30% of damage taken uses mana instead when above 50% mana",
        200
    ),
    "Battle Rage": Power(
        "Battle Rage",
        {"damage_boost": 0.25, "health_threshold": 0.3},
        "Deal 25% more damage when below 30% health",
        250
    )
}

# Update Enemy class for better balance
class Enemy:
    def __init__(self, name, health, damage, exp_reward, gold_reward, level=1):
        self.name = name
        self.level = level
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

def get_target(enemies, auto=False):
    """Helper function to handle target selection"""
    if len(enemies) == 1 or auto:
        # Auto-target the first living enemy
        for enemy in enemies:
            if enemy.health > 0:
                return enemy
    else:
        print("\nChoose your target:")
        valid_targets = [(i, enemy) for i, enemy in enumerate(enemies, 1) if enemy.health > 0]
        for i, enemy in valid_targets:
            print(f"{i}. {enemy.name} - HP: {enemy.health}")
        
        try:
            target_idx = int(input("> ")) - 1
            if 0 <= target_idx < len(valid_targets):
                return enemies[target_idx]
        except ValueError:
            pass
    return None

# In the combat function, update the auto-target initialization
def combat(player, enemies):
    """Updated combat function with auto-targeting"""
    print("\nEnemies appear!")
    for enemy in enemies:
        print(f"- {enemy.name} (HP: {enemy.health})")
    
    # Set auto-target to False by default
    auto_target = False
    
    while any(enemy.health > 0 for enemy in enemies) and player.health > 0:
        # Process status effects
        process_status_effects(player)
        for enemy in enemies:
            if enemy.health > 0:
                process_status_effects(enemy)
        
        # Display battle status
        print(f"\n{'-'*40}")
        print(f"Your HP: {player.health}/{player.max_health}")
        print(f"Your MP: {player.mana}/{player.max_mana}")
        print("\nEnemies:")
        for i, enemy in enumerate(enemies, 1):
            if enemy.health > 0:
                print(f"{i}. {enemy.name} - HP: {enemy.health}")
        
        print("\nWhat would you like to do?")
        print("1. Attack")
        print("2. Use Ability")
        print("3. Use Item")
        print("4. Use Gadget")
        print("5. Run")
        print("6. Toggle Auto-target", f"({'ON' if auto_target else 'OFF'})")
        
        choice = input("> ")
        
        if choice == "6":
            auto_target = not auto_target
            print(f"Auto-targeting turned {'ON' if auto_target else 'OFF'}")
            continue
        
        # Target selection for attacks and abilities
        if choice in ["1", "2", "4"] and any(enemy.health > 0 for enemy in enemies):
            target = get_target(enemies, auto_target)
            if not target:
                print("Invalid target!")
                continue

        # Process player turn
        if choice == "1":  # Basic attack
            if target:
                process_attack(player, target, enemies)
            else:
                print("No valid target!")
                continue
            
        elif choice == "2":  # Use ability
            abilities_list = show_abilities(player)
            ability_choice = input("Choose ability number (or 'back'): ")
            
            if ability_choice.lower() == 'back':
                continue
            
            try:
                ability_idx = int(ability_choice) - 1
                if 0 <= ability_idx < len(abilities_list):
                    ability_name, ability = abilities_list[ability_idx]
                    if player.mana >= ability["mana_cost"]:
                        target = get_target(enemies, auto_target)
                        if target:
                            # Get duration from ability if it exists, otherwise default to 0
                            duration = ability.get("duration", 0)
                            process_ability(player, target, enemies, ability_name, duration)
                        else:
                            print("No valid target!")
                            continue
                    else:
                        print("Not enough mana!")
                        continue
                else:
                    print("Invalid ability number!")
                    continue
            except ValueError:
                print("Invalid input!")
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
                
        elif choice == "4":  # Use Gadget
            if player.gadgets:
                gadget_list = show_gadgets(player)
                if gadget_list:
                    gadget_choice = input("Choose gadget number (or 'back'): ")
                    
                    try:
                        gadget_idx = int(gadget_choice) - 1
                        if 0 <= gadget_idx < len(gadget_list):
                            _, gadget = gadget_list[gadget_idx]
                            if gadget.charges > 0:
                                gadget.charges -= 1
                                result = process_gadget_effect(player, target, enemies, gadget.effect)
                            name, gadget = gadget_list[gadget_idx]
                            if gadget.use(player, target):
                                result = process_gadget_effect(player, target, enemies, gadget.effect)
                                if result == "fled":
                                    return "fled"
                            else:
                                print("Failed to use gadget!")
                        else:
                            print("Invalid gadget number!")
                    except ValueError:
                        print("Invalid input!")
                else:
                    print("No charges remaining on any gadgets!")
            else:
                print("No gadgets available!")

        elif choice == "5":
            if random.random() < 0.5:
                print("You successfully fled from combat!")
                return "fled"  # Changed return value to indicate fled status
            else:
                print("You failed to run away!")
        
        # Enemy turns
        for enemy in enemies:
            if enemy.health > 0:
                damage = process_enemy_attack(player, enemy)
                player.health -= damage
                print(f"{enemy.name} attacks you for {damage} damage!")
        
        # Check player death
        if player.health <= 0:
            print("You have been defeated...")
            return False
            
    # Combat victory - remove duplicate rewards
    if player.health > 0:
        defeated_enemies = [e for e in enemies if e.health <= 0]
        total_exp = sum(e.exp_reward for e in defeated_enemies)
        total_gold = sum(e.gold_reward for e in defeated_enemies)
        total_tp = sum((player.level * 15) for e in defeated_enemies)
        
        # Apply rewards once
        player.exp += total_exp
        player.gold += total_gold
        player.tech_points += total_tp
        
        print(f"\nRewards:")
        print(f"• {total_exp} EXP")
        print(f"• {total_gold} Gold")
        if total_tp > 0:
            print(f"• {total_tp} Tech Points")

        # Remove duplicate exp addition
        old_level = player.level
        
        # Check for level up
        while player.exp >= calculate_exp_requirement(player.level):
            player.exp -= calculate_exp_requirement(player.level)
            player.level += 1
            rewards = calculate_level_rewards(player.level)
            player.max_health += rewards["health"]
            player.health = player.max_health
            player.max_mana += rewards["mana"]
            player.mana = player.max_mana
            
            # Display level up screen
            level_up_display(player, old_level, rewards)
            
            # Update abilities for new level
            player.update_abilities()
            old_level = player.level
        
        # Victory healing
        heal_amount = int(player.max_health * (0.15 + (player.level * 0.01)))
        mana_restore = int(player.max_mana * (0.1 + (player.level * 0.01)))
        player.health = min(player.max_health, player.health + heal_amount)
        player.mana = min(player.max_mana, player.mana + mana_restore)
        print(f"Victory healing: Recovered {heal_amount} HP and {mana_restore} MP!")
        
        return True

# Add gadget effect processing
def process_gadget_effect(player, target, enemies, effect):
    """Process gadget effects with proper targeting"""
    if isinstance(effect, dict):
        if "damage" in effect:
            # Handle single target damage
            damage = effect["damage"]
            target.health -= damage
            print(f"Gadget deals {damage} damage to {target.name}!")
            
            # Handle area damage if present
            if "area_damage" in effect:
                for other in enemies:
                    if other != target and other.health > 0:
                        other.health -= effect["area_damage"]
                        print(f"{other.name} takes {effect['area_damage']} splash damage!")
        
        if "heal" in effect:
            heal = effect["heal"]
            original_health = player.health
            player.health = min(player.max_health, player.health + heal)
            actual_heal = player.health - original_health
            print(f"Gadget heals you for {actual_heal} HP!")
        
        if "flee" in effect:
            if random.random() < effect.get("chance", 0.5):
                print("Gadget allows you to escape!")
                return "fled"
        
        if "defense" in effect:
            player.status_effects.append({
                "name": "Shield",
                "defense": effect["defense"],
                "duration": effect["duration"]
            })
            print(f"Shield activated! +{effect['defense']} defense for {effect['duration']} turns!")

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
        # Basic items (adjusted prices)
        "Health Potion": {"cost": 15, "effect": "Restore 35 HP", "min_level": 1},
        "Mana Potion": {"cost": 15, "effect": "Restore 30 MP", "min_level": 1},
        
        # Melee Weapons
        # Tier 1
        "Iron Sword": {"cost": 45, "damage": 10, "type": "melee", "min_level": 1},
        "Bronze Axe": {"cost": 50, "damage": 12, "type": "melee", "min_level": 1},
        
        # Tier 2
        "Steel Sword": {"cost": 140, "damage": 16, "type": "melee", "min_level": 3},
        "Battle Axe": {"cost": 150, "damage": 18, "type": "melee", "min_level": 3},
        "War Hammer": {
            "cost": 200, 
            "damage": 14, 
            "area_damage": 8, 
            "type": "melee",
            "min_level": 3,
            "description": "Heavy weapon that deals area damage"
        },
        
        # Tier 3
        "Flame Sword": {"cost": 280, "damage": 28, "type": "melee", "min_level": 5},
        "Dragon Cleaver": {
            "cost": 400, 
            "damage": 25, 
            "area_damage": 15, 
            "type": "melee",
            "min_level": 5,
            "description": "Massive sword with wide cleaving damage"
        },

        # Ranged Weapons
        # Tier 1
        "Wooden Bow": {"cost": 40, "damage": 8, "type": "ranged", "min_level": 1},
        "Wooden Staff": {"cost": 45, "damage": 8, "mana_bonus": 12, "type": "ranged", "min_level": 1},
        
        # Tier 2
        "Longbow": {"cost": 145, "damage": 15, "type": "ranged", "min_level": 3},
        "Magic Staff": {"cost": 160, "damage": 14, "mana_bonus": 20, "type": "ranged", "min_level": 3},
        "Thundering Bow": {
            "cost": 220, 
            "damage": 12, 
            "area_damage": 10, 
            "type": "ranged",
            "min_level": 3,
            "description": "Bow that creates lightning area damage"
        },
        
        # Tier 3
        "Frost Staff": {"cost": 290, "damage": 25, "mana_bonus": 35, "type": "ranged", "min_level": 5},
        "Storm Staff": {
            "cost": 450, 
            "damage": 22, 
            "area_damage": 18, 
            "mana_bonus": 30,
            "type": "ranged",
            "min_level": 5,
            "description": "Powerful staff that creates storm damage"
        },
        
        # Armor remains the same
        "Leather Armor": {"cost": 50, "defense": 6, "min_level": 1},
        "Chain Mail": {"cost": 120, "defense": 12, "min_level": 3},
        "Plate Armor": {"cost": 250, "defense": 20, "min_level": 5},

        # Multi-hit weapons
        "Twin Daggers": {
            "cost": 160,
            "damage": 8,
            "hits": 2,
            "type": "melee",
            "min_level": 3,
            "description": "Strike twice per attack"
        },
        "Triple Crossbow": {
            "cost": 180,
            "damage": 7,
            "hits": 3,
            "type": "ranged",
            "min_level": 3,
            "description": "Fire three bolts per attack"
        },
        "Flurry Blade": {
            "cost": 350,
            "damage": 12,
            "hits": 4,
            "type": "melee",
            "min_level": 5,
            "description": "Fast blade dealing multiple hits"
        }
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
            if player.level >= items[choice]["min_level"]:  # Check level requirement
                if player.gold >= items[choice]["cost"]:
                    # Store old gold for verification
                    old_gold = player.gold
                    player.gold -= items[choice]["cost"]
                    
                    # Verify transaction
                    if player.gold >= 0:
                        if "damage" in items[choice]:
                            if "area_damage" in items[choice]:
                                player.weapons[choice] = {
                                    "damage": items[choice]["damage"],
                                    "area_damage": items[choice]["area_damage"],
                                    "type": items[choice]["type"]
                                }
                            else:
                                player.weapons[choice] = items[choice]
                        elif "defense" in items[choice]:
                            player.armor[choice] = items[choice]["defense"]
                        else:
                            player.inventory[choice] = player.inventory.get(choice, 0) + 1
                        print(f"Bought {choice}!")
                        print(f"Remaining gold: {player.gold}")
                    else:
                        player.gold = old_gold  # Revert if something went wrong
                        print("Transaction failed!")
                else:
                    print("Not enough gold!")
            else:
                print(f"Required level: {items[choice]['min_level']}")
        else:
            print("Invalid item!")

# Add Gadget Shop function
def gadget_shop(player):
    """Shop for tech gadgets with balanced effects"""
    gadgets = {
        # Common gadgets (50 TP)
        "Smoke Bomb": Gadget("Smoke Bomb", "common", {
            "flee": True,
            "chance": 0.8,
            "description": "80% chance to escape combat"
        }, 50),
        "Health Injector": Gadget("Health Injector", "common", {
            "heal": 40,
            "description": "Restore 40 HP instantly"
        }, 50),
        "Energy Cell": Gadget("Energy Cell", "common", {
            "mana": 35,
            "description": "Restore 35 MP instantly"
        }, 50),
        
        # Rare gadgets (100 TP)
        "Shock Generator": Gadget("Shock Generator", "rare", {
            "damage": 60,
            "stun": 1,
            "description": "Deal 60 damage and stun for 1 turn"
        }, 100),
        "Force Field": Gadget("Force Field", "rare", {
            "defense": 25,
            "duration": 3,
            "description": "+25 defense for 3 turns"
        }, 100),
        "Multi Targeter": Gadget("Multi Targeter", "rare", {
            "damage": 30,
            "targets": 3,
            "description": "Hit 3 enemies for 30 damage each"
        }, 100),
        
        # Epic gadgets (200 TP)
        "Chrono Shifter": Gadget("Chrono Shifter", "epic", {
            "extra_turn": True,
            "heal": 30,
            "description": "Take another turn and heal 30 HP"
        }, 200),
        "Power Amplifier": Gadget("Power Amplifier", "epic", {
            "damage_boost": 1.5,
            "duration": 2,
            "description": "Increase damage by 50% for 2 turns"
        }, 200),
        
        # Legendary gadgets (400 TP)
        "Quantum Annihilator": Gadget("Quantum Annihilator", "legendary", {
            "damage": 150,
            "area_damage": 75,
            "description": "Deal 150 damage + 75 area damage"
        }, 400),
        "Phoenix Core": Gadget("Phoenix Core", "legendary", {
            "revive": True,
            "health_percent": 0.5,
            "description": "Revive with 50% HP when defeated"
        }, 400)
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

def power_shop(player):
    """Shop for unlocking new powers"""
    while True:
        print("\n=== Power Shop ===")
        print(f"Tech Points: {player.tech_points}")
        print("\nAvailable Powers:")
        
        for name, power in AVAILABLE_POWERS.items():
            if name not in player.powers:
                print(f"\n{name} - {power.cost} TP")
                print(f"Effect: {power.description}")
        
        print("\nEnter power name to unlock (or 'exit' to leave):")
        choice = input("> ").title()
        
        if choice.lower() == "exit":
            break
            
        if choice in AVAILABLE_POWERS:
            if choice not in player.powers:
                if player.unlock_power(choice):
                    print(f"Successfully unlocked {choice}!")
                else:
                    print("Not enough Tech Points!")
            else:
                print("Power already unlocked!")
        else:
            print("Invalid power name!")

def show_abilities(player):
    """Display available abilities with numbers"""
    print("\nAvailable Abilities:")
    abilities_list = list(player.abilities.items())
    for i, (ability, details) in enumerate(abilities_list, 1):
        desc = details['description']
        mana = details['mana_cost']
        print(f"{i}. {ability} - {desc} (Mana: {mana})")
    return abilities_list

def show_gadgets(player):
    """Display available gadgets with numbers"""
    gadget_list = []
    print("\nAvailable Gadgets:")
    for name, gadget in player.gadgets.items():
        if gadget.charges > 0:
            gadget_list.append((name, gadget))
            print(f"{len(gadget_list)}. {name} ({gadget.charges} charges)")
    return gadget_list

def process_attack(player, target, enemies):
    """Process attack with multi-hit and area damage"""
    weapon_stats = player.weapons[player.current_weapon]
    total_damage = 0
    living_enemies = [e for e in enemies if e.health > 0]
    current_target = target if target.health > 0 else None

    if not living_enemies:
        print("No valid targets remaining!")
        return total_damage

    if not current_target and living_enemies:
        current_target = living_enemies[0]
    
    # Calculate base damage
    if isinstance(weapon_stats, dict):
        base_damage = weapon_stats["damage"]
        level_bonus = int(player.level * 1.5)
        
        # Handle multi-hit weapons
        if "hits" in weapon_stats:
            hits = weapon_stats["hits"]
            enemy_index = living_enemies.index(current_target)
            
            for hit in range(hits):
                if not living_enemies:  # Stop if no more targets
                    break
                
                # Get current target, cycle through living enemies
                current_target = living_enemies[enemy_index % len(living_enemies)]
                
                variation = random.randint(-2, 2)
                hit_damage = max(1, base_damage + level_bonus + variation)
                
                current_target.health -= hit_damage
                total_damage += hit_damage
                print(f"Hit {hit + 1}: {hit_damage} damage to {current_target.name}!")
                
                # Check if current target died
                if current_target.health <= 0:
                    print(f"{current_target.name} has been defeated!")
                    living_enemies = [e for e in enemies if e.health > 0]
                    if living_enemies:
                        enemy_index = (enemy_index + 1) % len(living_enemies)
                    else:
                        break
                else:
                    enemy_index += 1
            
            print(f"Total damage dealt: {total_damage}")
            
        else:
            # Single hit processing
            variation = random.randint(-2, 2)
            main_damage = max(1, base_damage + level_bonus + variation)
            target.health -= main_damage
            total_damage = main_damage
            print(f"You deal {main_damage} damage to {target.name}!")
            
        # Process area damage
        if "area_damage" in weapon_stats and living_enemies:
            for other in living_enemies:
                if other != target and other.health > 0:
                    splash_damage = max(1, weapon_stats["area_damage"] + int(level_bonus * 0.5))
                    other.health -= splash_damage
                    total_damage += splash_damage
                    print(f"{other.name} takes {splash_damage} splash damage!")
    else:
        # Simple weapon damage
        variation = random.randint(-2, 2)
        main_damage = max(1, weapon_stats + int(player.level * 1.5) + variation)
        target.health -= main_damage
        total_damage = main_damage
        print(f"You deal {main_damage} damage to {target.name}!")
    
    return total_damage

def process_enemy_attack(player, enemy):
    """More balanced enemy damage calculation"""
    base_damage = enemy.damage
    armor_value = player.armor[player.current_armor]
    defense_reduction = int(armor_value * (0.3 + (player.level * 0.015)))  # Reduced scaling
    final_damage = max(1, base_damage - defense_reduction)
    return final_damage

def process_ability(player, target, enemies, ability_name, duration=0):
    """Process ability with multi-target and healing support"""
    ability = player.abilities[ability_name]
    player.mana -= ability["mana_cost"]
    total_damage = 0
    total_healing = 0
    
    # Get ability parameters
    base_damage = ability.get("damage", 0)
    base_heal = ability.get("heal", 0)
    hits = ability.get("hits", 1)
    effect_type = ability.get("effect", None)
    duration = ability.get("duration", duration)
    
    # Process healing over time
    if base_heal > 0 and duration > 0:
        player.status_effects.append({
            "name": "Regeneration",
            "heal": base_heal,
            "duration": duration
        })
        print(f"Regeneration effect: {base_heal} HP per turn for {duration} turns!")
    
    # Process immediate healing with hits
    elif base_heal > 0:
        for hit in range(hits):
            heal_amount = base_heal
            original_health = player.health
            player.health = min(player.max_health, player.health + heal_amount)
            actual_heal = player.health - original_health
            total_healing += actual_heal
            if actual_heal > 0:
                print(f"Heal {hit + 1}: Restored {actual_heal} HP!")
    
    # Process damage
    if "area_damage" in ability:
        # Area damage to all enemies
        main_damage = base_damage
        area_damage = ability["area_damage"]
        
        # Apply main damage to target
        target.health -= main_damage
        total_damage += main_damage
        print(f"Main damage: {main_damage} to {target.name}")
        
        # Apply area damage to other enemies
        for enemy in enemies:
            if enemy != target and enemy.health > 0:
                enemy.health -= area_damage
                total_damage += area_damage
                print(f"Area damage: {area_damage} to {enemy.name}")
                
    elif "hits" in ability:
        for hit in range(hits):
            if target.health > 0:
                target.health -= base_damage
                total_damage += base_damage
                print(f"Hit {hit + 1}: {base_damage} damage to {target.name}!")
                
                # Process healing from damage if ability has both
                if base_heal > 0:
                    heal_from_damage = int(base_damage * 0.5)  # 50% of damage dealt
                    original_health = player.health
                    player.health = min(player.max_health, player.health + heal_from_damage)
                    actual_heal = player.health - original_health
                    total_healing += actual_heal
                    if actual_heal > 0:
                        print(f"Life drain from hit {hit + 1}: Restored {actual_heal} HP!")
    
    if total_healing > 0:
        print(f"Total healing done: {total_healing}")
    if total_damage > 0:
        print(f"Total damage dealt: {total_damage}")
    
    # Apply status effect if present
    if effect_type:
        apply_status_effect(target, effect_type, base_damage, duration)
    
    return total_damage

def apply_status_effect(target, effect_type, base_damage, duration):
    """Helper function to apply status effects"""
    if effect_type == "burn":
        target.status_effects.append({
            "name": "Burned",
            "damage": base_damage // 2,
            "duration": duration
        })
        print(f"{target.name} is burned for {duration} turns!")
        
    elif effect_type == "acid":
        # Acid reduces defense and does damage over time
        target.status_effects.append({
            "name": "Corroded",
            "damage": base_damage // 3,
            "defense_reduction": 5,
            "duration": duration
        })
        print(f"{target.name} is corroded for {duration} turns!")
        
    elif effect_type == "freeze":
        target.status_effects.append({
            "name": "Frozen",
            "damage": base_damage // 2,
            "duration": duration,
            "damage_reduction": 0.5
        })
        print(f"{target.name} is frozen for {duration} turns!")
    elif effect_type == "stun":
        target.status_effects.append({
            "name": "Stunned",
            "duration": duration
        })
        print(f"{target.name} is stunned for {duration} turns!")

def process_status_effects(entity):
    """Process status effects at the start of turn"""
    is_stunned = False
    damage_multiplier = 1.0
    
    for effect in entity.status_effects[:]:
        if effect["name"] == "Corroded":
            damage = effect["damage"]
            entity.health -= damage
            print(f"{entity.name} takes {damage} acid damage!")
            # Apply defense reduction if entity has armor
            if hasattr(entity, 'armor') and entity.current_armor:
                current_defense = entity.armor[entity.current_armor]
                reduced_defense = max(0, current_defense - effect["defense_reduction"])
                entity.armor[entity.current_armor] = reduced_defense
                print(f"{entity.name}'s armor is corroded! Defense reduced to {reduced_defense}!")
        elif effect["name"] == "Poison":
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
            print(f"{entity.name} is stunned and skips their turn!")
            
        effect["duration"] -= 1
        if effect["duration"] <= 0:
            entity.status_effects.remove(effect)
            print(f"{effect['name']} effect has worn off!")
            
    return is_stunned, damage_multiplier


# Update show_inventory_menu function
def show_inventory_menu(player):
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
            
            print("\nMelee Weapons:")
            for weapon, stats in player.weapons.items():
                if isinstance(stats, dict) and stats.get("type") == "melee":
                    print(f"{weapon} (Damage: {stats['damage']})")
            
            print("\nRanged Weapons:")
            for weapon, stats in player.weapons.items():
                if isinstance(stats, dict) and stats.get("type") == "ranged":
                    desc = f"Damage: {stats['damage']}"
                    if "mana_bonus" in stats:
                        desc += f", Mana Bonus: {stats['mana_bonus']}"
                    print(f"{weapon} ({desc})")
            
            print(f"\nCurrently equipped weapon: {player.current_weapon}")
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

# Update the EnemyType class with better scaling
class EnemyType:
    def __init__(self, name, base_health, base_damage, exp_reward, gold_reward, min_level=1):
        self.name = name
        self.base_health = base_health
        self.base_damage = base_damage
        self.base_exp = exp_reward
        self.base_gold = gold_reward
        self.min_level = min_level

    def scale_to_level(self, player_level):
        """Scale enemy stats based on player level"""
        level_diff = max(0, player_level - self.min_level)
        scaling = 1 + (level_diff * 0.2)  # 20% increase per level difference
        
        return Enemy(
            self.name,
            int(self.base_health * scaling),
            int(self.base_damage * scaling),
            int(self.base_exp * scaling),
            int(self.base_gold * scaling),
            min(player_level, self.min_level + 2)  # Cap enemy level
        )

# Update spawn table with base stats
spawn_table = [
    # Level 1 enemies
    (EnemyType("Goblin", 65, 15, 20, 25, 1), 20, 1),      # Base: 65 HP, 15 DMG
    (EnemyType("Wolf", 75, 18, 25, 30, 1), 20, 1),        # Base: 75 HP, 18 DMG
    (EnemyType("Slime", 55, 12, 15, 20, 1), 15, 1),       # Base: 55 HP, 12 DMG
    
    # Level 2 enemies
    (EnemyType("Bandit", 85, 22, 35, 45, 2), 15, 2),      # Base: 85 HP, 22 DMG
    (EnemyType("Skeleton", 80, 25, 30, 40, 2), 15, 2),     # Base: 80 HP, 25 DMG
    (EnemyType("Giant Spider", 78, 28, 32, 38, 2), 15, 2), # Base: 78 HP, 28 DMG
    
    # Level 3 enemies
    (EnemyType("Orc", 110, 32, 45, 50, 3), 12, 3),        # Base: 110 HP, 32 DMG
    (EnemyType("Dark Elf", 95, 35, 48, 55, 3), 12, 3),    # Base: 95 HP, 35 DMG
    (EnemyType("Werewolf", 120, 38, 50, 58, 3), 12, 3),   # Base: 120 HP, 38 DMG
    
    # Level 4 enemies
    (EnemyType("Troll", 150, 42, 60, 65, 4), 10, 4),      # Base: 150 HP, 42 DMG
    (EnemyType("Ogre", 165, 45, 65, 70, 4), 10, 4),       # Base: 165 HP, 45 DMG
    (EnemyType("Gargoyle", 140, 48, 70, 75, 4), 10, 4),   # Base: 140 HP, 48 DMG
    
    # Level 5+ special enemies
    (EnemyType("Dragon Whelp", 200, 55, 100, 120, 5), 5, 5), # Base: 200 HP, 55 DMG
    (EnemyType("Necromancer", 180, 58, 110, 130, 5), 5, 5),  # Base: 180 HP, 58 DMG
    (EnemyType("Giant", 250, 52, 120, 150, 5), 5, 5)         # Base: 250 HP, 52 DMG
]

# Define enemy types as a class for better organization
class EnemyType:
    def __init__(self, name, max_health, damage, exp_reward, gold_reward, level=1):
        self.name = name
        self.max_health = max_health
        self.damage = damage
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.level = level

# Replace the existing spawn_table with these balanced enemies
spawn_table = [
    # Level 1 enemies (balanced for higher player health)
    (EnemyType("Goblin", 45, 12, 20, 25, 1), 20, 1),      # HP: 30->45, DMG: 8->12
    (EnemyType("Wolf", 50, 15, 25, 30, 1), 20, 1),        # HP: 35->50, DMG: 10->15
    (EnemyType("Slime", 40, 10, 15, 20, 1), 15, 1),       # HP: 25->40, DMG: 6->10
    
    # Level 2 enemies
    (EnemyType("Bandit", 65, 18, 35, 45, 2), 15, 2),      # HP: 45->65, DMG: 12->18
    (EnemyType("Skeleton", 60, 20, 30, 40, 2), 15, 2),     # HP: 40->60, DMG: 13->20
    (EnemyType("Giant Spider", 58, 22, 32, 28, 2), 15, 2), # HP: 38->58, DMG: 14->22
    
    # Level 3 enemies
    (EnemyType("Orc", 85, 25, 45, 40, 3), 12, 3),         # HP: 60->85, DMG: 15->25
    (EnemyType("Dark Elf", 80, 28, 48, 45, 3), 12, 3),    # HP: 55->80, DMG: 18->28
    (EnemyType("Werewolf", 90, 30, 50, 48, 3), 12, 3),    # HP: 65->90, DMG: 20->30
    
    # Level 4 enemies
    (EnemyType("Troll", 120, 35, 60, 50, 4), 10, 4),      # HP: 80->120, DMG: 20->35
    (EnemyType("Ogre", 130, 38, 65, 55, 4), 10, 4),       # HP: 85->130, DMG: 22->38
    (EnemyType("Gargoyle", 110, 40, 70, 60, 4), 10, 4),   # HP: 75->110, DMG: 25->40
    
    # Level 5+ special enemies
    (EnemyType("Dragon Whelp", 180, 45, 100, 100, 5), 5, 5), # HP: 100->180, DMG: 30->45
    (EnemyType("Necromancer", 150, 50, 110, 110, 5), 5, 5),  # HP: 90->150, DMG: 35->50
    (EnemyType("Giant", 200, 42, 120, 120, 5), 5, 5)         # HP: 120->200, DMG: 28->42
]

def currency_exchange(player):
    """Exchange gold for tech points and vice versa"""
    GOLD_TO_TP_RATE = 10  # 100 gold = 1 tech point
    TP_TO_GOLD_RATE = 10   # 1 tech point = 100 gold 
    
    while True:
        print("\n=== Currency Exchange ===")
        print(f"Gold: {player.gold}")
        print(f"Tech Points: {player.tech_points}")
        print(f"\nExchange Rates:")
        print(f"• {GOLD_TO_TP_RATE} Gold -> 1 Tech Point")
        print(f"• 1 Tech Point -> {TP_TO_GOLD_RATE} Gold")
        print("\nOptions:")
        print("1. Convert Gold to Tech Points")
        print("2. Convert Tech Points to Gold")
        print("3. Back")
        
        choice = input("> ")
        
        if choice == "1":
            max_conversion = player.gold // GOLD_TO_TP_RATE
            if max_conversion < 1:
                print(f"Not enough gold! You need at least {GOLD_TO_TP_RATE} gold.")
                continue
                
            print(f"\nYou can convert up to {max_conversion} tech points")
            try:
                amount = int(input("How many tech points to buy? (0 to cancel): "))
                if 0 < amount <= max_conversion:
                    gold_cost = amount * GOLD_TO_TP_RATE
                    player.gold -= gold_cost
                    player.tech_points += amount
                    print(f"Converted {gold_cost} gold to {amount} tech points!")
                elif amount != 0:
                    print("Invalid amount!")
            except ValueError:
                print("Invalid input!")
                
        elif choice == "2":
            if player.tech_points < 1:
                print("Not enough tech points!")
                continue
                
            print(f"\nYou can convert up to {player.tech_points} tech points")
            try:
                amount = int(input("How many tech points to convert? (0 to cancel): "))
                if 0 < amount <= player.tech_points:
                    gold_gain = amount * TP_TO_GOLD_RATE
                    player.tech_points -= amount
                    player.gold += gold_gain
                    print(f"Converted {amount} tech points to {gold_gain} gold!")
                elif amount != 0:
                    print("Invalid amount!")
            except ValueError:
                print("Invalid input!")
                
        elif choice == "3":
            break

# Fix enemy spawn logic in main()
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
        print("4. Rest (Heal 50% HP/MP for 15 gold)")
        print("5. Show abilities")
        print("6. Visit gadget shop") 
        print("7. Currency Exchange")
        print("8. Visit power shop")
        print("9. Quit")
        
        choice = input("> ")
        if choice == "1":
            num_enemies = 1
            if player.level >= 5:
                num_enemies = random.randint(2, 3)
            
            # Initialize empty enemies list
            enemies = []
            
            # Fix the enemy spawn loop
            for _ in range(num_enemies):
                roll = random.uniform(0, 100)
                cumulative = 0
                for enemy_type, chance, min_level in spawn_table:
                    if player.level >= min_level:
                        cumulative += chance
                        if roll <= cumulative:
                            new_enemy = Enemy(
                                enemy_type.name,
                                enemy_type.max_health,
                                enemy_type.damage,
                                enemy_type.exp_reward,
                                enemy_type.gold_reward,
                                enemy_type.level
                            )
                            enemies.append(new_enemy)
                            break

            # Remove duplicate combat call and time.sleep
            if enemies:
                result = combat(player, enemies)
                if not result:
                    print(f"\nGame Over! Final Level: {player.level}")
                    print(f"Gold collected: {player.gold}")
                    break
            else:
                print("\nNo suitable enemies found in this area!")
                print("Try exploring a different area or coming back later.")
                time.sleep(1)

        elif choice == "2":
            shop(player)
           
        elif choice == "3":
            show_inventory_menu(player)
            
        elif choice == "4":
            rest_cost = 15
            if player.gold >= rest_cost:
                heal_amount = player.max_health // 2
                mana_amount = player.max_mana // 2
                player.health = min(player.max_health, player.health + heal_amount)
                player.mana = min(player.max_mana, player.mana + mana_amount)
                player.gold -= rest_cost
                print(f"Rested and recovered {heal_amount} HP and {mana_amount} MP!")
            else:
                print("Not enough gold to rest!")
                        
        elif choice == "5":
            show_abilities(player)
            
        elif choice == "6":
            gadget_shop(player)
            
        elif choice == "7":
            currency_exchange(player)
            
        elif choice == "8":
            power_shop(player)
            
        elif choice == "9":
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
