let currentPlayer = null;

class Character {
  constructor(name, classType) {
    this.name = name;
    this.classType = this.getClassName(classType);
    this.level = 1;
    this.exp = 0;
    this.gold = 100;
    this.techPoints = 0;

    // Initialize class-specific stats
    this.initializeClassStats();

    // Set up basic inventory
    this.inventory = { "Health Potion": 2, "Mana Potion": 2 };
    this.weapons = { "Basic Sword": 8 };
    this.currentWeapon = "Basic Sword";
    this.abilities = {};
    this.statusEffects = [];
    this.gadgets = {};
    this.powers = {};
  }

  getClassName(classChoice) {
    const classNames = {
      1: "Warrior",
      2: "Mage",
      3: "Paladin",
      4: "Necromancer",
      5: "Assassin",
      6: "Druid",
      7: "Monk",
      8: "Ranger",
      9: "Warlock",
      10: "Berserker",
      11: "Alchemist",
      12: "Shaman",
    };
    return classNames[classChoice] || "Unknown";
  }

  initializeClassStats() {
    const baseStats = {
      Warrior: { health: 140, mana: 40 },
      Mage: { health: 80, mana: 120 },
      Paladin: { health: 120, mana: 60 },
      Necromancer: { health: 90, mana: 100 },
      Assassin: { health: 95, mana: 50 },
      Druid: { health: 110, mana: 70 },
      Monk: { health: 100, mana: 80 },
      Ranger: { health: 95, mana: 65 },
      Warlock: { health: 85, mana: 95 },
      Berserker: { health: 130, mana: 45 },
      Alchemist: { health: 90, mana: 80 },
      Shaman: { health: 100, mana: 90 },
    };

    const stats = baseStats[this.classType] || { health: 100, mana: 50 };
    this.health = stats.health;
    this.maxHealth = stats.health;
    this.mana = stats.mana;
    this.maxMana = stats.mana;
  }

  getScalingFactor() {
    // Calculate scaling factor based on level
    return 1 + (this.level - 1) * 0.15;
  }

