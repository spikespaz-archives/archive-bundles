package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.Plugin;
import org.jetbrains.annotations.NotNull;

class CustomInventory implements InventoryHolder, Listener {
    private Plugin plugin = DeconstructionTable.getPlugin(DeconstructionTable.class);
    private Inventory inventory;

    CustomInventory() {
        inventory = plugin.getServer().createInventory(this, 18, "Deconstruction");
        plugin.getServer().getPluginManager().registerEvents(this, plugin);

        populateItems();
    }

    @Override
    public @NotNull Inventory getInventory() {
        return inventory;
    }

    public void populateItems() {
        ItemStack glassPane = new ItemStack(Material.BLACK_STAINED_GLASS_PANE);

        inventory.setItem(1, glassPane);
        inventory.setItem(2, glassPane);
        inventory.setItem(3, glassPane);
        inventory.setItem(4, glassPane);
        inventory.setItem(9, glassPane);
        inventory.setItem(10, glassPane);
        inventory.setItem(11, glassPane);
        inventory.setItem(12, glassPane);
    }

    @EventHandler
    void onInventoryClickEvent(InventoryClickEvent event) {
        assert event.getClickedInventory() != null;
        InventoryHolder holder = event.getClickedInventory().getHolder();
        if (holder != null && event.getClickedInventory().getHolder().getClass().isInstance(this))
            event.setCancelled(true);
    }
}
