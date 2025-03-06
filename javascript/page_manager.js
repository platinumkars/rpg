class PageManager {
  constructor() {
    this.currentPage = "characterCreation";
    this.setupInterfaces();
    this.addGlobalEventListeners();
  }

  setupInterfaces() {
    // Create base container
    this.container = document.getElementById("gameContainer");
    if (!this.container) {
      this.container = document.createElement("div");
      this.container.id = "gameContainer";
      document.body.appendChild(this.container);
    }

    // Define interfaces
    this.interfaces = {
      characterCreation: this.createCharacterCreation(),
      gameInterface: this.createGameInterface(),
      combatInterface: this.createCombatInterface(),
      shopInterface: this.createShopInterface(),
    };

    // Add interfaces to container
    Object.values(this.interfaces).forEach((interface) => {
      this.container.appendChild(interface);
    });

    // Show initial page
    this.showPage("characterCreation");
  }

  addGlobalEventListeners() {
    // Handle ESC key for menu return
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.currentPage !== "characterCreation") {
        this.showPage("gameInterface");
      }
    });

    // Add button feedback effects
    document.addEventListener("click", (e) => {
      if (e.target.matches("button:not(:disabled)")) {
        this.addButtonFeedback(e.target);
      }
    });
  }

  addButtonFeedback(button) {
    button.style.transform = "scale(0.95)";
    setTimeout(() => {
      button.style.transform = "";
    }, 100);
  }

  createCharacterCreation() {
    const div = document.createElement("div");
    div.id = "characterCreation";
    div.className = "interface-section";
    div.innerHTML = `
      <h2>Create Your Character</h2>
      <input type="text" 
        id="characterName" 
        placeholder="Enter character name"
        maxlength="20"
        required>
      <select id="classChoice" required>
        <option value="">Select a class...</option>
        <option value="1">Warrior - High HP and defense</option>
        <option value="2">Mage - Powerful spells and high mana</option>
        <option value="3">Paladin - Balanced stats with healing</option>
        <option value="4">Necromancer - Dark magic and life drain</option>
        <option value="5">Assassin - High damage and critical strikes</option>
        <option value="6">Druid - Nature magic and versatile abilities</option>
        <option value="7">Monk - Martial arts and meditation</option>
        <option value="8">Ranger - Skilled archer and animal companion</option>
        <option value="9">Warlock - Demonic powers and curses</option>
        <option value="10">Berserker - Rage and powerful attacks</option>
        <option value="11">Alchemist - Potions and explosives</option>
        <option value="12">Shaman - Elemental and spiritual magic</option>
      </select>
      <button id="startButton" onclick="createCharacter()" disabled>Start Game</button>
    `;

    // Add input validation
    const nameInput = div.querySelector("#characterName");
    const classSelect = div.querySelector("#classChoice");
    const startButton = div.querySelector("#startButton");

    const validateForm = () => {
      const isValid = nameInput.value.trim() && classSelect.value;
      startButton.disabled = !isValid;
    };

    nameInput.addEventListener("input", validateForm);
    classSelect.addEventListener("change", validateForm);

    return div;
  }

  createGameInterface() {
    const div = document.createElement("div");
    div.id = "gameInterface";
    div.className = "interface-section hidden";
    div.innerHTML = `
      <div id="playerStats"></div>
      <div id="gameOutput"></div>
      <div class="control-section">
        <div class="button-grid">
          <button class="game-button" data-command="1">Fight</button>
          <button class="game-button" data-command="2">Shop</button>
          <button class="game-button" data-command="3">Inventory</button>
          <button class="game-button" data-command="4">Rest</button>
          <button class="game-button" data-command="5">Abilities</button>
          <button class="game-button" data-command="6">Gadgets</button>
          <button class="game-button" data-command="7">Exchange</button>
          <button class="game-button" data-command="8">Powers</button>
          <button class="game-button" data-command="9">Quit</button>
        </div>
      </div>
    `;

    // Add button event listeners
    div.querySelectorAll(".game-button").forEach((button) => {
      button.addEventListener("click", () => {
        if (!button.disabled) {
          handleCommand(button.dataset.command);
        }
      });
    });

    return div;
  }

  createCombatInterface() {
    const div = document.createElement("div");
    div.id = "combatInterface";
    div.className = "interface-section hidden";
    div.innerHTML = `
      <div class="combat-status"></div>
      <div class="enemy-list"></div>
      <div class="combat-actions">
        <button onclick="handleCombatAction('attack')">Attack</button>
        <button onclick="handleCombatAction('ability')">Use Ability</button>
        <button onclick="handleCombatAction('item')">Use Item</button>
        <button onclick="handleCombatAction('gadget')">Use Gadget</button>
        <button onclick="handleCombatAction('flee')">Flee</button>
      </div>
    `;
    return div;
  }

  createShopInterface() {
    const div = document.createElement("div");
    div.id = "shopInterface";
    div.className = "interface-section hidden";
    div.innerHTML = `
      <div class="shop-inventory"></div>
      <div class="player-gold"></div>
      <div class="shop-actions">
        <button onclick="handleShopAction('buy')">Buy</button>
        <button onclick="handleShopAction('sell')">Sell</button>
        <button onclick="handleShopAction('exit')">Exit Shop</button>
      </div>
    `;
    return div;
  }

  showPage(pageName) {
    if (!this.interfaces[pageName]) return false;

    // Disable buttons during transition
    const buttons = document.querySelectorAll("button");
    buttons.forEach((btn) => (btn.disabled = true));

    // Hide all pages
    Object.values(this.interfaces).forEach((interface) => {
      interface.classList.add("hidden");
    });

    // Show requested page
    this.interfaces[pageName].classList.remove("hidden");
    this.currentPage = pageName;

    // Re-enable buttons
    setTimeout(() => {
      buttons.forEach((btn) => (btn.disabled = false));
    }, 100);

    return true;
  }

  getCurrentPage() {
    return this.currentPage;
  }

  updateInterface(pageName, data) {
    const interface = this.interfaces[pageName];
    if (!interface) return;

    switch (pageName) {
      case "combatInterface":
        interface.querySelector(".combat-status").textContent = data.status;
        interface.querySelector(".enemy-list").innerHTML = data.enemies;
        break;
      case "shopInterface":
        interface.querySelector(".shop-inventory").innerHTML = data.inventory;
        interface.querySelector(".player-gold").textContent = data.gold;
        break;
    }
  }
}
