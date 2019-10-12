package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.Plugin;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.stream.Collectors;


class PluginInventoryHolder implements InventoryHolder, Listener {
    private Plugin plugin = DeconstructionTable.getPlugin(DeconstructionTable.class);
    private ArrayList<ItemStack> virtualStorage = new ArrayList<>();
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
        virtualStorage.remove(item);
    }

    @EventHandler
    void onInventoryClickEvent(InventoryClickEvent event) {
        if (event.getClickedInventory() == null)
            return;

        InventoryHolder holder = event.getClickedInventory().getHolder();

        if (holder != null && holder.getClass().isInstance(this)) {
            final ItemStack item = event.getCurrentItem();
            if (item == null) return;
            final ItemMeta meta = item.getItemMeta();
            if (meta == null) return;

            if ((event.getRawSlot() >= 1 && event.getRawSlot() <= 4) || (event.getRawSlot() >= 9 && event.getRawSlot() <= 12)) {
                event.setCancelled(true);
                return;
            }

            final ItemStack cursor = event.getCursor();

            if (cursor == null) {
                Bukkit.broadcastMessage("Cursor is null.");
                return;
            }
            else if (cursor.getType().equals(Material.AIR) && !item.getType().equals(Material.AIR)) {
                // Player has put an item in the inventory
                Bukkit.broadcastMessage("Player has put an item in the inventory.");
            }
            else if (cursor.getType().equals(Material.AIR) && !item.getType().equals(Material.AIR)) {
                // Player has taken an item
                Bukkit.broadcastMessage("Player has taken an item.");
            }
            else if (!cursor.getType().equals(Material.AIR) && !item.getType().equals(Material.AIR)) {
                // Player has swapped an item for another
                Bukkit.broadcastMessage("Player has swapped an item for another.");
            }

            Bukkit.broadcastMessage("Cursor: " + cursor.getType().toString());
            Bukkit.broadcastMessage("Slot: " + item.getType().toString());
        }
    }

    @EventHandler
    void onInventoryDragEvent(InventoryDragEvent event) {
        Bukkit.broadcastMessage("Drag Event!");
        InventoryHolder holder = event.getInventory().getHolder();

        if (holder != null && holder.getClass().isInstance(this)) {
            final ArrayList<ItemStack> items = new ArrayList<>(event.getNewItems().values());

            boolean blankChanged = false;
            for (int slot : event.getRawSlots()) {
                blankChanged = (slot >= 1 && slot <= 4) || (slot >= 9 && slot <= 12) || blankChanged;
            }

            if (blankChanged) {
                event.setCancelled(true);
                return;
            }

            final ItemStack cursor = event.getCursor();

            if (cursor == null) {
                Bukkit.broadcastMessage("Cursor is null.");
                return;
            }
            else if (cursor.getType().equals(Material.AIR) && items.size() > 0) {
                // Player has put an item in the inventory
                Bukkit.broadcastMessage("Player has put an item in the inventory.");
            }
            else if (cursor.getType().equals(Material.AIR) && items.size() == 0) {
                // Player has taken an item
                Bukkit.broadcastMessage("Player has taken an item.");
            }
            else if (!cursor.getType().equals(Material.AIR) && items.size() > 0) {
                // Player has swapped an item for another
                Bukkit.broadcastMessage("Player has swapped an item for another.");
            }

            Bukkit.broadcastMessage("Cursor: " + cursor.getType().toString());
            ArrayList<String> slottedItems = items.stream().map(item -> item.getItemMeta().getDisplayName()).collect(Collectors.toCollection(ArrayList::new));
            Bukkit.broadcastMessage("Slot: " + String.join(", ", slottedItems));
        }
    }

    @Override
    public @NotNull Inventory getInventory() {
        return inventory;
    }

    void handleClick(InventoryClickEvent event) {}
}
