class PageManager {
  constructor() {
    this.currentPage = "characterCreation";
    this.pages = {
      characterCreation: document.getElementById("characterCreation"),
      gameInterface: document.getElementById("gameInterface"),
      combatInterface: document.createElement("div"),
      shopInterface: document.createElement("div"),
      inventoryInterface: document.createElement("div"),
    };

    this.setupInterfaces();
  }

  setupInterfaces() {
    // Setup Combat Interface
    this.pages.combatInterface.id = "combatInterface";
    this.pages.combatInterface.className = "hidden";
    this.pages.combatInterface.innerHTML = `
            <div class="combat-status"></div>
            <div class="enemy-list"></div>
            <div class="combat-actions">
                <button type="button" onclick="handleCombatAction('attack')">Attack</button>
                <button type="button" onclick="handleCombatAction('ability')">Use Ability</button>
                <button type="button" onclick="handleCombatAction('item')">Use Item</button>
                <button type="button" onclick="handleCombatAction('gadget')">Use Gadget</button>
                <button type="button" onclick="handleCombatAction('flee')">Flee</button>
            </div>
        `;

    // Setup Shop Interface
    this.pages.shopInterface.id = "shopInterface";
    this.pages.shopInterface.className = "hidden";
    this.pages.shopInterface.innerHTML = `
            <div class="shop-inventory"></div>
            <div class="player-gold"></div>
            <div class="shop-actions">
                <button type="button" onclick="handleShopAction('buy')">Buy</button>
                <button type="button" onclick="handleShopAction('sell')">Sell</button>
                <button type="button" onclick="handleShopAction('exit')">Exit Shop</button>
            </div>
        `;

    // Add interfaces to container
    const container = document.getElementById("gameContainer");
    container.appendChild(this.pages.combatInterface);
    container.appendChild(this.pages.shopInterface);
  }

  showPage(pageName) {
    if (!Object.keys(this.pages).includes(pageName)) return false;

    // Hide all pages
    Object.values(this.pages).forEach((page) => {
      if (page) page.classList.add("hidden");
    });

    // Show requested page
    const page = this.pages[pageName];
    if (page) {
      page.classList.remove("hidden");
      this.currentPage = pageName;
      return true;
    }
    return false;
  }

  getCurrentPage() {
    return this.currentPage;
  }
}