  updateAbilities() {
    // Update abilities based on level and class
    const scaling = this.getScalingFactor();
    let baseAbilities = {};

    if (this.classType.toLowerCase() === "warrior" || this.classType === "1") {
      this.health = 140 + (this.level - 1) * 25; // Increased health scaling
      this.maxHealth = this.health;
      this.mana = 40 + (this.level - 1) * 8; // Reduced mana scaling
      this.maxMana = this.mana;
      baseAbilities = {
        Rage: {
          damage: Math.floor(25 * scaling),
          manaCost: 15,
          description: "Strong attack with bonus damage",
        },
        "Shield Block": {
          defense: Math.floor(15 * scaling),
          duration: 2,
          manaCost: 10,
          description: "Temporary defense boost",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Whirlwind"] = {
          damage: Math.floor(18 * scaling),
          areaDamage: Math.floor(15 * scaling),
          hits: 3,
          manaCost: 25,
          description: "Spin attack hitting multiple enemies",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Berserk"] = {
          damage: Math.floor(40 * scaling),
          manaCost: 30,
          description: "Powerful rage attack",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Battle Shout"] = {
          damageBoost: Math.floor(15 * scaling),
          duration: 3,
          manaCost: 25,
          description: "Increase damage for 3 turns",
        };
      }
    } else if (
      this.classType.toLowerCase() === "mage" ||
      this.classType === "2"
    ) {
      this.health = 80 + (this.level - 1) * 12; // Reduced health scaling
      this.maxHealth = this.health;
      this.mana = 100 + (this.level - 1) * 20; // Increased mana scaling
      this.maxMana = this.mana;
      baseAbilities = {
        Fireball: {
          damage: Math.floor(20 * scaling),
          duration: 3,
          manaCost: 15,
          description: "Fire damage over time",
          effect: "burn",
        },
        "Frost Bolt": {
          damage: Math.floor(25 * scaling),
          manaCost: 20,
          description: "Direct magic damage",
          effect: "freeze",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Lightning Strike"] = {
          damage: Math.floor(35 * scaling),
          manaCost: 25,
          description: "Powerful lightning attack",
          effect: "stun",
          duration: 1,
        };
      }
      if (this.level >= 5) {
        baseAbilities["Meteor"] = {
          damage: Math.floor(35 * scaling),
          areaDamage: Math.floor(25 * scaling),
          manaCost: 40,
          description: "Massive area damage spell",
          effect: "burn",
          duration: 2,
        };
      }
      if (this.level >= 7) {
        baseAbilities["Chain Lightning"] = {
          damage: Math.floor(20 * scaling),
          hits: 3,
          effect: "stun",
          duration: 1,
          manaCost: 45,
          description: "Lightning jumps between targets",
        };
      }
    }

    if (this.classType.toLowerCase() === "paladin" || this.classType === "3") {
      this.health = 120 + (this.level - 1) * 20; // Balanced health scaling
      this.maxHealth = this.health;
      this.mana = 60 + (this.level - 1) * 12; // Balanced mana scaling
      this.maxMana = this.mana;
      let baseAbilities = {
        "Holy Strike": {
          damage: Math.floor(20 * scaling),
          heal: Math.floor(10 * scaling),
          manaCost: 15,
          description: "Holy damage with healing",
        },
        "Divine Shield": {
          defense: Math.floor(20 * scaling),
          duration: 3,
          manaCost: 20,
          description: "Strong defensive barrier",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Consecration"] = {
          damage: Math.floor(15 * scaling),
          areaDamage: Math.floor(12 * scaling),
          heal: Math.floor(15 * scaling),
          manaCost: 25,
          description: "Holy area damage and healing",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Divine Storm"] = {
          damage: Math.floor(35 * scaling),
          heal: Math.floor(20 * scaling),
          manaCost: 35,
          description: "Powerful holy attack with healing",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Holy Nova"] = {
          damage: Math.floor(30 * scaling),
          areaDamage: Math.floor(20 * scaling),
          heal: Math.floor(25 * scaling),
          manaCost: 40,
          description: "Area damage and group healing",
        };
      }
    } else if (
      this.classType.toLowerCase() === "necromancer" ||
      this.classType === "4"
    ) {
      this.health = 90 + (this.level - 1) * 15; // Low health scaling
      this.maxHealth = this.health;
      this.mana = 90 + (this.level - 1) * 18; // High mana scaling
      this.maxMana = this.mana;
      let baseAbilities = {
        "Death Bolt": {
          damage: Math.floor(22 * scaling),
          manaCost: 15,
          description: "Dark magic damage",
        },
        "Life Drain": {
          damage: Math.floor(18 * scaling),
          heal: Math.floor(15 * scaling),
          manaCost: 20,
          description: "Drain life from enemy",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Curse"] = {
          damage: Math.floor(12 * scaling),
          duration: 4,
          manaCost: 25,
          description: "Strong damage over time",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Death Nova"] = {
          damage: Math.floor(30 * scaling),
          areaDamage: Math.floor(20 * scaling),
          manaCost: 35,
          description: "Explosion of dark energy",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Soul Harvest"] = {
          damage: Math.floor(25 * scaling),
          heal: Math.floor(15 * scaling),
          hits: 3,
          manaCost: 45,
          description: "Multiple life drains",
        };
      }
    } else if (
      this.classType.toLowerCase() === "assassin" ||
      this.classType === "5"
    ) {
      this.health = 95 + (this.level - 1) * 14; // Medium-low health scaling
      this.maxHealth = this.health;
      this.mana = 50 + (this.level - 1) * 10; // Medium mana scaling
      this.maxMana = this.mana;
      let baseAbilities = {
        Backstab: {
          damage: Math.floor(30 * scaling),
          manaCost: 15,
          description: "High damage from stealth",
        },
        "Poison Strike": {
          damage: Math.floor(15 * scaling),
          duration: 3,
          manaCost: 20,
          description: "Poisoned weapon attack",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Shadow Step"] = {
          damage: Math.floor(25 * scaling),
          manaCost: 25,
          description: "Teleport behind enemy and strike",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Death Mark"] = {
          damage: Math.floor(45 * scaling),
          duration: 2,
          manaCost: 35,
          description: "Mark target for death",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Shadow Dance"] = {
          damage: Math.floor(20 * scaling),
          hits: 5,
          manaCost: 40,
          description: "Rapid strikes from shadows",
        };
      }
    } else if (
      this.classType.toLowerCase() === "druid" ||
      this.classType === "6"
    ) {
      this.health = 110 + (this.level - 1) * 18; // Medium-high health scaling
      this.maxHealth = this.health;
      this.mana = 70 + (this.level - 1) * 15; // Medium-high mana scaling
      this.maxMana = this.mana;
      let baseAbilities = {
        "Nature's Wrath": {
          damage: Math.floor(20 * scaling),
          manaCost: 15,
          description: "Nature damage",
        },
        Regrowth: {
          heal: Math.floor(25 * scaling),
          duration: 3,
          manaCost: 20,
          description: "Strong healing over time",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Entangling Roots"] = {
          damage: Math.floor(18 * scaling),
          duration: 2,
          manaCost: 25,
          description: "Root and damage over time",
          effect: "root",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Hurricane"] = {
          damage: Math.floor(25 * scaling),
          areaDamage: Math.floor(18 * scaling),
          hits: 3,
          manaCost: 35,
          description: "Multiple nature damage hits in area",
          effect: "wind",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Nature's Fury"] = {
          damage: Math.floor(35 * scaling),
          areaDamage: Math.floor(20 * scaling),
          effect: "root",
          duration: 2,
          manaCost: 45,
          description: "Massive nature damage and root",
        };
      }
    } else if (
      this.classType.toLowerCase() === "monk" ||
      this.classType === "7"
    ) {
      this.health = 100 + (this.level - 1) * 16;
      this.maxHealth = this.health;
      this.mana = 60 + (this.level - 1) * 12;
      this.maxMana = this.mana;
      let baseAbilities = {
        "Chi Strike": {
          damage: Math.floor(25 * scaling),
          manaCost: 15,
          description: "Powerful martial arts attack",
        },
        Meditation: {
          heal: Math.floor(20 * scaling),
          duration: 2,
          manaCost: 20,
          description: "Restore health over time",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Flying Kick"] = {
          damage: Math.floor(30 * scaling),
          effect: "stun",
          duration: 1,
          manaCost: 25,
          description: "High damage leap attack with stun",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Spirit Burst"] = {
          damage: Math.floor(35 * scaling),
          heal: Math.floor(20 * scaling),
          manaCost: 35,
          description: "Damage and healing combo",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Chakra Burst"] = {
          damage: Math.floor(40 * scaling),
          hits: 3,
          heal: Math.floor(15 * scaling),
          manaCost: 35,
          description: "Energy strikes with healing",
        };
      }
    } else if (
      this.classType.toLowerCase() === "ranger" ||
      this.classType === "8"
    ) {
      this.health = 95 + (this.level - 1) * 15;
      this.maxHealth = this.health;
      this.mana = 65 + (this.level - 1) * 13;
      this.maxMana = this.mana;
      let baseAbilities = {
        "Precise Shot": {
          damage: Math.floor(28 * scaling),
          manaCost: 15,
          description: "Accurate ranged attack",
        },
        "Animal Bond": {
          heal: Math.floor(18 * scaling),
          damage: Math.floor(15 * scaling),
          manaCost: 20,
          description: "Call animal companion",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Multi Shot"] = {
          damage: Math.floor(15 * scaling),
          hits: 3,
          manaCost: 25,
          description: "Fire multiple arrows",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Hunter's Mark"] = {
          damage: Math.floor(35 * scaling),
          duration: 3,
          manaCost: 30,
          description: "Mark target for extra damage",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Arrow Storm"] = {
          damage: Math.floor(15 * scaling),
          hits: 6,
          areaDamage: Math.floor(10 * scaling),
          manaCost: 45,
          description: "Rain of arrows",
        };
      }
    } else if (
      this.classType.toLowerCase() === "warlock" ||
      this.classType === "9"
    ) {
      this.health = 85 + (this.level - 1) * 14;
      this.maxHealth = this.health;
      this.mana = 95 + (this.level - 1) * 19;
      this.maxMana = this.mana;
      let baseAbilities = {
        "Shadow Bolt": {
          damage: Math.floor(27 * scaling),
          manaCost: 15,
          description: "Dark energy attack",
        },
        "Soul Drain": {
          damage: Math.floor(20 * scaling),
          heal: Math.floor(10 * scaling),
          manaCost: 20,
          description: "Drain enemy life force",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Demon Form"] = {
          damage: Math.floor(25 * scaling),
          duration: 3,
          manaCost: 30,
          description: "Transform for enhanced damage",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Chaos Blast"] = {
          damage: Math.floor(45 * scaling),
          manaCost: 40,
          description: "Powerful chaotic explosion",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Soul Fire"] = {
          damage: Math.floor(50 * scaling),
          effect: "burn",
          duration: 3,
          manaCost: 50,
          description: "Massive fire damage with burn",
        };
      }
    } else if (
      this.classType.toLowerCase() === "berserker" ||
      this.classType === "10"
    ) {
      this.health = 130 + (this.level - 1) * 22;
      this.maxHealth = this.health;
      this.mana = 35 + (this.level - 1) * 7;
      this.maxMana = this.mana;
      let baseAbilities = {
        Frenzy: {
          damage: Math.floor(35 * scaling),
          manaCost: 15,
          description: "Powerful rage attack",
        },
        "Battle Cry": {
          damage: Math.floor(20 * scaling),
          duration: 2,
          manaCost: 20,
          description: "Intimidating shout",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Blood Rage"] = {
          damage: Math.floor(30 * scaling),
          heal: Math.floor(15 * scaling),
          manaCost: 25,
          description: "Damage boost with life drain",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Rampage"] = {
          damage: Math.floor(25 * scaling),
          hits: 4,
          manaCost: 35,
          description: "Multiple savage attacks",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Unstoppable"] = {
          damage: Math.floor(45 * scaling),
          heal: Math.floor(20 * scaling),
          effect: "rage",
          duration: 2,
          manaCost: 40,
          description: "Powerful attack with healing rage",
        };
      }
    } else if (
      this.classType.toLowerCase() === "alchemist" ||
      this.classType === "11"
    ) {
      this.health = 90 + (this.level - 1) * 15;
      this.maxHealth = this.health;
      this.mana = 80 + (this.level - 1) * 16;
      this.maxMana = this.mana;
      let baseAbilities = {
        "Acid Splash": {
          damage: Math.floor(23 * scaling),
          hits: 2,
          manaCost: 15,
          description: "Corrosive damage over time",
        },
        "Healing Elixir": {
          heal: Math.floor(30 * scaling),
          manaCost: 20,
          description: "Powerful healing potion",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Explosive Flask"] = {
          damage: Math.floor(25 * scaling),
          areaDamage: Math.floor(20 * scaling),
          manaCost: 25,
          description: "Area damage chemical explosion",
        };
        baseAbilities["Acid Flask"] = {
          damage: Math.floor(20 * scaling),
          effect: "acid",
          duration: 3,
          manaCost: 25,
          description: "Throw corrosive acid that reduces defense",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Transmutation"] = {
          heal: Math.floor(25 * scaling),
          damage: Math.floor(25 * scaling),
          manaCost: 35,
          description: "Convert damage to healing",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Chain Reaction"] = {
          damage: Math.floor(30 * scaling),
          areaDamage: Math.floor(25 * scaling),
          effect: "acid",
          duration: 3,
          manaCost: 45,
          description: "Explosive chain of reactions",
        };
      }
    } else if (
      this.classType.toLowerCase() === "shaman" ||
      this.classType === "12"
    ) {
      this.health = 105 + (this.level - 1) * 17;
      this.maxHealth = this.health;
      this.mana = 75 + (this.level - 1) * 15;
      this.maxMana = this.mana;
      let baseAbilities = {
        "Lightning Chain": {
          damage: Math.floor(22 * scaling),
          hits: 2,
          manaCost: 15,
          description: "Chain lightning attack",
        },
        "Ancestral Spirit": {
          heal: Math.floor(25 * scaling),
          duration: 2,
          manaCost: 20,
          description: "Healing over time",
        },
      };
      if (this.level >= 3) {
        baseAbilities["Earthquake"] = {
          damage: Math.floor(30 * scaling),
          areaDamage: Math.floor(25 * scaling),
          effect: "stun",
          manaCost: 25,
          description: "Ground-shaking attack",
        };
      }
      if (this.level >= 5) {
        baseAbilities["Spirit Wolves"] = {
          damage: Math.floor(20 * scaling),
          hits: 3,
          manaCost: 35,
          description: "Summon spirit wolves to attack",
        };
      }
      if (this.level >= 7) {
        baseAbilities["Elemental Fury"] = {
          damage: Math.floor(25 * scaling),
          hits: 4,
          effect: "stun",
          duration: 1,
          manaCost: 45,
          description: "Multiple elemental strikes",
        };
      }
    }

    this.abilities = baseAbilities;
  }

