package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.Plugin;
import org.jetbrains.annotations.NotNull;


class PluginInventoryHolder implements InventoryHolder, Listener {
    private Plugin plugin = DeconstructionTable.getPlugin(DeconstructionTable.class);
    private Inventory inventory;

    PluginInventoryHolder() {
        inventory = plugin.getServer().createInventory(this, 18, "Deconstruction");
        plugin.getServer().getPluginManager().registerEvents(this, plugin);

        populateItems();
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

    public void setItemSlot(int slot, ItemStack item) {
        if (slot < 3)
            slot += 5;

        if (slot > 4)
            slot += 13;

        inventory.setItem(slot, item);
    }

    @EventHandler
    void onInventoryClickEvent(InventoryClickEvent event) {
        if (event.getClickedInventory() == null)
            return;

        org.bukkit.inventory.InventoryHolder holder = event.getClickedInventory().getHolder();

        if (holder != null && holder.getClass().isInstance(this)) {
            ItemStack item = event.getCurrentItem();
            if (item == null) return;
            ItemMeta meta = item.getItemMeta();
            if (meta == null) return;

            Bukkit.broadcastMessage(meta.getDisplayName());

            if ((event.getRawSlot() >= 1 && event.getRawSlot() <= 4) || (event.getRawSlot() >= 9 && event.getRawSlot() <= 12))
                event.setCancelled(true);
        }
    }

    @Override
    public @NotNull Inventory getInventory() {
        return inventory;
    }

    void handleClick(InventoryClickEvent event) {}
}
