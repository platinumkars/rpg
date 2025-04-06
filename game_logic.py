import random
import time
import json
import os
from datetime import datetime

# Add at the top with other constants
COMPANION_TIERS = {
    5: {  # Level 5 companions
        "cat": {
            "health": 60,
            "damage": 12,
            "ability": "Agile Strike", 
            "description": "20% chance to dodge attacks"
        },
        "owl": {
            "health": 45,
            "damage": 10,
            "ability": "Night Vision",
            "description": "Reveals enemy weaknesses, increasing damage by 25%"
        }
    },
    8: {  # Level 8 companions
        "bear": {
            "health": 100,
            "damage": 20,
            "ability": "Mighty Roar",
            "description": "Intimidates enemies, reducing their damage by 15%"
        },
        "fox": {
            "health": 70,
            "damage": 15,
            "ability": "Cunning",
            "description": "35% chance to strike twice"
        }
    },
    12: {  # Level 12 companions
        "unicorn": {
            "health": 90,
            "damage": 18,
            "ability": "Holy Light",
            "description": "Heals player for 20% of damage dealt"
        },
        "griffin": {
            "health": 110,
            "damage": 22,
            "ability": "Sky Strike",
            "description": "Can attack multiple enemies for 60% damage"
        }
    }
}

COMPANION_QUESTS = {
    "Forest Trial": {
        "level_req": 7,
        "description": "Defeat the Ancient Treant without using potions",
        "reward": "Additional companion slot and a companion token",
        "boss": {
            "name": "Ancient Treant",
            "health": 300,
            "damage": 25,
            "special": {"Nature's Wrath": {"damage": 40, "area_damage": 20}}
        },
        "quest_rules": {"no_potions": True}
    },
    "Spirit Challenge": {
        "level_req": 10,
        "description": "Survive 5 turns against the Spirit King with <30% HP",
        "reward": "Additional companion slot and a companion tokens",
        "boss": {
            "name": "Spirit King",
            "health": 400,
            "damage": 30,
            "special": {"Soul Drain": {"damage": 35, "heal": 35}}
        },
        "quest_rules": {"turns": 5, "health_threshold": 0.3}
    }
}

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
        self.bonus_defense = 0  # Track temporary defense bonuses from abilities and effects
        self.base_defense = 0   # Track base defense value
        self.defense_modifiers = []  # Store active defense modifiers
        self.defense_effects = []
        self.armor = {"Basic Leather": 5}
        self.current_armor = "Basic Leather"
        self.tech_points = 0
        self.gadgets = {}
        self.powers = {}  # Dictionary to store unlocked powers
        self.companions = []
        self.max_companions = 1
        self.companion_quests_completed = []
        self.companion_tokens = 0
        self.companion_upgrades = {
            "health": 0,
            "damage": 0,
            "ability": 0
        }

        # Add basic abilities that all classes get
        self.abilities = {}

        # Initialize and merge class-specific abilities
        self.update_abilities()
        
        # Add character-specific abilities based on name choice
        print("\nChoose your character's special ability type:")
        print("1. Dragon Blood - Fire-based abilities")
        print("2. Shadow Walker - Stealth and darkness abilities")
        print("3. Storm Born - Lightning-based abilities")
        print("4. Frost Heart - Ice-based abilities")
        print("5. Blood Mage - Blood magic abilities")
        print("6. Light Bearer - Holy light abilities")
        print("7. Nature's Child - Nature-based abilities")
        print("8. Tech Master - Technology-based abilities")
        
        while True:
            try:
                ability_choice = int(input("\nEnter your choice (1-8): "))
                if 1 <= ability_choice <= 8:
                    self.special_type = ability_choice
                    self.add_special_abilities()
                    break
                print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
        
    def get_scaling_factor(self):
        """Calculate scaling factor based on level"""
        return 1 + (self.level - 1) * 0.15
        
    def update_abilities(self):
        """Update abilities while preserving special abilities"""
        # Store special abilities before update
        special_abilities = {}
        if hasattr(self, 'special_type'):
            special_abilities = {name: ability for name, ability in self.abilities.items() 
                               if name in ["Dragon's Breath", "Shadow Fusion", "Thunder Strike", 
                                         "Glacial Storm", "Blood Ritual", "Divine Radiance", 
                                         "Primal Surge", "Overclock"]}
        
        # Regular ability update
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
            if self.level >= 9:
                base_abilities["Heroic Strike"] = {
                    "damage": int(85 * scaling),
                    "area_damage": int(45 * scaling),
                    "effect": "stun",
                    "duration": 2,
                    "mana_cost": 65,
                    "description": "Massive area attack that stuns enemies"
                }
            if self.level >= 11:
                base_abilities["Ultimate Warrior"] = {
                    "damage": int(100 * scaling),
                    "heal": int(50 * scaling),
                    "effect": "rage",
                    "duration": 3,
                    "mana_cost": 80,
                    "description": "Unleash ultimate warrior power, massive damage and healing"
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
            if self.level >= 9:
                base_abilities["Arcane Barrage"] = {
                    "damage": int(40 * scaling),
                    "hits": 5,
                    "effect": "freeze",
                    "duration": 2,
                    "mana_cost": 70,
                    "description": "Multiple arcane missiles with freeze"
                }
            if self.level >= 11:
                base_abilities["Dimensional Rift"] = {
                    "damage": int(120 * scaling),
                    "area_damage": int(60 * scaling),
                    "effect": ["freeze", "stun"],
                    "duration": 2,
                    "mana_cost": 85,
                    "description": "Open a devastating magical rift"
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
            if self.level >= 9:
                base_abilities["Divine Judgment"] = {
                    "damage": int(75 * scaling),
                    "heal": int(40 * scaling),
                    "area_damage": int(35 * scaling),
                    "effect": "holy",
                    "duration": 3,
                    "mana_cost": 75,
                    "description": "Holy strike with area healing"
                }
            if self.level >= 11:
                base_abilities["Divine Intervention"] = {
                    "heal": int(80 * scaling),
                    "area_damage": int(70 * scaling),
                    "effect": "holy",
                    "duration": 3,
                    "mana_cost": 75,
                    "description": "Call upon ultimate divine power"
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
            if self.level >= 9:
                base_abilities["Death's Embrace"] = {
                    "damage": int(65 * scaling),
                    "hits": 4,
                    "effect": "curse",
                    "duration": 3,
                    "heal": int(30 * scaling),
                    "mana_cost": 70,
                    "description": "Multiple dark strikes with life drain"
                }
            if self.level >= 11:
                base_abilities["Army of Darkness"] = {
                    "damage": int(40 * scaling),
                    "hits": 6,
                    "effect": "curse",
                    "duration": 3,
                    "mana_cost": 90,
                    "description": "Summon multiple dark minions to attack"
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
            if self.level >= 9:
                base_abilities["Fatal Dance"] = {
                    "damage": int(50 * scaling),
                    "hits": 6,
                    "effect": "bleed",
                    "duration": 2,
                    "mana_cost": 65,
                    "description": "Rapid deadly strikes causing bleeding"
                }
            if self.level >= 11:
                base_abilities["Death's Dance"] = {
                    "damage": int(45 * scaling),
                    "hits": 8,
                    "effect": "bleed",
                    "duration": 2,
                    "mana_cost": 70,
                    "description": "Execute a deadly series of strikes"
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
            if self.level >= 9:
                base_abilities["Nature's Wrath"] = {
                    "damage": int(70 * scaling),
                    "area_damage": int(35 * scaling),
                    "heal": int(35 * scaling),
                    "effect": ["root", "poison"],
                    "duration": 3,
                    "mana_cost": 75,
                    "description": "Unleash nature's fury with healing"
                }
            if self.level >= 11:
                base_abilities["Force of Nature"] = {
                    "damage": int(90 * scaling),
                    "area_damage": int(45 * scaling),
                    "heal": int(45 * scaling),
                    "effect": ["root", "regenerate"],
                    "duration": 3,
                    "mana_cost": 85,
                    "description": "Channel pure nature's fury"
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
            if self.level >= 9:
                base_abilities["Zen Assault"] = {
                    "damage": int(45 * scaling),
                    "hits": 5,
                    "heal": int(25 * scaling),
                    "effect": "stun",
                    "duration": 2,
                    "mana_cost": 60,
                    "description": "Rapid strikes with healing and stun"
                }
            if self.level >= 11:
                base_abilities["Transcendence"] = {
                    "damage": int(50 * scaling),
                    "hits": 5,
                    "heal": int(40 * scaling),
                    "effect": "enlightened",
                    "duration": 3,
                    "mana_cost": 75,
                    "description": "Achieve perfect harmony of attack and defense"
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
            if self.level >= 9:
                base_abilities["Piercing Storm"] = {
                    "damage": int(35 * scaling),
                    "hits": 8,
                    "area_damage": int(20 * scaling),
                    "effect": "pierce",
                    "duration": 2,
                    "mana_cost": 70,
                    "description": "Rain of piercing arrows"
                }
            if self.level >= 11:
                base_abilities["Rain of Arrows"] = {
                    "damage": int(30 * scaling),
                    "hits": 10,
                    "area_damage": int(25 * scaling),
                    "effect": "pierce",
                    "duration": 2,
                    "mana_cost": 80,
                    "description": "Unleash a devastating arrow barrage"
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
            if self.level >= 9:
                base_abilities["Demonic Fury"] = {
                    "damage": int(80 * scaling),
                    "area_damage": int(40 * scaling),
                    "effect": ["burn", "curse"],
                    "duration": 3,
                    "mana_cost": 80,
                    "description": "Unleash demonic destruction"
                }
            if self.level >= 11:
                base_abilities["Apocalypse"] = {
                    "damage": int(110 * scaling),
                    "area_damage": int(55 * scaling),
                    "effect": ["burn", "curse"],
                    "duration": 3,
                    "mana_cost": 95,
                    "description": "Unleash pure demonic destruction"
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
            if self.level >= 9:
                base_abilities["Battle Frenzy"] = {
                    "damage": int(55 * scaling),
                    "hits": 5,
                    "heal": int(25 * scaling),
                    "effect": "rage",
                    "duration": 3,
                    "mana_cost": 65,
                    "description": "Frenzied attacks with life drain"
                }
            if self.level >= 11:
                base_abilities["Berserker Fury"] = {
                    "damage": int(60 * scaling),
                    "hits": 6,
                    "heal": int(30 * scaling),
                    "effect": "berserk",
                    "duration": 3,
                    "mana_cost": 85,
                    "description": "Enter ultimate berserker state"
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
            if self.level >= 9:
                base_abilities["Catalyst Burst"] = {
                    "damage": int(70 * scaling),
                    "area_damage": int(35 * scaling),
                    "effect": ["acid", "poison"],
                    "duration": 3,
                    "mana_cost": 75,
                    "description": "Explosive chemical reaction"
                }
            if self.level >= 11:
                base_abilities["Grand Synthesis"] = {
                    "damage": int(85 * scaling),
                    "area_damage": int(40 * scaling),
                    "heal": int(40 * scaling),
                    "effect": ["acid", "regenerate"],
                    "duration": 3,
                    "mana_cost": 80,
                    "description": "Ultimate alchemical reaction"
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
            if self.level >= 9:
                base_abilities["Storm Ritual"] = {
                    "damage": int(40 * scaling),
                    "hits": 6,
                    "area_damage": int(30 * scaling),
                    "effect": ["stun", "lightning"],
                    "duration": 2,
                    "mana_cost": 70,
                    "description": "Chain of elemental strikes"
                }
            if self.level >= 11:
                base_abilities["Spirit Storm"] = {
                    "damage": int(45 * scaling),
                    "hits": 7,
                    "area_damage": int(35 * scaling),
                    "effect": ["stun", "spirit"],
                    "duration": 3,
                    "mana_cost": 90,
                    "description": "Unleash a storm of spiritual energy"
                }

        self.abilities = base_abilities
        
        # Restore special abilities
        self.abilities.update(special_abilities)

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

    def add_special_abilities(self):
        """Add basic and special abilities"""
        scaling = self.get_scaling_factor()
        
        # Add basic abilities that all characters get
        basic_abilities = {
            "Basic Attack": {
                "damage": int(10 * scaling),
                "mana_cost": 0,
                "description": "Basic weapon attack"
            },
            "Power Strike": {
                "damage": int(15 * scaling),
                "mana_cost": 10, 
                "description": "A stronger attack with increased damage"
            },
            "Quick Shot": {
                "damage": int(12 * scaling),
                "hits": 2,
                "mana_cost": 15,
                "description": "Fire two quick attacks"
            },
            "Minor Heal": {
                "heal": int(20 * scaling),
                "mana_cost": 15,
                "description": "Restore some health points"
            },
            "Focus": {
                "mana": 25,
                "mana_cost": 0,
                "cooldown": 3,
                "effect": "focus",
                "description": "Restore mana and increase next attack damage"
            }
        }
        
        # Add basic abilities first
        self.abilities.update(basic_abilities)
        print("\n✨ Basic Abilities Unlocked!")
        
        # Special character abilities
        special_abilities = {
            1: {  # Dragon Blood
                "Dragon's Breath": {
                    "damage": int(80 * scaling),
                    "area_damage": int(40 * scaling),
                    "effect": "burn",
                    "duration": 3,
                    "mana_cost": 65,
                    "description": "Unleash powerful dragon flame"
                }
            },
            2: {  # Shadow Walker
                "Shadow Fusion": {
                    "damage": int(70 * scaling),
                    "hits": 4,
                    "effect": "blind",
                    "duration": 2,
                    "mana_cost": 60,
                    "description": "Strike from the shadows with multiple hits"
                }
            },
            3: {  # Storm Born
                "Thunder Strike": {
                    "damage": int(65 * scaling),
                    "area_damage": int(35 * scaling),
                    "effect": "stun",
                    "duration": 2,
                    "mana_cost": 70,
                    "description": "Call down devastating lightning"
                }
            },
            4: {  # Frost Heart
                "Glacial Storm": {
                    "damage": int(75 * scaling),
                    "area_damage": int(38 * scaling),
                    "effect": "freeze",
                    "duration": 3,
                    "mana_cost": 65,
                    "description": "Unleash a devastating ice storm"
                }
            },
            5: {  # Blood Mage
                "Blood Ritual": {
                    "damage": int(60 * scaling),
                    "heal": int(40 * scaling),
                    "effect": "lifesteal",
                    "duration": 2,
                    "mana_cost": 75,
                    "description": "Sacrifice health for powerful magic"
                }
            },
            6: {  # Light Bearer
                "Divine Radiance": {
                    "damage": int(70 * scaling),
                    "heal": int(45 * scaling),
                    "area_damage": int(35 * scaling),
                    "effect": "holy",
                    "duration": 2,
                    "mana_cost": 80,
                    "description": "Channel pure divine light"
                }
            },
            7: {  # Nature's Child
                "Primal Surge": {
                    "damage": int(55 * scaling),
                    "heal": int(35 * scaling),
                    "area_damage": int(30 * scaling),
                    "effect": ["root", "regenerate"],
                    "duration": 3,
                    "mana_cost": 70,
                    "description": "Unleash nature's raw power"
                }
            },
            8: {  # Tech Master
                "Overclock": {
                    "damage": int(75 * scaling),
                    "hits": 5,
                    "effect": "stun",
                    "duration": 2,
                    "mana_cost": 85,
                    "description": "Supercharge your abilities"
                }
            }
        }
        
        # Add special ability to character's abilities
        if self.special_type in special_abilities:
            self.abilities.update(special_abilities[self.special_type])
            ability_name = list(special_abilities[self.special_type].keys())[0]
            print(f"\n✨ Special Ability Unlocked: {ability_name}")
            print(f"📜 {special_abilities[self.special_type][ability_name]['description']}")

    def unlock_companion(self):
        """Enhanced companion unlock system"""
        if len(self.companions) >= self.max_companions:
            print("\n❌ No free companion slots!")
            print("Complete companion quests to unlock more slots!")
            return
            
        print("\n🐾 Available Companions:")
        available_companions = []
        
        for req_level, companions in COMPANION_TIERS.items():
            if self.level >= req_level:
                print(f"\nLevel {req_level} Companions:")
                for comp_type, stats in companions.items():
                    available_companions.append(comp_type)
                    print(f"- {comp_type.title()}: {stats['description']}")
        
        if not available_companions:
            print("No companions available at your level!")
            return
            
        while True:
            choice = input("\nChoose companion type (or 'back'): ").lower()
            if choice == 'back':
                return
                
            if choice in available_companions:
                name = input(f"\nName your {choice.title()}: ")
                companion = Companion(name, choice)
                self.companions.append(companion)
                print(f"\n✨ {name} has joined your party!")
                break
            print("Invalid choice!")

    # Add to Character class
    def start_quest_menu(self):
        """Display and handle companion quest menu"""
        while True:
            print("\n=== Companion Quests ===")
            available_quests = []
            
            for quest_name, quest in COMPANION_QUESTS.items():
                # Show level requirement and completion status
                status = "✅ Completed" if quest_name in self.companion_quests_completed else "❌ Incomplete"
                level_status = "✨" if self.level >= quest["level_req"] else "🔒"
                
                if self.level >= quest["level_req"] and quest_name not in self.companion_quests_completed:
                    available_quests.append(quest_name)
                    print(f"\n{level_status} {quest_name} (Level {quest['level_req']}+) - {status}")
                    print(f"📜 {quest['description']}")
                    print(f"🎁 Reward: {quest['reward']}")
            
            if not available_quests:
                print("\nNo available quests right now!")
                input("\nPress Enter to continue...")
                break
                
            print("\nEnter quest name to start (or 'back' to return):")
            choice = input("> ")
            
            if choice.lower() == 'back':
                break
                
            if choice in available_quests:
                self.start_companion_quest(choice)

    def start_companion_quest(self, quest_name):
        """Handle companion quest logic"""
        if quest_name not in COMPANION_QUESTS:
            print("Invalid quest!")
            return
            
        quest = COMPANION_QUESTS[quest_name]
        if self.level < quest["level_req"]:
            print(f"You need to be level {quest['level_req']} for this quest!")
            return
            
        if quest_name in self.companion_quests_completed:
            print("You've already completed this quest!")
            return
            
        print(f"\n=== {quest_name} ===")
        print(f"📜 {quest['description']}")
        print(f"🎁 Reward: {quest['reward']}")
        
        confirm = input("\nStart quest? (y/n): ").lower()
        if confirm == 'y':
            # Create boss for the quest
            boss_info = quest["boss"]
            boss = Boss(
                name=boss_info["name"],
                health=boss_info["health"],
                exp_reward=200,
                gold_reward=300,
                special_moves=boss_info["special"],
                level_req=quest["level_req"]
            )
            
            # Scale boss to player level
            boss.scale_stats(self.level)
            
            # Start boss battle
            result = combat(self, [boss])
            if result is True:  # Victory
                print(f"\n🎊 Congratulations! You've completed {quest_name}!")
                self.max_companions += 1
                self.companion_quests_completed.append(quest_name)
                self.companion_tokens += 1
                print(f"\n✨ You can now have up to {self.max_companions} companions!")
                print("You've earned a companion token!")
                
                if len(self.companions) < self.max_companions:
                    if input("\nWould you like to recruit a new companion? (y/n): ").lower() == 'y':
                        self.unlock_companion()

    def upgrade_companion(self):
            """Upgrade companion stats with tokens"""
            if not self.companions:
                print("No companions to upgrade!")
                return

            if self.companion_tokens <= 0:
                print("No upgrade tokens available!")
                return

            print("\n=== Companion Upgrade ===")
            print(f"Available Tokens: {self.companion_tokens}")
            print("\nUpgrade Options:")
            print(f"1. Health (Level {self.companion_upgrades['health']}/5) - +20% HP")
            print(f"2. Damage (Level {self.companion_upgrades['damage']}/5) - +20% DMG")
            print(f"3. Ability (Level {self.companion_upgrades['ability']}/3) - Enhance special ability")
            print("4. Back")

            choice = input("\nChoose upgrade: ")

            try:
                if choice == "1":
                    if self.companion_upgrades['health'] >= 5:
                        print("Health upgrade already at maximum level!")
                        return
                    self.companion_tokens -= 1
                    self.companion_upgrades['health'] += 1
                    for companion in self.companions:
                        old_health = companion.max_health
                        companion.max_health = int(companion.max_health * 1.2)
                        companion.health = companion.max_health
                        print(f"{companion.name}'s HP increased from {old_health} to {companion.max_health}!")

                elif choice == "2":
                    if self.companion_upgrades['damage'] >= 5:
                        print("Damage upgrade already at maximum level!")
                        return
                    self.companion_tokens -= 1
                    self.companion_upgrades['damage'] += 1
                    for companion in self.companions:
                        old_damage = companion.damage
                        companion.damage = int(companion.damage * 1.2)
                        print(f"{companion.name}'s damage increased from {old_damage} to {companion.damage}!")

                elif choice == "3":
                    if self.companion_upgrades['ability'] >= 3:
                        print("Ability upgrade already at maximum level!")
                        return
                    self.companion_tokens -= 1
                    self.companion_upgrades['ability'] += 1
                    for companion in self.companions:
                        print(f"{companion.name}'s {companion.ability} ability enhanced!")

                elif choice == "4":
                    return

                else:
                    print("Invalid choice!")
                    return

                print(f"\nUpgrade successful! Remaining tokens: {self.companion_tokens}")

            except ValueError:
                print("Invalid input!")

# Add Companion class
class Companion:
    def __init__(self, name, companion_type):
        self.name = name
        self.type = companion_type
        self.level = 1
        self.exp = 0
        
        # Get companion tier based on type
        for tier, companions in COMPANION_TIERS.items():
            if companion_type in companions:
                stats = companions[companion_type]
                break
        else:
            raise ValueError(f"Invalid companion type: {companion_type}")
    
        
        stats = companions[companion_type]
        self.max_health = stats["health"]
        self.health = self.max_health
        self.damage = stats["damage"]
        self.ability = stats["ability"]
        self.ability_description = stats["description"]
        
    def scale_stats(self, player_level):
        """Scale companion stats based on player level"""
        scaling = 1 + ((self.level - 1) * 0.15)
        self.max_health = int(self.max_health * scaling)
        self.health = self.max_health
        self.damage = int(self.damage * scaling)

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
        self.max_health = health  # Add max_health attribute
        self.health = health
        self.level = level
        self.damage = damage
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.status_effects = []
        self.accuracy = 85  # Base 85% hit chance
        self.base_accuracy = 85  # Store base accuracy for modifications
        self.evasion = 5   # Base 5% chance to evade

    def scale_stats(self, player_level):
        """Scale enemy stats based on player level"""
        # Calculate level difference and scaling factor
        level_diff = max(0, player_level - self.level)
        scaling = 1 + (level_diff * 0.15)  # Reduced from 0.2 for smoother scaling
        
        # Scale base stats
        self.max_health = int(self.max_health * scaling)
        self.health = self.max_health
        self.damage = int(self.damage * scaling)
        self.exp_reward = int(self.exp_reward * scaling)
        self.gold_reward = int(self.gold_reward * scaling)
        
        # Scale accuracy and evasion based on player level
        if player_level > self.level:
            # Scale accuracy and evasion with diminishing returns
            self.accuracy = min(95, self.base_accuracy + (level_diff * 0.5))  # Cap at 95%
            self.evasion = min(15, self.evasion + (level_diff * 0.3))   # Cap at 15%

    def is_alive(self):
        """Check if enemy is still alive"""
        return self.health > 0
        
    def take_damage(self, amount):
        """Handle damage taken by enemy"""
        self.health = max(0, self.health - amount)
        return amount

class Boss:
    def __init__(self, name, health, damage, exp_reward, gold_reward, special_moves, level_req):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.special_moves = special_moves
        self.level_req = level_req
        self.status_effects = []
        self.accuracy = 90  # Higher base accuracy than regular enemies
        self.base_accuracy = 90
        self.phase = 1      # For multi-phase boss fights
        self.evasion = 5   # Base evasion chance

    def take_damage(self, amount):
        """Handle damage taken by boss"""
        self.health = max(0, self.health - amount)
        return amount

    def is_alive(self):
        """Check if boss is still alive"""
        return self.health > 0

    def scale_stats(self, player_level):
        """Scale boss stats based on player level"""
        level_diff = max(0, player_level - self.level_req)
        scaling = 1 + (level_diff * 0.12)  # Slightly reduced scaling for better balance
        
        self.max_health = int(self.max_health * scaling)
        self.health = self.max_health
        self.damage = int(self.damage * scaling)
        self.exp_reward = int(self.exp_reward * scaling)
        self.gold_reward = int(self.gold_reward * scaling)

def get_target(enemies, auto=False):
    """Improved target selection with better validation"""
    living_enemies = [e for e in enemies if e.health > 0]
    
    if not living_enemies:
        return None
        
    if auto or len(living_enemies) == 1:
        return living_enemies[0]
    
    while True:
        print("\nChoose your target:")
        for i, enemy in enumerate(living_enemies, 1):
            print(f"{i}. {enemy.name} - HP: {enemy.health}/{enemy.max_health}")
        
        try:
            choice = input("> ")
            if choice.lower() == 'back':
                return None
                
            index = int(choice) - 1
            if 0 <= index < len(living_enemies):
                return living_enemies[index]
            print("Invalid target number!")
        except ValueError:
            print("Please enter a valid number!")

# In the combat function, update the auto-target initialization
def combat(player, enemies):
    """Updated combat function with proper victory condition"""
    print("\nEnemies appear!")
    for enemy in enemies:
        print(f"- {enemy.name} (HP: {enemy.health})")
    
    auto_target = False
    
    # Main combat loop
    while any(enemy.health > 0 for enemy in enemies) and player.health > 0:
        # Check victory condition at start of each loop
        if not any(enemy.health > 0 for enemy in enemies):
            # Process victory rewards
            total_exp = sum(enemy.exp_reward for enemy in enemies)
            total_gold = sum(enemy.gold_reward for enemy in enemies)
            tech_points = calculate_tech_points_reward(player.level, isinstance(enemies[0], Boss))
            
            player.exp += total_exp
            player.gold += total_gold
            player.tech_points += tech_points
            
            print("\nVictory!")
            print(f"Gained {total_exp} experience!")
            print(f"Found {total_gold} gold!")
            print(f"Earned {tech_points} tech points!")
            return True

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
        
        # Process player turn based on choice
        if choice == "1":  # Basic attack
            living_enemies = [e for e in enemies if e.health > 0]
            if not living_enemies:
                print("No living enemies to target!")
                continue
            target = get_target(living_enemies, auto_target)
            if target:
                process_attack(player, target, enemies)
            else:
                print("Invalid target!")
                continue
                
        elif choice == "2":  # Use ability 
            abilities_list = show_abilities(player)
            if not abilities_list:
                print("No abilities available or not enough mana!")
                continue
                
            print("\nChoose ability number or 'back' to return")
            ability_choice = input("> ").lower()
            
            if ability_choice == 'back':
                continue
                
            try:
                ability_idx = int(ability_choice) - 1
                if 0 <= ability_idx < len(abilities_list):
                    ability_name, ability = abilities_list[ability_idx]
                    
                    # Get target first if ability requires one
                    target = None
                    if "damage" in ability or "area_damage" in ability:
                        target = get_target(enemies, auto_target)
                        if not target:
                            print("Invalid target!")
                            continue
                    
                    # Then process the ability
                    total_damage, healing = process_ability(player, target, enemies, ability_name)
                    
                    if total_damage > 0:
                        print(f"✨ {ability_name} dealt a total of {total_damage} damage!")
                    if healing > 0:
                        print(f"💚 {ability_name} restored {healing} HP!")
                else:
                    print("Invalid ability choice!")
            except ValueError:
                print("Invalid input!")
                continue

        elif choice == "3":  # Use item
            print("\nAvailable items:")
            if player.inventory.get("Health Potion", 0) > 0:
                heal_amount = calculate_potion_healing(player.level)
                print(f"1. Health Potion (Restores {heal_amount} HP)")
            if player.inventory.get("Mana Potion", 0) > 0:
                mana_amount = calculate_potion_mana(player.level)
                print(f"2. Mana Potion (Restores {mana_amount} MP)")
            if player.inventory.get("Mega Health Potion", 0) > 0 and isinstance(enemies[0], Boss):
                mega_heal = calculate_mega_potion_healing(player.level)
                print(f"3. Mega Health Potion (Restores {mega_heal} HP)")
            if player.inventory.get("Companion Revival Potion", 0) > 0:
                revival_percent = calculate_companion_revival(player.level)
                print(f"4. Companion Revival Potion (Revives companion with {int(revival_percent * 100)}% HP)")
                
                # Show dead companions
                dead_companions = [comp for comp in player.companions if comp.health <= 0]
                if dead_companions:
                    print("\nFallen Companions:")
                    for i, comp in enumerate(dead_companions, 1):
                        print(f"{i}. {comp.name} ({comp.type})")
            
            item_choice = input("Choose item to use (or 'back'): ")
            
            if item_choice == "1" and player.inventory.get("Health Potion", 0) > 0:
                heal_amount = calculate_potion_healing(player.level)
                player.health = min(player.max_health, player.health + heal_amount)
                player.inventory["Health Potion"] -= 1
                print(f"You drink a health potion and recover {heal_amount} HP!")
            elif item_choice == "2" and player.inventory.get("Mana Potion", 0) > 0:
                mana_amount = calculate_potion_mana(player.level)
                player.mana = min(player.max_mana, player.mana + mana_amount)
                player.inventory["Mana Potion"] -= 1
                print(f"You drink a mana potion and recover {mana_amount} MP!")
            elif item_choice == "3" and player.inventory.get("Mega Health Potion", 0) > 0:
                if isinstance(enemies[0], Boss):
                    mega_heal = calculate_mega_potion_healing(player.level)
                    player.health = min(player.max_health, player.health + mega_heal)
                    player.inventory["Mega Health Potion"] -= 1
                    print(f"💖 You drink a mega health potion and recover {mega_heal} HP!")
                else:
                    print("Mega Health Potions can only be used during boss battles!")
            elif item_choice == "4" and player.inventory.get("Companion Revival Potion", 0) > 0:
                dead_companions = [comp for comp in player.companions if comp.health <= 0]
                if dead_companions:
                    print("\nChoose companion to revive:")
                    for i, comp in enumerate(dead_companions, 1):
                        print(f"{i}. {comp.name} ({comp.type})")
                    
                    try:
                        comp_choice = int(input("\nChoice: ")) - 1
                        if 0 <= comp_choice < len(dead_companions):
                            companion = dead_companions[comp_choice]
                            revival_percent = calculate_companion_revival(player.level)
                            companion.health = int(companion.max_health * revival_percent)
                            player.inventory["Companion Revival Potion"] -= 1
                            print(f"✨ {companion.name} has been revived with {companion.health} HP!")
                        else:
                            print("Invalid choice!")
                    except ValueError:
                        print("Invalid input!")
                else:
                    print("No fallen companions to revive!")
            elif item_choice.lower() == "back":
                continue
            else:
                print("Invalid item or not enough potions!")
                continue

        elif choice == "4":  # Use Gadget
            if player.gadgets:
                gadget_list = show_gadgets(player)
                if gadget_list:
                    print("\nChoose gadget number or 'back' to return")
                    gadget_choice = input("> ").lower()
                    
                    if gadget_choice == 'back':
                        continue
                        
                    try:
                        gadget_idx = int(gadget_choice) - 1
                        if 0 <= gadget_idx < len(gadget_list):
                            gadget = gadget_list[gadget_idx]
                            target = get_target(enemies, auto_target)
                            if target:
                                process_gadget_effect(player, target, enemies, gadget.effect)
                    except ValueError:
                        print("Invalid input!")
                else:
                    print("No gadget charges remaining!")
            else:
                print("No gadgets available!")

        elif choice == "5":  # Run
            if random.random() < 0.5:
                print("You successfully fled from combat!")
                return "fled"
            else:
                print("You failed to run away!")
                continue
        
        # Companion turn
        # Companion turns - now all living companions will attack
        if player.companions:
            # Get all living enemies once for companions to target
            living_enemies = [e for e in enemies if e.health > 0]
            
            # Get all living companions
            living_companions = [c for c in player.companions if c.health > 0]
            
            # Have each living companion take their turn
            for companion in living_companions:
                if living_enemies:  # Only attack if there are still enemies alive
                    print(f"\n🐾 {companion.name}'s turn!")
            
                # Get random target from living enemies
                target = random.choice(living_enemies)
                damage = companion.damage
            
                # Find companion tier
                for tier, companions in COMPANION_TIERS.items():
                    if companion.type in companions:
                        companion_data = companions[companion.type]
                        ability = companion_data["ability"]
                        break
            
                # Handle abilities based on companion type
                if companion.type == "cat":  # Level 5
                    target.take_damage(damage)
                    print(f"😺 {companion.name}'s Attack: Agile Strike for {damage} damage!")
                elif companion.type == "owl":  # Level 5
                    enhanced_damage = int(damage * 1.25)  # 25% bonus damage
                    target.take_damage(enhanced_damage)
                    print(f"🦉 {companion.name}'s Attack: Reveals weakness for {enhanced_damage} damage!")
                elif companion.type == "bear":  # Level 8
                    target.take_damage(damage)
                    target.damage = int(target.damage * 0.85)  # Reduce enemy damage by 15%
                    print(f"🐻 {companion.name}'s Attack: Mighty Roar for {damage} damage and reduces enemy damage!")
                elif companion.type == "fox":  # Level 8
                    if random.random() < 0.35:  # 35% double strike chance
                        target.take_damage(damage * 2)
                        print(f"🦊 {companion.name}'s Attack: Strikes twice for {damage * 2} damage!")
                    else:
                        target.take_damage(damage)
                        print(f"🦊 {companion.name}'s Attack: Attacks for {damage} damage!")
                elif companion.type == "unicorn":  # Level 12
                    target.take_damage(damage)
                    heal = int(damage * 0.2)  # Heal 20% of damage
                    player.health = min(player.max_health, player.health + heal)
                    print(f"🦄 {companion.name}'s Attack: Holy Light for {damage} damage and heals you for {heal}!")
                elif companion.type == "griffin":  # Level 12
                # Attack multiple enemies for 60% damage
                    for enemy in living_enemies[:3]:  # Hit up to 3 enemies
                        splash = int(damage * 0.6)
                        enemy.take_damage(splash)
                        print(f"🦅 {companion.name}'s Attack: Hits {enemy.name} for {splash} damage with Sky Strike!")
                else:  # Default attack if type not found
                    # Check if there are any living enemies before attacking
                    living_enemies = [e for e in enemies if e.health > 0]
                    if living_enemies:
                        target = random.choice(living_enemies)
                        target.take_damage(damage)
                        print(f"🐾 {companion.name}'s Attack: Deals {damage} damage to {target.name}!")
                    else:
                        break  # No living enemies to attack
                
                # Update living enemies list after each companion's attacks
                living_enemies = [e for e in enemies if e.health > 0]
                if not living_enemies:
                    break  # Stop companion turns if all enemies are defeated

        # Enemy turns
        for enemy in enemies:
            if enemy.health > 0:
                # Calculate hit chance
                hit_roll = random.randint(1, 100)
                if hit_roll <= enemy.accuracy:
                    # Process damage with defense
                    raw_damage = enemy.damage
                    final_damage = process_enemy_attack(player, enemy)
                    player.health -= final_damage
                    print(f"🎯 {enemy.name} hits you for {final_damage} damage! (Reduced from {raw_damage})")
                else:
                    print(f"❌ {enemy.name}'s attack missed!")
        
        # Check player death
        if player.health <= 0:
            return handle_player_death(player)
            
        # Check again after player's action
        if not any(enemy.health > 0 for enemy in enemies):
            break  # Exit combat loop if all enemies are dead after player's turn

    # Combat victory rewards
    if player.health > 0:
        print("\nVictory!")
        total_exp = 0
        total_gold = 0
        tech_points = 0
        
        for enemy in enemies:
            total_exp += enemy.exp_reward
            total_gold += enemy.gold_reward
            
        # Add tech points reward (only if there were enemies)
        if enemies:
            tech_points = calculate_tech_points_reward(player.level, isinstance(enemies[0], Boss))
            
            # Add rewards
            player.exp += total_exp
            player.gold += total_gold
            player.tech_points += tech_points
            
            print(f"Gained {total_exp} experience!")
            print(f"Found {total_gold} gold!")
            print(f"Earned {tech_points} tech points!")
        return True
    
    if player.health <= 0:
        return handle_player_death(player)

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
    # Changed from 75 * (1 + (level * 0.4)) to a better curve
    return int(100 * (1 + (level * 0.35)) * (1 + (level * 0.1)))

def calculate_level_rewards(level):
    """More balanced level-up rewards"""
    return {
        "health": 10 + int(level * 1.5),  # Reduced from 12 + (level * 2)
        "mana": 5 + int(level * 1.2),     # Reduced from 6 + (level * 1.5)
        "damage_bonus": int(level * 0.6),  # Reduced from 0.8
        "defense_bonus": int(level * 0.5)  # Reduced from 0.7
    }

def calculate_potion_healing(player_level):
    """Calculate healing amount based on player level"""
    base_heal = 40
    level_bonus = int(player_level * 5)  # 5 HP per level
    return base_heal + level_bonus

def calculate_potion_mana(player_level):
    """Calculate mana restoration based on player level"""
    base_mana = 35
    level_bonus = int(player_level * 3)  # 3 MP per level
    return base_mana + level_bonus

def calculate_mega_potion_healing(player_level):
    """Calculate mega potion healing based on player level"""
    base_heal = 100
    level_bonus = int(player_level * 10)  # 10 HP per level
    return base_heal + level_bonus

# Add to potion calculations
def calculate_companion_revival(player_level):
    """Calculate companion revival effectiveness based on player level"""
    base_heal_percent = 0.5  # Base 50% health restoration
    level_bonus = min(0.3, player_level * 0.02)  # Up to 30% bonus based on level
    return base_heal_percent + level_bonus

# Update shop function's item handling
def shop(player):
    """Improved shop with level-based filtering and numbered items"""
    items = {
        # Basic items (adjusted prices)
        "Health Potion": {
            "cost": 20, 
            "effect": f"Restore {calculate_potion_healing(player.level)} HP", 
            "min_level": 1
        },
        "Mana Potion": {
            "cost": 20, 
            "effect": f"Restore {calculate_potion_mana(player.level)} MP", 
            "min_level": 1
        },
        
        # Add Mega Healing Potion
        "Mega Health Potion": {
            "cost": 100, 
            "effect": f"Restore {calculate_mega_potion_healing(player.level)} HP", 
            "min_level": 5,  # Only available at level 5+
            "description": "Powerful healing potion for boss battles",
            "boss_only": True  # Mark as boss-only item
        },
        
        # Add Companion Revival Potion
        "Companion Revival Potion": {
            "cost": 150,
            "effect": f"Revive fallen companion with {int(calculate_companion_revival(player.level) * 100)}% HP",
            "min_level": 5,
            "description": "Resurrect fallen companions"
        },
        
        # Tier 1 weapons (adjusted damage)
        "Iron Sword": {"cost": 50, "damage": 12, "type": "melee", "min_level": 1},
        "Wooden Bow": {"cost": 50, "damage": 10, "type": "ranged", "min_level": 1},
        
        # Tier 2 weapons
        "Steel Sword": {"cost": 150, "damage": 20, "type": "melee", "min_level": 3},
        "Longbow": {"cost": 150, "damage": 18, "type": "ranged", "min_level": 3},
        
        # Armor (adjusted defense)
        "Leather Armor": {"cost": 60, "defense": 8, "min_level": 1},
        "Chain Mail": {"cost": 140, "defense": 15, "min_level": 3},
        "Plate Armor": {"cost": 300, "defense": 25, "min_level": 5},

        # Multi-hit weapons
        "Twin Daggers": {
            "cost": 200, 
            "damage": 15, 
            "hits": 2, 
            "type": "melee", 
            "min_level": 2,
            "description": "Strike twice per attack"
        },
        "Triple Shot Bow": {
            "cost": 300, 
            "damage": 12, 
            "hits": 3, 
            "type": "ranged", 
            "min_level": 3,
            "description": "Fire three arrows"
        },

        # Area damage weapons
        "Flame Sword": {
            "cost": 400, 
            "damage": 25, 
            "area_damage": 12, 
            "type": "melee", 
            "min_level": 4,
            "description": "Deals splash damage"
        },
        "Bomb Launcher": {
            "cost": 500, 
            "damage": 20, 
            "area_damage": 15, 
            "type": "ranged", 
            "min_level": 4,
            "description": "Explosive area damage"
        },

        # High-tier weapons
        "Whirlwind Blade": {
            "cost": 800,
            "damage": 30,
            "hits": 3,
            "area_damage": 15,
            "type": "melee",
            "min_level": 6,
            "description": "Multiple hits with area damage"
        },
        "Storm Bow": {
            "cost": 1000,
            "damage": 25,
            "hits": 4,
            "area_damage": 12,
            "type": "ranged",
            "min_level": 7,
            "description": "Rain of explosive arrows"
        }
    }
    
    while True:
        print("\n=== Shop ===")
        print(f"Gold: {player.gold}")
        print(f"Level: {player.level}")
        
        # Filter and categorize items by type
        available_items = {
            "Potions": [],
            "Weapons": [],
            "Armor": []
        }
        
        # Sort and filter items based on player level
        for item_name, details in items.items():
            if details.get('min_level', 1) <= player.level:
                if 'Potion' in item_name:
                    available_items["Potions"].append((item_name, details))
                elif 'damage' in details:
                    available_items["Weapons"].append((item_name, details))
                elif 'defense' in details:
                    available_items["Armor"].append((item_name, details))
        
        # Display items by category with numbers
        item_number = 1
        numbered_items = {}  # Store item numbers for purchase reference
        
        for category, items_list in available_items.items():
            if items_list:
                print(f"\n{category}:")
                for item_name, details in sorted(items_list, key=lambda x: x[1]['cost']):
                    cost = details['cost']
                    desc = []
                    
                    if 'damage' in details:
                        desc.append(f"DMG: {details['damage']}")
                    if 'defense' in details:
                        desc.append(f"DEF: {details['defense']}")
                    if 'hits' in details:
                        desc.append(f"Hits: {details['hits']}x")
                    if 'area_damage' in details:
                        desc.append(f"Area DMG: {details['area_damage']}")
                    if 'effect' in details:
                        desc.append(details['effect'])
                    if 'description' in details:
                        desc.append(details['description'])
                    
                    # Color code based on affordability
                    if player.gold >= cost:
                        status = "✓"  # Can afford
                    else:
                        status = "✗"  # Cannot afford
                        
                    print(f"{item_number}. {status} {item_name}")
                    print(f"   Cost: {cost} gold | {' | '.join(desc)}")
                    
                    numbered_items[item_number] = item_name
                    item_number += 1
        
        print("\nEnter item number to buy (or 'exit' to leave):")
        choice = input("> ").lower()
        
        if choice == "exit":
            break
            
        try:
            item_number = int(choice)
            if item_number in numbered_items:
                item_name = numbered_items[item_number]
                item_details = items[item_name]
                
                if player.gold >= item_details['cost']:
                    # Store old gold for verification
                    old_gold = player.gold
                    player.gold -= item_details['cost']
                    
                    # Process purchase based on item type
                    if 'damage' in item_details:
                        player.weapons[item_name] = item_details
                        print(f"\nBought {item_name}!")
                        print(f"Damage: {item_details['damage']}")
                        if 'hits' in item_details:
                            print(f"Hits: {item_details['hits']}x")
                        if 'area_damage' in item_details:
                            print(f"Area Damage: {item_details['area_damage']}")
                    elif 'defense' in item_details:
                        player.armor[item_name] = item_details['defense']
                        print(f"\nBought {item_name}!")
                        print(f"Defense: {item_details['defense']}")
                    else:
                        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
                        print(f"\nBought {item_name}!")
                    
                    print(f"Remaining gold: {player.gold}")
                else:
                    print("\nNot enough gold!")
            else:
                print("\nInvalid item number!")
        except ValueError:
            print("\nInvalid input!")
            
        input("\nPress Enter to continue...")
        
        print("5. Companion Services")
        
        if choice == "5" and player.companions:
            print("\n=== Companion Services ===")
            for companion in player.companions:
                print(f"1. Heal {companion.name} (30 gold) - Current HP: {companion.health}/{companion.max_health}")
            print("2. Back")
            
            service = input("> ")
            if service == "1":
                if player.gold >= 30:
                    player.gold -= 30
                    companion.health = companion.max_health
                    print(f"{companion.name} has been fully healed!")
                else:
                    print("Not enough gold!")

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
    """Show available abilities with proper validation"""
    abilities_list = []
    
    print("\n=== Available Abilities ===")
    print(f"Mana: {player.mana}/{player.max_mana}")
    
    # Basic abilities first
    basic_abilities = {k:v for k,v in player.abilities.items() 
                      if k in ["Basic Attack", "Power Strike", "Quick Shot", "Minor Heal", "Focus"]
                      and v['mana_cost'] <= player.mana}
    
    if basic_abilities:
        print("\n🗡️ Basic Abilities:")
        for name, ability in basic_abilities.items():
            abilities_list.append((name, ability))
            index = len(abilities_list)
            stats = []
            if 'damage' in ability:
                stats.append(f"💥 DMG: {ability['damage']}")
            if 'heal' in ability:
                stats.append(f"💚 Heal: {ability['heal']}")
            if 'mana' in ability:
                stats.append(f"✨ MP: {ability['mana']}")
            stats.append(f"Cost: {ability['mana_cost']} MP")
            
            print(f"\n{index}. {name}")
            print(f"   {' | '.join(stats)}")
            print(f"   📜 {ability['description']}")
    
    # Class abilities second
    class_abilities = {k:v for k,v in player.abilities.items() 
                      if k not in basic_abilities
                      and v['mana_cost'] <= player.mana}
    
    if class_abilities:
        print("\n✨ Class Abilities:")
        for name, ability in class_abilities.items():
            abilities_list.append((name, ability))
            index = len(abilities_list)
            stats = []
            if 'damage' in ability:
                stats.append(f"💥 DMG: {ability['damage']}")
            if 'heal' in ability:
                stats.append(f"💚 Heal: {ability['heal']}")
            if 'area_damage' in ability:
                stats.append(f"⚡ Area: {ability['area_damage']}")
            stats.append(f"Cost: {ability['mana_cost']} MP")
            
            print(f"\n{index}. {name}")
            print(f"   {' | '.join(stats)}")
            print(f"   📜 {ability['description']}")
    
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
    """Process attack with improved target validation and victory check"""
    if not enemies:
        print("No enemies to attack!")
        return 0
        
    weapon_stats = player.weapons[player.current_weapon]
    total_damage = 0
    living_enemies = [e for e in enemies if e.health > 0]
    
    if not living_enemies:
        print("Victory! All enemies have been defeated!")
        return total_damage
        
    # If no target is provided or target is invalid, select first living enemy
    if target is None or target not in living_enemies:
        target = living_enemies[0]

    # Validate target exists in living enemies
    if target not in living_enemies:
        if living_enemies:
            target = living_enemies[0]
        else:
            print("Victory! All enemies have been defeated!")
            return total_damage

    # Get target index from living enemies
    enemy_index = living_enemies.index(target)

    if isinstance(weapon_stats, dict):
        base_damage = weapon_stats["damage"]
        level_bonus = int(player.level * 1.5)
        
        # Handle multi-hit attacks
        hits = weapon_stats.get("hits", 1)
        for hit in range(hits):
            # Update living enemies list
            living_enemies = [e for e in enemies if e.health > 0]
            if not living_enemies:
                print("Victory! All enemies have been defeated!")
                break
                
            # Get current target
            current_target = living_enemies[enemy_index % len(living_enemies)]
            
            # Calculate and apply damage
            variation = random.randint(-2, 2)
            hit_damage = max(1, base_damage + level_bonus + variation)
            current_target.health -= hit_damage
            total_damage += hit_damage
            
            print(f"Hit {hit + 1}: {hit_damage} damage to {current_target.name}!")
            
            # Handle target death
            if current_target.health <= 0:
                print(f"{current_target.name} has been defeated!")
                # Update living enemies and index
                living_enemies = [e for e in enemies if e.health > 0]
                if living_enemies:
                    enemy_index = min(enemy_index, len(living_enemies) - 1)
                else:
                    print("Victory! All enemies have been defeated!")
                    
                    total_exp = 0
                    total_gold = 0
                    tech_points = 0
                        
                    for enemy in enemies:
                        total_exp += enemy.exp_reward
                        total_gold += enemy.gold_reward
                            
                    # Add tech points reward (only if there were enemies)
                    if enemies:
                        tech_points = calculate_tech_points_reward(player.level, isinstance(enemies[0], Boss))
                            
                        # Add rewards
                        player.exp += total_exp
                        player.gold += total_gold
                        player.tech_points += tech_points
                            
                        print(f"Gained {total_exp} experience!")
                        print(f"Found {total_gold} gold!")
                        print(f"Earned {tech_points} tech points!")
                        
                    break  # No more enemies to attack
                
            else:
                enemy_index = (enemy_index + 1) % len(living_enemies)
        
        # Process area damage after hits
        if "area_damage" in weapon_stats:
            living_enemies = [e for e in enemies if e.health > 0]
            if living_enemies:
                splash_damage = max(1, weapon_stats["area_damage"] + int(level_bonus * 0.5))
                for other in living_enemies:
                    if other != target and other.health > 0:
                        other.health -= splash_damage
                        total_damage += splash_damage
                        print(f"{other.name} takes {splash_damage} splash damage!")
                        if other.health <= 0:
                            print(f"{other.name} has been defeated!")
                
                # Check if all enemies are defeated after splash damage
                if not any(e.health > 0 for e in enemies):
                    print("Victory! All enemies have been defeated!")
        
        print(f"Total damage dealt: {total_damage}")
                    
    else:  # Legacy weapon handling
        variation = random.randint(-2, 2)
        main_damage = max(1, weapon_stats + int(player.level * 1.5) + variation)
        target.health -= main_damage
        total_damage = main_damage
        print(f"You deal {main_damage} damage to {target.name}!")
        
        if target.health <= 0:
            print(f"{target.name} has been defeated!")
            if not any(e.health > 0 for e in enemies):
                print("Victory! All enemies have been defeated!")
    
    return total_damage

def process_enemy_attack(player, enemy):
    """Process enemy attack with proper defense calculation"""
    # Calculate base damage
    base_damage = enemy.damage
    
    # Calculate base defense from armor and bonus defense
    base_defense = player.armor.get(player.current_armor, 0)
    total_defense = base_defense + player.bonus_defense

    defense_multiplier = 0.05  # Each point of defense reduces damage by 5%
    damage_reduction = total_defense * defense_multiplier
    
    # Cap damage reduction at 75%
    damage_reduction = min(0.75, damage_reduction)
    
    # Calculate final damage
    reduced_damage = max(1, int(base_damage * (1 - damage_reduction)))
    
    # Show defense feedback
    damage_blocked = base_damage - reduced_damage
    print(f"🛡️ Your defense blocked {damage_blocked} damage!")
    
    return reduced_damage


def process_ability(player, target, enemies, ability_name):
    """Process abilities with proper validation"""
    if ability_name not in player.abilities:
        print("Invalid ability!")
        return 0, 0
        
    ability = player.abilities[ability_name]
    
    # Validate mana cost
    if player.mana < ability['mana_cost']:
        print("Not enough mana!")
        return 0, 0
        
    # Deduct mana
    player.mana -= ability['mana_cost']
    
    total_damage = 0
    total_healing = 0
    
    # Process healing if present
    if "heal" in ability:
        heal_amount = ability["heal"]
        old_health = player.health
        player.health = min(player.max_health, player.health + heal_amount)
        total_healing = player.health - old_health
        print(f"💚 Healed for {total_healing} HP!")
    
    # Process damage if present
    if "damage" in ability and target and target.health > 0:
        damage = ability["damage"]
        target.health -= damage
        total_damage += damage
        print(f"💥 Dealt {damage} damage to {target.name}!")
        
        # Handle area damage
        if "area_damage" in ability:
            area_damage = ability["area_damage"]
            for enemy in enemies:
                if enemy != target and enemy.health > 0:
                    enemy.health -= area_damage
                    total_damage += area_damage
                    print(f"⚡ Area damage: {area_damage} to {enemy.name}!")
    
    return total_damage, total_healing

def apply_status_effect(target, effect_type, base_damage, duration):
    """Enhanced status effect system with accuracy modifications"""
    effects = {
        "burn": {
            "name": "Burned",
            "damage": max(1, base_damage // 3),
            "duration": duration,
            "message": "🔥 {} is burning!"
        },
        "freeze": {
            "name": "Frozen",
            "damage": max(1, base_damage // 4),
            "duration": duration,
            "damage_reduction": 0.5,
            "message": "❄️ {} is frozen!"
        },
        "stun": {
            "name": "Stunned",
            "duration": duration,
            "skip_turn": True,
            "message": "⚡ {} is stunned!"
        },
        "poison": {
            "name": "Poisoned",
            "damage": max(1, base_damage // 3),
            "duration": duration,
            "message": "☠️ {} is poisoned!"
        },
        "bleed": {
            "name": "Bleeding",
            "damage": max(1, base_damage // 2),
            "duration": duration,
            "message": "💉 {} is bleeding!"
        },
        "root": {
            "name": "Rooted",
            "duration": duration,
            "movement_locked": True,
            "message": "🌱 {} is rooted!"
        },
        "holy": {
            "name": "Holy",
            "damage": max(1, base_damage // 3),
            "heal_reduction": 0.5,
            "duration": duration,
            "message": "✨ {} is marked by holy light!"
        },
        "curse": {
            "name": "Cursed",
            "damage": max(1, base_damage // 4),
            "damage_taken_increase": 1.3,
            "duration": duration,
            "message": "👻 {} is cursed!"
        },
        "acid": {
            "name": "Corroded",
            "damage": max(1, base_damage // 3),
            "defense_reduction": 5,
            "duration": duration,
            "message": "⚗️ {} is corroded!"
        },
        "blind": {
            "name": "Blinded",
            "accuracy_reduction": 30,  # Reduce accuracy by 30%
            "duration": duration,
            "message": "🌑 {} is blinded and has reduced accuracy!"
        },
        "daze": {
            "name": "Dazed",
            "accuracy_reduction": 15,  # Reduce accuracy by 15%
            "duration": duration,
            "message": "💫 {} is dazed and has reduced accuracy!"
        },
        "rage": {
            "name": "Enraged",
            "damage_boost": 1.3,
            "defense_reduction": 0.7,
            "duration": duration,
            "message": "💢 {} is enraged!"
        },
        "enlightened": {
            "name": "Enlightened",
            "damage_boost": 1.2,
            "healing_boost": 1.2,
            "duration": duration,
            "message": "🔆 {} is enlightened!"
        },
        "spirit": {
            "name": "Spirit Marked",
            "damage_taken_increase": 1.2,
            "duration": duration,
            "message": "👻 {} is spirit marked!"
        },
        "regenerate": {
            "name": "Regenerating",
            "heal": max(1, base_damage // 4),
            "duration": duration,
            "message": "💚 {} is regenerating!"
        },
        "pierce": {
            "name": "Armor Pierced",
            "defense_ignored": True,
            "duration": duration,
            "message": "🎯 {} armor is pierced!"
        },
        "lifesteal": {
            "name": "Life Drained",
            "damage": max(1, base_damage // 3),
            "heal_percent": 0.5,
            "duration": duration,
            "message": "💀 {} life force is being drained!"
        },
        "focus": {
            "name": "Focused",
            "damage_boost": 1.5,
            "accuracy_boost": 20,  # Increase accuracy by 20%
            "critical_chance": 0.25,  # 25% increased crit chance
            "duration": duration,
            "message": "🎯 {} is focused and gains increased damage and accuracy!"
        }
    }

    # Handle multiple effects
    if isinstance(effect_type, list):
        for effect in effect_type:
            if effect in effects:
                status = effects[effect].copy()
                target.status_effects.append(status)
                print(status["message"].format(target.name))
    # Handle single effect
    elif effect_type in effects:
        status = effects[effect_type].copy()
        target.status_effects.append(status)
        print(status["message"].format(target.name))

def process_status_effects(entity):
    """Process status effects including accuracy modifications"""
    is_stunned = False
    damage_multiplier = 1.0
    accuracy_modifier = 0  # Track accuracy modifications
    
    """Process status effects including defense"""
    # Process defense effects
    if hasattr(entity, 'defense_effects'):
        for effect in entity.defense_effects[:]:
            effect['duration'] -= 1
            if effect['duration'] <= 0:
                entity.bonus_defense -= effect['amount']
                entity.defense_effects.remove(effect)
                print(f"🛡️ {effect['name']}'s defense bonus has worn off!")
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
        elif "accuracy_reduction" in effect:
            accuracy_modifier -= effect["accuracy_reduction"]
            
        effect["duration"] -= 1
        if effect["duration"] <= 0:
            entity.status_effects.remove(effect)
            print(f"{effect['name']} effect has worn off!")
    
    # Apply accuracy modifications if entity is an enemy
    if isinstance(entity, Enemy):
        entity.accuracy = max(5, min(95, entity.base_accuracy + accuracy_modifier))
    
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
        # Reduced scaling from 0.2 to 0.15 for smoother progression
        scaling = 1 + (level_diff * 0.15)
        
        # Add randomization for variety
        health_var = random.uniform(0.9, 1.1)
        damage_var = random.uniform(0.9, 1.1)
        
        return Enemy(
            self.name,
            int(self.base_health * scaling * health_var),
            int(self.base_damage * scaling * damage_var),
            int(self.base_exp * scaling),
            int(self.base_gold * scaling),
            min(player_level, self.min_level + 2)
        )

# Add at the top of the file with other constants
spawn_table = [
    # Level 1 enemies
    (EnemyType("Goblin", 45, 8, 20, 25, 1), 20, 1),      
    (EnemyType("Wolf", 50, 10, 25, 30, 1), 20, 1),        
    (EnemyType("Slime", 40, 6, 15, 20, 1), 15, 1),       
    
    # Level 3 enemies
    (EnemyType("Bandit", 65, 12, 35, 45, 3), 15, 3),      
    (EnemyType("Skeleton", 60, 13, 30, 40, 3), 15, 3),     
    
    # Level 5 enemies
    (EnemyType("Orc", 80, 15, 45, 55, 5), 10, 5),
    (EnemyType("Dark Elf", 70, 18, 50, 60, 5), 10, 5),
    
    # Level 7 enemies
    (EnemyType("Troll", 100, 20, 65, 75, 7), 8, 7),
    (EnemyType("Wraith", 85, 22, 70, 80, 7), 8, 7),
    
    # Level 10 enemies
    (EnemyType("Giant", 130, 25, 90, 100, 10), 5, 10),
    (EnemyType("Dragon Whelp", 110, 28, 95, 105, 10), 5, 10)
]

def spawn_enemies(player, num_enemies):
    """Spawn enemies with proper validation and scaling"""
    enemies = []
    
    # Filter eligible enemy types based on player level
    eligible_enemies = []
    for enemy_type, chance, min_level in spawn_table:
        if player.level >= min_level:
            eligible_enemies.append((enemy_type, chance))
    
    if not eligible_enemies:
        # Fallback to basic enemies if nothing else is available
        basic_enemy = EnemyType("Goblin", 45, 8, 20, 25, 1)
        enemies.append(basic_enemy.scale_to_level(player.level))
        return enemies
    
    # Spawn requested number of enemies
    for _ in range(num_enemies):
        # Calculate total chance for normalization
        total_chance = sum(chance for _, chance in eligible_enemies)
        if total_chance <= 0:
            break
            
        # Roll for enemy type
        roll = random.uniform(0, total_chance)
        cumulative = 0
        enemy_spawned = False
        
        for enemy_type, chance in eligible_enemies:
            cumulative += chance
            if roll <= cumulative:
                # Create and scale enemy
                enemy = enemy_type.scale_to_level(player.level)
                enemies.append(enemy)
                enemy_spawned = True
                break
        
        # Fallback if no enemy was spawned
        if not enemy_spawned and eligible_enemies:
            enemy_type, _ = eligible_enemies[0]
            enemy = enemy_type.scale_to_level(player.level)
            enemies.append(enemy)
    
    return enemies

def currency_exchange(player):
    """More balanced exchange rates"""
    GOLD_TO_TP_RATE = 120  # Increased from 100
    TP_TO_GOLD_RATE = 80   # Decreased from 100
    
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

# Add boss definitions
BOSSES = {
    "Dragon Warlord": Boss(
        name="Dragon Warlord",
        health=300,
        damage=25,
        exp_reward=200,
        gold_reward=300,
        special_moves={
            "Flame Breath": {"damage": 40, "area_damage": 20, "effect": "burn"},
            "Wing Slash": {"damage": 30, "hits": 2},
            "Ground Slam": {"damage": 35, "effect": "stun"}
        },
        level_req=5
    ),
    "Shadow Queen": Boss(
        name="Shadow Queen",
        health=400,
        damage=30,
        exp_reward=300,
        gold_reward=400,
        special_moves={
            "Dark Nova": {"damage": 45, "area_damage": 25, "effect": "blind"},
            "Soul Drain": {"damage": 35, "heal": 35},
            "Shadow Storm": {"damage": 25, "hits": 4}
        },
        level_req=10
    ),
    "Ancient Golem": Boss(
        name="Ancient Golem",
        health=500,
        damage=35,
        exp_reward=400,
        gold_reward=500,
        special_moves={
            "Earthquake": {"damage": 50, "area_damage": 30, "effect": "stun"},
            "Rock Barrage": {"damage": 30, "hits": 3},
            "Stone Armor": {"defense": 50, "duration": 3}
        },
        level_req=15
    )
}

def boss_battle(player, boss):
    """Handle boss battle with phases and special moves"""
    print(f"\n{'='*60}")
    print(f"BOSS BATTLE: {boss.name}")
    print(f"{'='*60}")
    
    while boss.health > 0 and player.health > 0:
        # Display boss status with HP bar
        hp_percent = boss.health / boss.max_health
        hp_bar = "█" * int(hp_percent * 20)
        hp_bar += "░" * (20 - len(hp_bar))
        print(f"\n{boss.name} HP: [{hp_bar}] {boss.health}/{boss.max_health}")
        
        # Player turn
        result = combat(player, [boss])
        if result == "fled":
            return "fled"
            
        # Boss phase changes
        if boss.health <= boss.max_health * 0.5 and boss.phase == 1:
            boss.phase = 2
            print(f"\n⚠️ {boss.name} enters phase 2!")
            boss.damage = int(boss.damage * 1.2)
            
        # Boss turn
        if boss.health > 0:
            # Choose special move or normal attack
            if random.random() < 0.3:  # 30% chance for special move
                move_name = random.choice(list(boss.special_moves.keys()))
                move = boss.special_moves[move_name]
                print(f"\n🔥 {boss.name} uses {move_name}!")
                
                if "damage" in move:
                    damage = move["damage"]
                    if boss.phase == 2:
                        damage = int(damage * 1.2)
                    player.health -= damage
                    print(f"You take {damage} damage!")
                    
                    if "area_damage" in move and player.companions:
                        for companion in player.companions:
                            companion.health -= move["area_damage"]
                            print(f"{companion.name} takes {move['area_damage']} splash damage!")
                        
                if "effect" in move:
                    apply_status_effect(player, move["effect"], damage, 2)
                    
                if "heal" in move:
                    heal = move["heal"]
                    boss.health = min(boss.max_health, boss.health + heal)
                    print(f"{boss.name} heals for {heal} HP!")
            else:
                # Normal attack
                damage = boss.damage
                hit_roll = random.randint(1, 100)
                if hit_roll <= boss.accuracy:
                    player.health -= damage
                    print(f"\n{boss.name} hits you for {damage} damage!")
                else:
                    print(f"\n{boss.name}'s attack missed!")
                    
    # Battle results
    if player.health <= 0:
        return handle_player_death(player)
    else:
        print(f"\n🏆 You have defeated {boss.name}!")
        
        # Add substantial tech points reward for boss victory
        tech_points = calculate_tech_points_reward(player.level, True)
        player.tech_points += tech_points
        
        print(f"Gained {boss.exp_reward} experience!")
        print(f"Found {boss.gold_reward} gold!")
        print(f"Earned {tech_points} tech points!")
        print(f"🎫 Earned a Companion Token! (Total: {player.companion_tokens})")
        return True

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
    
    # Add immediate companion check for new characters at level 5+
    if player.level >= 5 and not player.companions:
        print("\nSince you're level 5 or higher, you can choose a companion!")
        player.unlock_companion()
    
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
        print("2. Challenge Boss (Level 5+ required)")  # Add this line
        print("3. Visit shop")
        print("4. Check inventory")
        print("5. Rest (Heal 50% HP/MP for 15 gold)")
        print("6. Show abilities")
        print("7. Visit gadget shop") 
        print("8. Currency Exchange")
        print("9. Visit power shop")
        print("10. Manage Companion")  # Add this option
        print("11. Save game")
        print("12. Load game")
        print("13. Quit")
        
        choice = input("> ")
        # Update the combat section in main()
        if choice == "1":
            # Determine number of enemies based on player level
            num_enemies = 1
            if player.level >= 5:
                num_enemies = random.randint(2, 3)
            
            try:
                # Spawn enemies with validation
                enemies = spawn_enemies(player, num_enemies)
                
                if enemies:
                    print(f"\nEncountered {len(enemies)} enemies!")
                    for enemy in enemies:
                        print(f"- {enemy.name} (Level {enemy.level})")
                    
                    result = combat(player, enemies)
                    if result == False:  # Player died and chose not to continue
                        print(f"\nGame Over! Final Level: {player.level}")
                        print(f"Gold collected: {player.gold}")
                        break
                else:
                    print("\nArea seems quiet. Try exploring somewhere else.")
                    continue
                    
            except Exception as e:
                continue

        elif choice == "2":
            if player.level < 5:
                print("You must be at least level 5 to challenge bosses!")
                continue
                
            print("\nAvailable Bosses:")
            available_bosses = []
            for name, boss in BOSSES.items():
                if player.level >= boss.level_req:
                    available_bosses.append((name, boss))
                    print(f"{len(available_bosses)}. {name} (Level {boss.level_req}+ required)")
            
            if not available_bosses:
                print("No bosses available at your level!")
                continue
                
            try:
                boss_choice = int(input("\nChoose boss to fight (0 to cancel): "))
                if 0 < boss_choice <= len(available_bosses):
                    boss_name, boss = available_bosses[boss_choice - 1]
                    boss.scale_stats(player.level)
                    result = boss_battle(player, boss)
                    if result == False:  # Player died
                        print(f"\nGame Over! Final Level: {player.level}")
                        break
            except ValueError:
                print("Invalid input!")

        elif choice == "3":
            shop(player)
           
        elif choice == "4":
            show_inventory_menu(player)
            # Add companion management option if companion exists
            if player.companions:
                print("\nCompanion Status:")
                for companion in player.companions:
                    print(f"Name: {companion.name}")
                    print(f"Type: {companion.type}")
                    print(f"Health: {companion.health}/{companion.max_health}")
                    print(f"Damage: {companion.damage}")
                    print(f"Ability: {companion.ability}")
                print(f"\nCompanion Tokens: {player.companion_tokens}")
                
                if player.companion_tokens > 0:
                    upgrade = input("\nWould you like to upgrade your companion? (y/n): ")
                    if upgrade.lower() == 'y':
                        player.upgrade_companion()
            
        elif choice == "5":
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
                        
        elif choice == "6":
            show_abilities(player)
            
        elif choice == "7":
            gadget_shop(player)
            
        elif choice == "8":
            currency_exchange(player)
            
        elif choice == "9":
            power_shop(player)
            
        elif choice == "10":  # Companion Management
            print("\n=== Companion Management ===")
            print("1. View Companions")
            print("2. Upgrade Companions")
            print("3. Available Quests")
            print("4. Back")
            player.unlock_companion()
            
            manage_choice = input("> ")
            
            if manage_choice == "1":
                if player.companions:
                    for companion in player.companions:
                        print(f"\n=== {companion.name} Status ===")
                        print(f"Type: {companion.type}")
                        print(f"Health: {companion.health}/{companion.max_health}")
                        print(f"Damage: {companion.damage}")
                        print(f"Ability: {companion.ability}")
                        print(f"Description: {companion.ability_description}")
                elif player.level >= 5:
                    print("\nYou are eligible for a companion!")
                    player.unlock_companion()
                else:
                    print("\nReach level 5 to unlock companions!")
                    
            elif manage_choice == "2":
                if player.companion_tokens > 0:
                    player.upgrade_companion()
                else:
                    print("No upgrade tokens available!")
                    
            elif manage_choice == "3":
                player.start_quest_menu()

        elif choice == "11":  # Save
            save_game(player)
            
        elif choice == "12":  # Load
            loaded_player = load_game()
            if loaded_player:
                player = loaded_player
                # Check for companion eligibility after loading
                if player.level >= 5 and not player.companions:
                    print("\nYou can choose a companion!")
                    player.unlock_companion()
            
        elif choice == "13":  # Quit
            confirm = input("Are you sure you want to quit? (y/n): ").lower()
            if confirm == 'y':
                print("Thanks for playing!")
                break

def handle_player_death(player):
    """Handle player death with retry options"""
    print("\n" + "="*50)
    print("💀 You have been defeated! 💀")
    print(f"Level reached: {player.level}")
    print(f"Gold collected: {player.gold}")
    print("="*50)
    
    while True:
        print("\nOptions:")
        print("1. Rest and try again (Cost: 100 gold)")
        print("2. Give up and start new game")
        
        choice = input("> ")
        
        if choice == "1":
            if player.gold >= 100:
                player.gold -= 100
                player.health = player.max_health
                player.mana = player.max_mana
                print("\nYou have been revived!")
                print(f"Remaining gold: {player.gold}")
                return True
            else:
                print("Not enough gold to rest!")
                return False
        elif choice == "2":
            return False
        else:
            print("Invalid choice!")

# Add save/load functions
def save_game(player):
    """Save game progress to a file"""
    save_dir = "saves"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    # Convert player object to dictionary
    player_data = {
        "name": player.name,
        "class_type": player.class_type,
        "health": player.health,
        "max_health": player.max_health,
        "mana": player.mana,
        "max_mana": player.max_mana,
        "level": player.level,
        "exp": player.exp,
        "gold": player.gold,
        "inventory": player.inventory,
        "weapons": player.weapons,
        "current_weapon": player.current_weapon,
        "armor": player.armor,
        "current_armor": player.current_armor,
        "tech_points": player.tech_points,
        "gadgets": {name: {"charges": g.charges} for name, g in player.gadgets.items()},
        "powers": list(player.powers.keys()),
        "abilities": player.abilities,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    filename = f"saves/{player.name}_{player.level}.json"
    with open(filename, 'w') as f:
        json.dump(player_data, f, indent=2)
    print(f"\nGame saved as: {filename}")

def load_game():
    """Load a saved game file"""
    save_dir = "saves"
    if not os.path.exists(save_dir):
        print("No saved games found!")
        return None
        
    saves = [f for f in os.listdir(save_dir) if f.endswith('.json')]
    if not saves:
        print("No saved games found!")
        return None
        
    print("\nAvailable saves:")
    for i, save in enumerate(saves, 1):
        with open(os.path.join(save_dir, save)) as f:
            data = json.load(f)
            print(f"{i}. {data['name']} (Level {data['level']}) - {data['timestamp']}")
            
    try:
        choice = int(input("\nChoose save to load (0 to cancel): "))
        if choice == 0:
            return None
        if 1 <= choice <= len(saves):
            with open(os.path.join(save_dir, saves[choice-1])) as f:
                data = json.load(f)
                
            # Create new character from save data
            player = Character(data['name'], data['class_type'])
            player.health = data['health']
            player.max_health = data['max_health']
            player.mana = data['mana']
            player.max_mana = data['max_mana']
            player.level = data['level']
            player.exp = data['exp']
            player.gold = data['gold']
            player.inventory = data['inventory']
            player.weapons = data['weapons']
            player.current_weapon = data['current_weapon']
            player.armor = data['armor']
            player.current_armor = data['current_armor']
            player.tech_points = data['tech_points']
            
            # Restore gadgets
            for name, gdata in data['gadgets'].items():
                gadget = Gadget(name, "common", {}, 0)  # Temporary gadget
                gadget.charges = gdata['charges']
                player.gadgets[name] = gadget
                
            # Restore powers
            for power_name in data['powers']:
                if power_name in AVAILABLE_POWERS:
                    player.powers[power_name] = AVAILABLE_POWERS[power_name]
                    
            # Restore abilities
            player.abilities = data['abilities']
            
            print(f"\nLoaded save: {player.name} (Level {player.level})")
            return player
    except (ValueError, IndexError):
        print("Invalid choice!")
    return None

def calculate_tech_points_reward(player_level, is_boss=False):
    """Calculate tech points reward based on player level and enemy type"""
    if is_boss:
        # More tech points for boss battles
        base_reward = 25
        level_bonus = player_level * 5
    else:
        # Regular combat rewards
        base_reward = 5
        level_bonus = player_level * 2
    
    return base_reward + level_bonus

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Game terminated.")