  unlockPower(powerName) {
    // Unlock a new power if player has enough tech points
    if (AVAILABLE_POWERS[powerName] && !this.powers[powerName]) {
      const power = AVAILABLE_POWERS[powerName];
      if (this.techPoints >= power.cost) {
        this.techPoints -= power.cost;
        this.powers[powerName] = power;
        console.log(`Unlocked power: ${powerName}!`);
        console.log(`Effect: ${power.description}`);
        return true;
      }
    }
    return false;
  }
}

// Add Gadget class
class Gadget {
  constructor(name, rarity, effect, cost) {
    this.name = name;
    this.rarity = rarity; // common, rare, epic, legendary
    this.effect = effect;
    this.cost = cost;
    this.charges = this.getCharges();
  }

  getCharges() {
    const charges = {
      common: 3,
      rare: 2,
      epic: 2,
      legendary: 1,
    };
    return charges[this.rarity] || 1;
  }

  use() {
    if (this.charges > 0) {
      this.charges -= 1;
      return true;
    }
    return false;
  }
}

// Add Power class to define available powers
class Power {
  constructor(name, effect, description, cost) {
    this.name = name;
    this.effect = effect;
    this.description = description;
    this.cost = cost; // Cost in tech points to unlock
  }
}

// Add available powers dictionary
const AVAILABLE_POWERS = {
  "Life Link": new Power(
    "Life Link",
    { healPercent: 0.15, cooldown: 3 },
    "Heal 15% of damage dealt",
    100
  ),
  "Critical Strike": new Power(
    "Critical Strike",
    { critChance: 0.2, critMultiplier: 2.0 },
    "20% chance to deal double damage",
    150
  ),
  "Mana Shield": new Power(
    "Mana Shield",
    { damageToMana: 0.3, threshold: 0.5 },
    "30% of damage taken uses mana instead when above 50% mana",
    200
  ),
  "Battle Rage": new Power(
    "Battle Rage",
    { damageBoost: 0.25, healthThreshold: 0.3 },
    "Deal 25% more damage when below 30% health",
    250
  ),
};

// Update Enemy class for better balance
class Enemy {
  constructor(name, health, damage, expReward, goldReward, level = 1) {
    this.name = name;
    this.level = level;
    const levelMultiplier = 1 + (level - 1) * 0.2;
    this.health = Math.floor(health * levelMultiplier);
    this.maxHealth = this.health;
    this.damage = Math.floor(damage * levelMultiplier);
    this.expReward = Math.floor(expReward * levelMultiplier);
    this.goldReward = Math.floor(goldReward * levelMultiplier);
    this.statusEffects = [];
    this.abilities = {};
    this.isBoss = false;
  }

  isAlive() {
    // Check if enemy is still alive
    return this.health > 0;
  }

  takeDamage(amount) {
    // Handle damage taken by enemy
    this.health = Math.max(0, this.health - amount);
    return amount;
  }
}

async function getTarget(enemies, auto = false) {
  // Helper function to handle target selection
  if (enemies.length === 1 || auto) {
    // Auto-target the first living enemy
    for (const enemy of enemies) {
      if (enemy.health > 0) {
        return enemy;
      }
    }
  } else {
    console.log("\nChoose your target:");
    const validTargets = enemies
      .map((enemy, i) => ({ index: i, enemy }))
      .filter(({ enemy }) => enemy.health > 0);
    validTargets.forEach(({ index, enemy }) => {
      console.log(`${index + 1}. ${enemy.name} - HP: ${enemy.health}`);
    });

    const targetIdx = parseInt(await prompt("> ")) - 1;
    if (targetIdx >= 0 && targetIdx < validTargets.length) {
      return enemies[targetIdx];
    }
  }
  return null;
}

