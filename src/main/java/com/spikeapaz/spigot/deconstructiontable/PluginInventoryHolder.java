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
import org.bukkit.plugin.java.JavaPlugin;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;


class PluginInventoryHolder implements InventoryHolder {
    private DeconstructionTable plugin = JavaPlugin.getPlugin(DeconstructionTable.class);
    private ArrayList<ItemStack> virtualStorage = new ArrayList<>();
    private Inventory inventory;

    //      0 1 2 3 4 5 6 7 8
    //
    // +0   X X X X X 0 0 0 X
    // +8   X X 0 X X 0 0 0 X
    // +18  X X X X X 0 0 0 X
    private int[] emptySlotsIntArray = {
            0 + 0,
            0 + 1,
            0 + 2,
            0 + 3,
            0 + 4,
            0 + 8,
            9 + 0,
            9 + 1,
            9 + 3,
            9 + 4,
            9 + 8,
            18 + 0,
            18 + 1,
            18 + 2,
            18 + 3,
            18 + 4,
            18 + 8
    };
    private ArrayList<Integer> emptySlots = new ArrayList<>(Arrays.stream(emptySlotsIntArray).boxed().collect(Collectors.toList()));

    PluginInventoryHolder() {
        inventory = plugin.getServer().createInventory(this, 27, "Deconstruction");

        populateItems();
    }

    private void populateItems() {
        ItemStack glassPane = new ItemStack(Material.BLACK_STAINED_GLASS_PANE);
        ItemMeta glassPaneMeta = glassPane.getItemMeta();
        assert glassPaneMeta != null;
        glassPaneMeta.setDisplayName(Character.toString((char) 0xE2));
        glassPane.setItemMeta(glassPaneMeta);

        for (int i : emptySlots)
            inventory.setItem(i, glassPane);
    }

    public void setItemSlot(int slot, ItemStack item) {
        if (slot >= 0 && slot <= 2)
            slot += 5;
        if (slot >= 3 && slot <= 5)
            slot += 9;
        if (slot >= 6 && slot <= 8)
            slot += 17;

        inventory.setItem(slot, item);
        virtualStorage.remove(item);
    }

    void handleClick(InventoryClickEvent event) {
        Bukkit.broadcastMessage("Click Event!");

        if (event.getClickedInventory() == null)
            return;

        final ItemStack item = event.getCurrentItem();
        if (item == null) return;
        final ItemMeta meta = item.getItemMeta();
        if (meta == null) return;

        if (emptySlots.contains(event.getRawSlot())) {
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

    void handleDrag(InventoryDragEvent event) {
        Bukkit.broadcastMessage("Drag Event!");

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

    @Override
    public @NotNull Inventory getInventory() {
        return inventory;
    }
}