function levelUpDisplay(player, oldLevel, rewards) {
  // Display level up information with visual effects
  console.log("\n" + "=".repeat(50));
  console.log(`╔${"═".repeat(48)}╗`);
  console.log(`║${" ".repeat(17)}LEVEL UP!${" ".repeat(22)}║`);
  console.log(
    `║${" ".repeat(16)}Level ${oldLevel} → ${player.level}${" ".repeat(21)}║`
  );
  console.log(`╚${"═".repeat(48)}╝`);
  console.log("\nStats increased:");
  console.log(
    `♥ Max HP: ${player.maxHealth - rewards.health} → ${player.maxHealth}`
  );
  console.log(`✧ Max MP: ${player.maxMana - rewards.mana} → ${player.maxMana}`);

  // Show new abilities if unlocked
  if ([3, 5].includes(player.level)) {
    console.log("\n⚔ New Abilities Unlocked!");
    const newAbilities = Object.entries(player.abilities).filter(
      ([name]) => name !== "Basic Attack"
    );
    newAbilities.forEach(([name, ability]) => {
      console.log(`- ${name}: ${ability.description}`);
    });
  }

  console.log("=".repeat(50) + "\n");
  // In the combat function, update the auto-target initialization
  async function combat(player, enemies) {
    console.log("\nEnemies appear!");
    enemies.forEach((enemy) => {
      console.log(`- ${enemy.name} (HP: ${enemy.health})`);
    });

    // Set auto-target to False by default
    let autoTarget = false;

    while (enemies.some((enemy) => enemy.health > 0) && player.health > 0) {
      // Process status effects
      processStatusEffects(player);
      enemies.forEach((enemy) => {
        if (enemy.health > 0) {
          processStatusEffects(enemy);
        }
      });

      // Display battle status
      console.log("\n" + "-".repeat(40));
      console.log(`Your HP: ${player.health}/${player.maxHealth}`);
      console.log(`Your MP: ${player.mana}/${player.maxMana}`);
      console.log("\nEnemies:");
      enemies.forEach((enemy, i) => {
        if (enemy.health > 0) {
          console.log(`${i + 1}. ${enemy.name} - HP: ${enemy.health}`);
        }
      });

      console.log("\nWhat would you like to do?");
      console.log("1. Attack");
      console.log("2. Use Ability");
      console.log("3. Use Item");
      console.log("4. Use Gadget");
      console.log("5. Run");
      console.log(`6. Toggle Auto-target (${autoTarget ? "ON" : "OFF"})`);

      const choice = await prompt("> ");

      if (choice === "6") {
        autoTarget = !autoTarget;
        console.log(`Auto-targeting turned ${autoTarget ? "ON" : "OFF"}`);
        continue;
      }

      // Target selection for attacks and abilities
      let target;
      if (
        ["1", "2", "4"].includes(choice) &&
        enemies.some((enemy) => enemy.health > 0)
      ) {
        target = await getTarget(enemies, autoTarget);
        if (!target) {
          console.log("Invalid target!");
          continue;
        }
      }

      // Process player turn
      if (choice === "1") {
        // Basic attack
        if (target) {
          processAttack(player, target, enemies);
        } else {
          console.log("No valid target!");
          continue;
        }
      } else if (choice === "2") {
        // Use ability
        const abilitiesList = showAbilities(player);
        const abilityChoice = await prompt(
          "Choose ability number (or 'back'): "
        );

        if (abilityChoice.toLowerCase() === "back") {
          continue;
        }

        try {
          const abilityIdx = parseInt(abilityChoice) - 1;
          if (abilityIdx >= 0 && abilityIdx < abilitiesList.length) {
            const [abilityName, ability] = abilitiesList[abilityIdx];
            if (player.mana >= ability.mana_cost) {
              target = await getTarget(enemies, autoTarget);
              if (target) {
                const duration = ability.duration || 0;
                processAbility(player, target, enemies, abilityName, duration);
              } else {
                console.log("No valid target!");
                continue;
              }
            } else {
              console.log("Not enough mana!");
              continue;
            }
          } else {
            console.log("Invalid ability number!");
            continue;
          }
        } catch (error) {
          console.log("Invalid input!");
          continue;
        }
      } else if (choice === "3") {
        console.log("\nAvailable items:");
        if (player.inventory["Health Potion"] > 0) {
          console.log("1. Health Potion");
        }
        if (player.inventory["Mana Potion"] > 0) {
          console.log("2. Mana Potion");
        }

        const itemChoice = await prompt("Choose item to use (or 'back'): ");

        if (itemChoice === "1" && player.inventory["Health Potion"] > 0) {
          player.health = Math.min(player.maxHealth, player.health + 30);
          player.inventory["Health Potion"]--;
          console.log("You drink a health potion and recover 30 HP!");
        } else if (itemChoice === "2" && player.inventory["Mana Potion"] > 0) {
          player.mana = Math.min(player.maxMana, player.mana + 25);
          player.inventory["Mana Potion"]--;
          console.log("You drink a mana potion and recover 25 MP!");
        } else if (itemChoice.toLowerCase() === "back") {
          continue;
        } else {
          console.log("Invalid item or not enough potions!");
          continue;
        }
      } else if (choice === "4") {
        // Use Gadget
        if (player.gadgets.length > 0) {
          const gadgetList = showGadgets(player);
          if (gadgetList.length > 0) {
            const gadgetChoice = await prompt(
              "Choose gadget number (or 'back'): "
            );

            try {
              const gadgetIdx = parseInt(gadgetChoice) - 1;
              if (gadgetIdx >= 0 && gadgetIdx < gadgetList.length) {
                const [name, gadget] = gadgetList[gadgetIdx];
                if (gadget.charges > 0) {
                  gadget.charges--;
                  const result = processGadgetEffect(
                    player,
                    target,
                    enemies,
                    gadget.effect
                  );
                  if (result === "fled") {
                    return "fled";
                  }
                } else {
                  console.log("No charges remaining on this gadget!");
                }
              } else {
                console.log("Invalid gadget number!");
              }
            } catch (error) {
              console.log("Invalid input!");
            }
          } else {
            console.log("No gadgets available!");
          }
        } else {
          console.log("No gadgets available!");
        }
      } else if (choice === "5") {
        if (Math.random() < 0.5) {
          console.log("You successfully fled from combat!");
          return "fled"; // Changed return value to indicate fled status
        } else {
          console.log("You failed to run away!");
        }
      }

      // Enemy turns
      enemies.forEach((enemy) => {
        if (enemy.health > 0) {
          const damage = processEnemyAttack(player, enemy);
          player.health -= damage;
          console.log(`${enemy.name} attacks you for ${damage} damage!`);
        }
      });

      // Check player death
      if (player.health <= 0) {
        console.log("You have been defeated...");
        return false;
      }
    }

    // Combat victory - remove duplicate rewards
    if (player.health > 0) {
      const defeatedEnemies = enemies.filter((e) => e.health <= 0);
      const totalExp = defeatedEnemies.reduce(
        (sum, e) => sum + e.exp_reward,
        0
      );
      const totalGold = defeatedEnemies.reduce(
        (sum, e) => sum + e.gold_reward,
        0
      );
      const totalTp = defeatedEnemies.length * (player.level * 15);

      // Apply rewards once
      player.exp += totalExp;
      player.gold += totalGold;
      player.tech_points += totalTp;

      console.log("\nRewards:");
      console.log(`• ${totalExp} EXP`);
      console.log(`• ${totalGold} Gold`);
      if (totalTp > 0) {
        console.log(`• ${totalTp} Tech Points`);
      }

      // Remove duplicate exp addition
      let oldLevel = player.level;

      // Check for level up
      while (player.exp >= calculateExpRequirement(player.level)) {
        player.exp -= calculateExpRequirement(player.level);
        player.level++;
        const rewards = calculateLevelRewards(player.level);
        player.maxHealth += rewards.health;
        player.health = player.maxHealth;
        player.maxMana += rewards.mana;
        player.mana = player.maxMana;

        // Display level up screen
        levelUpDisplay(player, oldLevel, rewards);

        // Update abilities for new level
        player.updateAbilities();
        oldLevel = player.level;
      }

      // Victory healing
      const healAmount = Math.floor(
        player.maxHealth * (0.15 + player.level * 0.01)
      );
      const manaRestore = Math.floor(
        player.maxMana * (0.1 + player.level * 0.01)
      );
      player.health = Math.min(player.maxHealth, player.health + healAmount);
      player.mana = Math.min(player.maxMana, player.mana + manaRestore);
      console.log(
        `Victory healing: Recovered ${healAmount} HP and ${manaRestore} MP!`
      );

      return true;
    }
  }

  // Add gadget effect processing
  function processGadgetEffect(player, target, enemies, effect) {
    if (typeof effect === "object") {
      if (effect.damage) {
        // Handle single target damage
        target.health -= effect.damage;
        console.log(`Gadget deals ${effect.damage} damage to ${target.name}!`);

        // Handle area damage if present
        if (effect.area_damage) {
          enemies.forEach((other) => {
            if (other !== target && other.health > 0) {
              other.health -= effect.area_damage;
              console.log(
                `${other.name} takes ${effect.area_damage} splash damage!`
              );
            }
          });
        }
      }

      if (effect.heal) {
        const originalHealth = player.health;
        player.health = Math.min(player.maxHealth, player.health + effect.heal);
        const actualHeal = player.health - originalHealth;
        console.log(`Gadget heals you for ${actualHeal} HP!`);
      }

      if (effect.flee) {
        if (Math.random() < (effect.chance || 0.5)) {
          console.log("Gadget allows you to escape!");
          return "fled";
        }
      }

      if (effect.defense) {
        player.status_effects.push({
          name: "Shield",
          defense: effect.defense,
          duration: effect.duration,
        });
        console.log(
          `Shield activated! +${effect.defense} defense for ${effect.duration} turns!`
        );
      }
    }

    if (effect.revive) {
      if (player.health <= 0) {
        player.health = Math.floor(player.maxHealth * effect.health_percent);
        console.log("Phoenix Protocol activates! You're revived!");
      }
    }
  }

  // Update experience and level scaling
  function calculateExpRequirement(level) {
    return Math.floor(100 * Math.pow(1.5, level - 1));
  }

  function calculateLevelRewards(level) {
    return {
      health: 12 + level * 2, // Reduced from 15 + (level * 3)
      mana: 6 + level * 1.5, // Reduced from 8 + (level * 2)
      damage_bonus: Math.floor(level * 0.8),
      defense_bonus: Math.floor(level * 0.7),
    };
  }

  // Update shop function's item handling
  async function shop(player) {
    const items = {
      // Basic items (adjusted prices)
      "Health Potion": { cost: 15, effect: "Restore 35 HP", min_level: 1 },
      "Mana Potion": { cost: 15, effect: "Restore 30 MP", min_level: 1 },

      // Melee Weapons
      // Tier 1
      "Iron Sword": { cost: 45, damage: 10, type: "melee", min_level: 1 },
      "Bronze Axe": { cost: 50, damage: 12, type: "melee", min_level: 1 },

      // Tier 2
      "Steel Sword": { cost: 140, damage: 16, type: "melee", min_level: 3 },
      "Battle Axe": { cost: 150, damage: 18, type: "melee", min_level: 3 },
      "War Hammer": {
        cost: 200,
        damage: 14,
        area_damage: 8,
        type: "melee",
        min_level: 3,
        description: "Heavy weapon that deals area damage",
      },

      // Tier 3
      "Flame Sword": { cost: 280, damage: 28, type: "melee", min_level: 5 },
      "Dragon Cleaver": {
        cost: 400,
        damage: 25,
        area_damage: 15,
        type: "melee",
        min_level: 5,
        description: "Massive sword with wide cleaving damage",
      },

      // Ranged Weapons
      // Tier 1
      "Wooden Bow": { cost: 40, damage: 8, type: "ranged", min_level: 1 },
      "Wooden Staff": {
        cost: 45,
        damage: 8,
        mana_bonus: 12,
        type: "ranged",
        min_level: 1,
      },

      // Tier 2
      Longbow: { cost: 145, damage: 15, type: "ranged", min_level: 3 },
      "Magic Staff": {
        cost: 160,
        damage: 14,
        mana_bonus: 20,
        type: "ranged",
        min_level: 3,
      },
      "Thundering Bow": {
        cost: 220,
        damage: 12,
        area_damage: 10,
        type: "ranged",
        min_level: 3,
        description: "Bow that creates lightning area damage",
      },

      // Tier 3
      "Frost Staff": {
        cost: 290,
        damage: 25,
        mana_bonus: 35,
        type: "ranged",
        min_level: 5,
      },
      "Storm Staff": {
        cost: 450,
        damage: 22,
        area_damage: 18,
        mana_bonus: 30,
        type: "ranged",
        min_level: 5,
        description: "Powerful staff that creates storm damage",
      },

      // Armor remains the same
      "Leather Armor": { cost: 50, defense: 6, min_level: 1 },
      "Chain Mail": { cost: 120, defense: 12, min_level: 3 },
      "Plate Armor": { cost: 250, defense: 20, min_level: 5 },

      // Multi-hit weapons
      "Twin Daggers": {
        cost: 160,
        damage: 8,
        hits: 2,
        type: "melee",
        min_level: 3,
        description: "Strike twice per attack",
      },
      "Triple Crossbow": {
        cost: 180,
        damage: 7,
        hits: 3,
        type: "ranged",
        min_level: 3,
        description: "Fire three bolts per attack",
      },
      "Flurry Blade": {
        cost: 350,
        damage: 12,
        hits: 4,
        type: "melee",
        min_level: 5,
        description: "Fast blade dealing multiple hits",
      },
    };

    while (true) {
      console.log("\nWelcome to the shop!");
      console.log(`Your gold: ${player.gold}`);
      console.log("\nAvailable items:");
      for (const [item, details] of Object.entries(items)) {
        let desc = details.effect || "Equipment";
        if (details.damage) {
          desc = `Damage: ${details.damage}`;
        }
        if (details.defense) {
          desc = `Defense: ${details.defense}`;
        }
        if (details.mana_bonus) {
          desc += `, Mana Bonus: ${details.mana_bonus}`;
        }
        console.log(`${item}: ${details.cost} gold - ${desc}`);
      }
      console.log("\nEnter item name to buy (or 'exit' to leave):");

      const choice = (await prompt("> ")).title();
      if (choice.toLowerCase() === "exit") {
        break;
      }

      if (items[choice]) {
        if (player.level >= items[choice].min_level) {
          // Check level requirement
          if (player.gold >= items[choice].cost) {
            // Store old gold for verification
            const oldGold = player.gold;
            player.gold -= items[choice].cost;

            // Verify transaction
            if (player.gold >= 0) {
              if (items[choice].damage) {
                if (items[choice].area_damage) {
                  player.weapons[choice] = {
                    damage: items[choice].damage,
                    area_damage: items[choice].area_damage,
                    type: items[choice].type,
                  };
                } else {
                  player.weapons[choice] = items[choice];
                }
              } else if (items[choice].defense) {
                player.armor[choice] = items[choice].defense;
              } else {
                player.inventory[choice] = (player.inventory[choice] || 0) + 1;
              }
              console.log(`Bought ${choice}!`);
              console.log(`Remaining gold: ${player.gold}`);
            } else {
              player.gold = oldGold; // Revert if something went wrong
              console.log("Transaction failed!");
            }
          } else {
            console.log("Not enough gold!");
          }
        } else {
          console.log(`Required level: ${items[choice].min_level}`);
        }
      } else {
        console.log("Invalid item!");
      }
    }
  }

  // Add Gadget Shop function
  async function gadgetShop(player) {
    const gadgets = {
      // Common gadgets (50 TP)
      "Smoke Bomb": new Gadget(
        "Smoke Bomb",
        "common",
        {
          flee: true,
          chance: 0.8,
          description: "80% chance to escape combat",
        },
        50
      ),
      "Health Injector": new Gadget(
        "Health Injector",
        "common",
        {
          heal: 40,
          description: "Restore 40 HP instantly",
        },
        50
      ),
      "Energy Cell": new Gadget(
        "Energy Cell",
        "common",
        {
          mana: 35,
          description: "Restore 35 MP instantly",
        },
        50
      ),

      // Rare gadgets (100 TP)
      "Shock Generator": new Gadget(
        "Shock Generator",
        "rare",
        {
          damage: 60,
          stun: 1,
          description: "Deal 60 damage and stun for 1 turn",
        },
        100
      ),
      "Force Field": new Gadget(
        "Force Field",
        "rare",
        {
          defense: 25,
          duration: 3,
          description: "+25 defense for 3 turns",
        },
        100
      ),
      "Multi Targeter": new Gadget(
        "Multi Targeter",
        "rare",
        {
          damage: 30,
          targets: 3,
          description: "Hit 3 enemies for 30 damage each",
        },
        100
      ),

      // Epic gadgets (200 TP)
      "Chrono Shifter": new Gadget(
        "Chrono Shifter",
        "epic",
        {
          extra_turn: true,
          heal: 30,
          description: "Take another turn and heal 30 HP",
        },
        200
      ),
      "Power Amplifier": new Gadget(
        "Power Amplifier",
        "epic",
        {
          damage_boost: 1.5,
          duration: 2,
          description: "Increase damage by 50% for 2 turns",
        },
        200
      ),

      // Legendary gadgets (400 TP)
      "Quantum Annihilator": new Gadget(
        "Quantum Annihilator",
        "legendary",
        {
          damage: 150,
          area_damage: 75,
          description: "Deal 150 damage + 75 area damage",
        },
        400
      ),
      "Phoenix Core": new Gadget(
        "Phoenix Core",
        "legendary",
        {
          revive: true,
          health_percent: 0.5,
          description: "Revive with 50% HP when defeated",
        },
        400
      ),
    };

    while (true) {
      console.log("\n=== Gadget Shop ===");
      console.log(`Tech Points: ${player.tech_points}`);
      console.log("\nAvailable Gadgets:");

      for (const [name, gadget] of Object.entries(gadgets)) {
        if (!player.gadgets[name]) {
          console.log(
            `${name} (${
              gadget.rarity.charAt(0).toUpperCase() + gadget.rarity.slice(1)
            }) - ${gadget.cost} TP`
          );
          console.log(`  Effect: ${JSON.stringify(gadget.effect)}`);
          console.log(`  Charges: ${gadget.getCharges()}`);
        }
      }

      console.log("\nEnter gadget name to buy (or 'exit' to leave):");
      const choice = (await prompt("> ")).trim().toLowerCase();

      if (choice === "exit") {
        break;
      }

      if (gadgets[choice] && !player.gadgets[choice]) {
        if (player.tech_points >= gadgets[choice].cost) {
          player.tech_points -= gadgets[choice].cost;
          player.gadgets[choice] = gadgets[choice];
          console.log(`Bought ${choice}!`);
        } else {
          console.log("Not enough Tech Points!");
        }
      } else {
        console.log("Invalid gadget or already owned!");
      }
    }
  }

  async function powerShop(player) {
    while (true) {
      console.log("\n=== Power Shop ===");
      console.log(`Tech Points: ${player.tech_points}`);
      console.log("\nAvailable Powers:");

      for (const [name, power] of Object.entries(AVAILABLE_POWERS)) {
        if (!player.powers[name]) {
          console.log(`${name} - ${power.cost} TP`);
          console.log(`Effect: ${power.description}`);
        }
      }

      console.log("\nEnter power name to unlock (or 'exit' to leave):");
      const choice = (await prompt("> ")).trim().toLowerCase();

      if (choice === "exit") {
        break;
      }

      if (AVAILABLE_POWERS[choice]) {
        if (!player.powers[choice]) {
          if (player.unlockPower(choice)) {
            console.log(`Successfully unlocked ${choice}!`);
          } else {
            console.log("Not enough Tech Points!");
          }
        } else {
          console.log("Power already unlocked!");
        }
      } else {
        console.log("Invalid power name!");
      }
    }
  }

  function showAbilities(player) {
    console.log("\nAvailable Abilities:");
    const abilitiesList = Object.entries(player.abilities);
    abilitiesList.forEach(([ability, details], index) => {
      const desc = details.description;
      const mana = details.mana_cost;
      console.log(`${index + 1}. ${ability} - ${desc} (Mana: ${mana})`);
    });
    return abilitiesList;
  }

  function showGadgets(player) {
    const gadgetList = [];
    console.log("\nAvailable Gadgets:");
    for (const [name, gadget] of Object.entries(player.gadgets)) {
      if (gadget.charges > 0) {
        gadgetList.push([name, gadget]);
        console.log(
          `${gadgetList.length}. ${name} (${gadget.charges} charges)`
        );
      }
    }
    return gadgetList;
  }

  function processAttack(player, target, enemies) {
    const weaponStats = player.weapons[player.currentWeapon];
    let totalDamage = 0;
    let livingEnemies = enemies.filter((e) => e.health > 0);
    let currentTarget = target.health > 0 ? target : null;

    if (!livingEnemies.length) {
      console.log("No valid targets remaining!");
      return totalDamage;
    }

    if (!currentTarget && livingEnemies.length) {
      currentTarget = livingEnemies[0];
    }

    // Calculate base damage
    if (typeof weaponStats === "object") {
      const baseDamage = weaponStats.damage;
      const levelBonus = Math.floor(player.level * 1.5);

      // Handle multi-hit weapons
      if (weaponStats.hits) {
        const hits = weaponStats.hits;
        let enemyIndex = livingEnemies.indexOf(currentTarget);

        for (let hit = 0; hit < hits; hit++) {
          if (!livingEnemies.length) break;

          // Get current target, cycle through living enemies
          currentTarget = livingEnemies[enemyIndex % livingEnemies.length];

          const variation = Math.floor(Math.random() * 5) - 2; // Random variation between -2 and 2
          const hitDamage = Math.max(1, baseDamage + levelBonus + variation);

          currentTarget.health -= hitDamage;
          totalDamage += hitDamage;
          console.log(
            `Hit ${hit + 1}: ${hitDamage} damage to ${currentTarget.name}!`
          );

          // Check if current target died
          if (currentTarget.health <= 0) {
            console.log(`${currentTarget.name} has been defeated!`);
            livingEnemies = enemies.filter((e) => e.health > 0);
            if (livingEnemies.length) {
              enemyIndex = (enemyIndex + 1) % livingEnemies.length;
            } else {
              break;
            }
          } else {
            enemyIndex += 1;
          }
        }

        console.log(`Total damage dealt: ${totalDamage}`);
      } else {
        // Single hit processing
        const variation = Math.floor(Math.random() * 5) - 2; // Random variation between -2 and 2
        const mainDamage = Math.max(1, baseDamage + levelBonus + variation);
        target.health -= mainDamage;
        totalDamage = mainDamage;
        console.log(`You deal ${mainDamage} damage to ${target.name}!`);
      }

      // Process area damage
      if (weaponStats.area_damage && livingEnemies.length) {
        for (const other of livingEnemies) {
          if (other !== target && other.health > 0) {
            const splashDamage = Math.max(
              1,
              weaponStats.area_damage + Math.floor(levelBonus * 0.5)
            );
            other.health -= splashDamage;
            totalDamage += splashDamage;
            console.log(`${other.name} takes ${splashDamage} splash damage!`);
          }
        }
      }
    } else {
      // Simple weapon damage
      const variation = Math.floor(Math.random() * 5) - 2; // Random variation between -2 and 2
      const mainDamage = Math.max(
        1,
        weaponStats + Math.floor(player.level * 1.5) + variation
      );
      target.health -= mainDamage;
      totalDamage = mainDamage;
      console.log(`You deal ${mainDamage} damage to ${target.name}!`);
    }

    return totalDamage;
  }

  function processEnemyAttack(player, enemy) {
    const baseDamage = enemy.damage;
    const armorValue = player.armor[player.currentArmor];
    const defenseReduction = Math.floor(
      armorValue * (0.3 + player.level * 0.015)
    ); // Reduced scaling
    const finalDamage = Math.max(1, baseDamage - defenseReduction);
    return finalDamage;
  }

  function processAbility(player, target, enemies, abilityName, duration = 0) {
    const ability = player.abilities[abilityName];
    player.mana -= ability.mana_cost;
    let totalDamage = 0;
    let totalHealing = 0;

    // Get ability parameters
    const baseDamage = ability.damage || 0;
    const baseHeal = ability.heal || 0;
    const hits = ability.hits || 1;
    const effectType = ability.effect || null;
    duration = ability.duration || duration;

    // Process healing over time
    if (baseHeal > 0 && duration > 0) {
      player.status_effects.push({
        name: "Regeneration",
        heal: baseHeal,
        duration: duration,
      });
      console.log(
        `Regeneration effect: ${baseHeal} HP per turn for ${duration} turns!`
      );
    } else if (baseHeal > 0) {
      for (let hit = 0; hit < hits; hit++) {
        const healAmount = baseHeal;
        const originalHealth = player.health;
        player.health = Math.min(player.maxHealth, player.health + healAmount);
        const actualHeal = player.health - originalHealth;
        totalHealing += actualHeal;
        if (actualHeal > 0) {
          console.log(`Heal ${hit + 1}: Restored ${actualHeal} HP!`);
        }
      }
    }

    // Process damage
    if (ability.area_damage) {
      // Area damage to all enemies
      const mainDamage = baseDamage;
      const areaDamage = ability.area_damage;

      // Apply main damage to target
      target.health -= mainDamage;
      totalDamage += mainDamage;
      console.log(`Main damage: ${mainDamage} to ${target.name}`);

      // Apply area damage to other enemies
      for (const enemy of enemies) {
        if (enemy !== target && enemy.health > 0) {
          enemy.health -= areaDamage;
          totalDamage += areaDamage;
          console.log(`Area damage: ${areaDamage} to ${enemy.name}`);
        }
      }
    } else if (ability.hits) {
      for (let hit = 0; hit < hits; hit++) {
        if (target.health > 0) {
          target.health -= baseDamage;
          totalDamage += baseDamage;
          console.log(
            `Hit ${hit + 1}: ${baseDamage} damage to ${target.name}!`
          );

          // Process healing from damage if ability has both
          if (baseHeal > 0) {
            const healFromDamage = Math.floor(baseDamage * 0.5); // 50% of damage dealt
            const originalHealth = player.health;
            player.health = Math.min(
              player.maxHealth,
              player.health + healFromDamage
            );
            const actualHeal = player.health - originalHealth;
            totalHealing += actualHeal;
            if (actualHeal > 0) {
              console.log(
                `Life drain from hit ${hit + 1}: Restored ${actualHeal} HP!`
              );
            }
          }
        }
      }
    }

    if (totalHealing > 0) {
      console.log(`Total healing done: ${totalHealing}`);
    }
    if (totalDamage > 0) {
      console.log(`Total damage dealt: ${totalDamage}`);
    }

    // Apply status effect if present
    if (effectType) {
      applyStatusEffect(target, effectType, baseDamage, duration);
    }

    return totalDamage;
  }

  function applyStatusEffect(target, effectType, baseDamage, duration) {
    if (effectType === "burn") {
      target.status_effects.push({
        name: "Burned",
        damage: Math.floor(baseDamage / 2),
        duration: duration,
      });
      console.log(`${target.name} is burned for ${duration} turns!`);
    } else if (effectType === "acid") {
      // Acid reduces defense and does damage over time
      target.status_effects.push({
        name: "Corroded",
        damage: Math.floor(baseDamage / 3),
        defense_reduction: 5,
        duration: duration,
      });
      console.log(`${target.name} is corroded for ${duration} turns!`);
    } else if (effectType === "freeze") {
      target.status_effects.push({
        name: "Frozen",
        damage: Math.floor(baseDamage / 2),
        duration: duration,
        damage_reduction: 0.5,
      });
      console.log(`${target.name} is frozen for ${duration} turns!`);
    } else if (effectType === "stun") {
      target.status_effects.push({
        name: "Stunned",
        duration: duration,
      });
      console.log(`${target.name} is stunned for ${duration} turns!`);
    }
  }

  function processStatusEffects(entity) {
    let isStunned = false;
    let damageMultiplier = 1.0;

    for (const effect of [...entity.status_effects]) {
      if (effect.name === "Corroded") {
        const damage = effect.damage;
        entity.health -= damage;
        console.log(`${entity.name} takes ${damage} acid damage!`);
        // Apply defense reduction if entity has armor
        if (entity.armor && entity.currentArmor) {
          const currentDefense = entity.armor[entity.currentArmor];
          const reducedDefense = Math.max(
            0,
            currentDefense - effect.defense_reduction
          );
          entity.armor[entity.currentArmor] = reducedDefense;
          console.log(
            `${entity.name}'s armor is corroded! Defense reduced to ${reducedDefense}!`
          );
        }
      } else if (effect.name === "Poison") {
        const damage = effect.damage;
        entity.health -= damage;
        console.log(`${entity.name} takes ${damage} poison damage!`);
      } else if (effect.name === "Burned") {
        const damage = effect.damage;
        entity.health -= damage;
        console.log(`${entity.name} takes ${damage} burn damage!`);
      } else if (effect.name === "Frozen") {
        const damage = effect.damage;
        entity.health -= damage;
        damageMultiplier *= effect.damage_reduction || 1.0;
        console.log(
          `${entity.name} takes ${damage} frost damage and has reduced damage!`
        );
      } else if (effect.name === "Regeneration") {
        const heal = effect.heal;
        entity.health = Math.min(entity.maxHealth, entity.health + heal);
        console.log(`${entity.name} is stunned and skips their turn!`);
      }

      effect.duration -= 1;
      if (effect.duration <= 0) {
        entity.status_effects = entity.status_effects.filter(
          (e) => e !== effect
        );
        console.log(`${effect.name} effect has worn off!`);
      }
    }
    return isStunned, damageMultiplier;
  }

  // Update show_inventory_menu function
  async function showInventoryMenu(player) {
    while (true) {
      console.log("\n=== Inventory Menu ===");
      console.log("1. View Items");
      console.log("2. Change Weapon");
      console.log("3. Change Armor");
      console.log("4. Back");

      const choice = await prompt("> ");

      if (choice === "1") {
        console.log("\nInventory:");
        for (const [item, quantity] of Object.entries(player.inventory)) {
          console.log(`${item}: ${quantity}`);
        }

        console.log("\nMelee Weapons:");
        for (const [weapon, stats] of Object.entries(player.weapons)) {
          if (typeof stats === "object" && stats.type === "melee") {
            console.log(`${weapon} (Damage: ${stats.damage})`);
          }
        }

        console.log("\nRanged Weapons:");
        for (const [weapon, stats] of Object.entries(player.weapons)) {
          if (typeof stats === "object" && stats.type === "ranged") {
            let desc = `Damage: ${stats.damage}`;
            if (stats.mana_bonus) {
              desc += `, Mana Bonus: ${stats.mana_bonus}`;
            }
            console.log(`${weapon} (${desc})`);
          }
        }

        console.log(`\nCurrently equipped weapon: ${player.currentWeapon}`);
        console.log("\nArmor:");
        for (const [armor, defense] of Object.entries(player.armor)) {
          console.log(`${armor} (Defense: ${defense})`);
        }
        console.log(`Currently equipped armor: ${player.currentArmor}`);
      } else if (choice === "2") {
        console.log("\nAvailable Weapons:");
        const weapons = Object.keys(player.weapons);
        weapons.forEach((weapon, index) => {
          const damage = player.weapons[weapon];
          console.log(`${index + 1}. ${weapon} (Damage: ${damage})`);
          if (weapon === player.currentWeapon) {
            console.log("   *Currently Equipped*");
          }
        });

        try {
          const weaponChoice = parseInt(
            await prompt("\nChoose weapon number (0 to cancel): "),
            10
          );
          if (weaponChoice > 0 && weaponChoice <= weapons.length) {
            const newWeapon = weapons[weaponChoice - 1];
            if (newWeapon !== player.currentWeapon) {
              player.currentWeapon = newWeapon;
              console.log(`Equipped ${newWeapon}!`);
            } else {
              console.log("That weapon is already equipped!");
            }
          } else if (weaponChoice !== 0) {
            console.log("Invalid weapon number!");
          }
        } catch (error) {
          console.log("Invalid input!");
        }
      } else if (choice === "3") {
        console.log("\nAvailable Armor:");
        const armors = Object.keys(player.armor);
        armors.forEach((armor, index) => {
          const defense = player.armor[armor];
          console.log(`${index + 1}. ${armor} (Defense: ${defense})`);
          if (armor === player.currentArmor) {
            console.log("   *Currently Equipped*");
          }
        });

        try {
          const armorChoice = parseInt(
            await prompt("\nChoose armor number (0 to cancel): "),
            10
          );
          if (armorChoice > 0 && armorChoice <= armors.length) {
            const newArmor = armors[armorChoice - 1];
            if (newArmor !== player.currentArmor) {
              player.currentArmor = newArmor;
              console.log(`Equipped ${newArmor}!`);
            } else {
              console.log("That armor is already equipped!");
            }
          } else if (armorChoice !== 0) {
            console.log("Invalid armor number!");
          }
        } catch (error) {
          console.log("Invalid input!");
        }
      } else if (choice === "4") {
        break;
      }
    }
  }

  // Define enemy types as a class for better organization
  class EnemyType {
    constructor(name, max_health, damage, exp_reward, gold_reward, level = 1) {
      this.name = name;
      this.max_health = max_health;
      this.damage = damage;
      this.exp_reward = exp_reward;
      this.gold_reward = gold_reward;
      this.level = level;
    }
  }

  // Define spawn table with enemy types and their spawn chances
  const spawnTable = [
    // Level 1 enemies (increased rewards)
    [new EnemyType("Goblin", 30, 8, 20, 25, 1), 20, 1], // Increased from 15 to 25 gold
    [new EnemyType("Wolf", 35, 10, 25, 30, 1), 20, 1], // Increased from 20 to 30 gold
    [new EnemyType("Slime", 25, 6, 15, 20, 1), 15, 1], // Increased from 10 to 20 gold

    // Level 2 enemies
    [new EnemyType("Bandit", 45, 12, 35, 45, 2), 15, 2],
    [new EnemyType("Skeleton", 40, 13, 30, 40, 2), 15, 2],
    [new EnemyType("Giant Spider", 38, 14, 32, 28, 2), 15, 2],

    // Level 3 enemies
    [new EnemyType("Orc", 60, 15, 45, 40, 3), 12, 3],
    [new EnemyType("Dark Elf", 55, 18, 48, 45, 3), 12, 3],
    [new EnemyType("Werewolf", 65, 20, 50, 48, 3), 12, 3],

    // Level 4 enemies
    [new EnemyType("Troll", 80, 20, 60, 50, 4), 10, 4],
    [new EnemyType("Ogre", 85, 22, 65, 55, 4), 10, 4],
    [new EnemyType("Gargoyle", 75, 25, 70, 60, 4), 10, 4],

    // Level 5+ special enemies
    [new EnemyType("Dragon Whelp", 100, 30, 100, 100, 5), 5, 5],
    [new EnemyType("Necromancer", 90, 35, 110, 110, 5), 5, 5],
    [new EnemyType("Giant", 120, 28, 120, 120, 5), 5, 5],
  ];

  async function currencyExchange(player) {
    const GOLD_TO_TP_RATE = 10; // 100 gold = 1 tech point
    const TP_TO_GOLD_RATE = 10; // 1 tech point = 100 gold

    while (true) {
      console.log("\n=== Currency Exchange ===");
      console.log(`Gold: ${player.gold}`);
      console.log(`Tech Points: ${player.tech_points}`);
      console.log("\nExchange Rates:");
      console.log(`• ${GOLD_TO_TP_RATE} Gold -> 1 Tech Point`);
      console.log(`• 1 Tech Point -> ${TP_TO_GOLD_RATE} Gold`);
      console.log("\nOptions:");
      console.log("1. Convert Gold to Tech Points");
      console.log("2. Convert Tech Points to Gold");
      console.log("3. Back");

      const choice = await prompt("> ");

      if (choice === "1") {
        const maxConversion = Math.floor(player.gold / GOLD_TO_TP_RATE);
        if (maxConversion < 1) {
          console.log(
            `Not enough gold! You need at least ${GOLD_TO_TP_RATE} gold.`
          );
          continue;
        }

        console.log(`\nYou can convert up to ${maxConversion} tech points`);
        try {
          const amount = parseInt(
            await prompt("How many tech points to buy? (0 to cancel): "),
            10
          );
          if (amount > 0 && amount <= maxConversion) {
            const goldCost = amount * GOLD_TO_TP_RATE;
            player.gold -= goldCost;
            player.tech_points += amount;
            console.log(`Converted ${goldCost} gold to ${amount} tech points!`);
          } else if (amount !== 0) {
            console.log("Invalid amount!");
          }
        } catch (error) {
          console.log("Invalid input!");
        }
      } else if (choice === "2") {
        if (player.tech_points < 1) {
          console.log("Not enough tech points!");
          continue;
        }

        console.log(
          `\nYou can convert up to ${player.tech_points} tech points`
        );
        try {
          const amount = parseInt(
            await prompt("How many tech points to convert? (0 to cancel): "),
            10
          );
          if (amount > 0 && amount <= player.tech_points) {
            const goldGain = amount * TP_TO_GOLD_RATE;
            player.tech_points -= amount;
            player.gold += goldGain;
            console.log(`Converted ${amount} tech points to ${goldGain} gold!`);
          } else if (amount !== 0) {
            console.log("Invalid amount!");
          }
        } catch (error) {
          console.log("Invalid input!");
        }
      } else if (choice === "3") {
        break;
      }
    }
  }

  // Fix enemy spawn logic in main()
  async function main() {
    console.log("Welcome to the Text RPG!");
    console.log("\nChoose your class:");
    console.log("1. Warrior - High HP and defense, strong melee attacks");
    console.log("2. Mage - Powerful spells and high mana");
    console.log("3. Paladin - Balanced stats with healing abilities");
    console.log("4. Necromancer - Dark magic and life drain");
    console.log("5. Assassin - High damage and critical strikes");
    console.log("6. Druid - Nature magic and versatile abilities");
    console.log("7. Monk - Martial arts and meditation");
    console.log("8. Ranger - Skilled archer and animal companion");
    console.log("9. Warlock - Demonic powers and curses");
    console.log("10. Berserker - Rage and powerful attacks");
    console.log("11. Alchemist - Potions and explosives");
    console.log("12. Shaman - Elemental and spiritual magic");

    const name = await prompt("\nEnter your character's name: ");
    let classChoice;
    while (true) {
      classChoice = await prompt("Choose your class (1-12): ");
      if (
        [
          "1",
          "2",
          "3",
          "4",
          "5",
          "6",
          "7",
          "8",
          "9",
          "10",
          "11",
          "12",
        ].includes(classChoice)
      ) {
        break;
      }
      console.log("Invalid choice!");
    }

    const player = new Character(name, classChoice);
    currentPlayer = player;
    console.log(`\nWelcome, ${player.name} the ${player.class_type}!`);

    while (true) {
      // Status display
      console.log(`\n${"=".repeat(50)}`);
      console.log(`${player.name} - Level ${player.level}`);
      console.log(`HP: ${player.health}/${player.maxHealth}`);
      console.log(`MP: ${player.mana}/${player.maxMana}`);
      console.log(
        `EXP: ${player.exp}/${calculateExpRequirement(player.level)}`
      );
      console.log(`Gold: ${player.gold}`);
      console.log(`Current Weapon: ${player.currentWeapon}`);
      console.log(`Current Armor: ${player.currentArmor}`);
      console.log(`${"=".repeat(50)}`);

      // Main menu
      console.log("\nWhat would you like to do?");
      console.log("1. Fight monsters");
      console.log("2. Visit shop");
      console.log("3. Check inventory");
      console.log("4. Rest (Heal 50% HP/MP for 15 gold)");
      console.log("5. Show abilities");
      console.log("6. Visit gadget shop");
      console.log("7. Currency Exchange");
      console.log("8. Visit power shop");
      console.log("9. Quit");

      const choice = await prompt("> ");
      if (choice === "1") {
        const enemies = [];
        let numEnemies = 1;
        if (player.level >= 5) {
          numEnemies = Math.floor(Math.random() * 2) + 2; // Randomly 2 or 3 enemies
        }

        // Fix the enemy spawn loop
        for (let i = 0; i < numEnemies; i++) {
          const roll = Math.random() * 100;
          let cumulative = 0;
          for (const [enemyType, chance, minLevel] of spawnTable) {
            if (player.level >= minLevel) {
              cumulative += chance;
              if (roll <= cumulative) {
                const newEnemy = new Enemy(
                  enemyType.name,
                  enemyType.max_health,
                  enemyType.damage,
                  enemyType.exp_reward,
                  enemyType.gold_reward,
                  enemyType.level
                );
                enemies.push(newEnemy);
                break;
              }
            }
          }
        }

        // Remove duplicate combat call and time.sleep
        if (enemies.length) {
          const result = await combat(player, enemies);
          if (!result) {
            console.log(`\nGame Over! Final Level: ${player.level}`);
            console.log(`Gold collected: ${player.gold}`);
            break;
          }
        } else {
          console.log("\nNo suitable enemies found in this area!");
          console.log("Try exploring a different area or coming back later.");
          // Simulate a delay
          setTimeout(() => {}, 1000);
        }
      } else if (choice === "2") {
        await shop(player);
      } else if (choice === "3") {
        await showInventoryMenu(player);
      } else if (choice === "4") {
        const restCost = 15;
        if (player.gold >= restCost) {
          const healAmount = Math.floor(player.maxHealth / 2);
          const manaAmount = Math.floor(player.maxMana / 2);
          player.health = Math.min(
            player.maxHealth,
            player.health + healAmount
          );
          player.mana = Math.min(player.maxMana, player.mana + manaAmount);
          player.gold -= restCost;
          console.log(
            `Rested and recovered ${healAmount} HP and ${manaAmount} MP!`
          );
        } else {
          console.log("Not enough gold to rest!");
        }
      } else if (choice === "5") {
        showAbilities(player);
      } else if (choice === "6") {
        await gadgetShop(player);
      } else if (choice === "7") {
        await currencyExchange(player);
      } else if (choice === "8") {
        await powerShop(player);
      } else if (choice === "9") {
        const confirm = (
          await prompt("Are you sure you want to quit? (y/n): ")
        ).toLowerCase();
        if (confirm === "y") {
          console.log("Thanks for playing!");
          break;
        }
      }
    }

    if (require.main === module) {
      try {
        main();
      } catch (error) {
        console.log(`\nAn error occurred: ${error}`);
        console.log("Game terminated.");
      }
    }
  }
}
