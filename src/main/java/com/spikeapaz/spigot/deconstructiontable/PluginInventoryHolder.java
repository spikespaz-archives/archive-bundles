package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.event.inventory.InventoryMoveItemEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.PlayerInventory;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.java.JavaPlugin;

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
        inventory = Bukkit.createInventory(this, 27, "Deconstruction");

        populateItems();
    }

    private void populateItems() {
        ItemStack glassPane = new ItemStack(Material.BLACK_STAINED_GLASS_PANE);
        ItemMeta glassPaneMeta = glassPane.getItemMeta();
        assert glassPaneMeta != null;
        glassPaneMeta.setDisplayName("\u00A0");
        glassPane.setItemMeta(glassPaneMeta);

        for (int i : emptySlots)
            inventory.setItem(i, glassPane);

        setInputItem(new ItemStack(Material.GOLDEN_CARROT));

        setItemSlot(0, new ItemStack(Material.GOLD_NUGGET));
        setItemSlot(1, new ItemStack(Material.GOLD_NUGGET));
        setItemSlot(2, new ItemStack(Material.GOLD_NUGGET));
        setItemSlot(3, new ItemStack(Material.GOLD_NUGGET));
        setItemSlot(4, new ItemStack(Material.CARROT));
        setItemSlot(5, new ItemStack(Material.GOLD_NUGGET));
        setItemSlot(6, new ItemStack(Material.GOLD_NUGGET));
        setItemSlot(7, new ItemStack(Material.GOLD_NUGGET));
        setItemSlot(8, new ItemStack(Material.GOLD_NUGGET));
    }

    public void setItemSlot(int slot, ItemStack item) {
        assert slot >= 0 && slot <= 8;

        if (slot > 5)
            slot += 17;
        else if (slot > 2)
            slot += 11;
        else
            slot += 5;

        inventory.setItem(slot, item);
    }

    public void setInputItem(ItemStack item) {
        inventory.setItem(11, item);
    }

    // Delegate for the event handler that has access to an instance of this class.
    // This is here so that only one event handler for clicks must exist, the rest is just a method here.
    void handleClick(InventoryClickEvent event) {
        if (emptySlots.contains(event.getRawSlot())) {
            event.setCancelled(true);
            return;
        }

        switch (event.getAction()) {
            case NOTHING:
            case MOVE_TO_OTHER_INVENTORY:
                return;
            case COLLECT_TO_CURSOR:
            case PICKUP_ALL:
                Bukkit.broadcastMessage("Item has been removed.");
                break;
            case DROP_ALL_CURSOR:
            case DROP_ALL_SLOT:
            case DROP_ONE_CURSOR:
            case DROP_ONE_SLOT:
            case PLACE_ALL:
            case PLACE_ONE:
            case PLACE_SOME:
                if (event.getRawSlot() == 11) {
                    Bukkit.broadcastMessage("Item has been inserted.");
                    return;
                } else
                    event.setCancelled(true);
                break;
            case SWAP_WITH_CURSOR:
                if (event.getRawSlot() == 11) {
                    Bukkit.broadcastMessage("Swapped with cursor.");
                    return;
                } else
                    event.setCancelled(true);
                break;
            case UNKNOWN:
                Utils.tellConsole("Unknown inventory action.");
                break;
            default:
                Bukkit.broadcastMessage(event.getAction().toString());
                event.setCancelled(true);
        }
    }

    // Delegate for the event handler that has access to an instance of this class.
    // This is here so that only one event handler for drags must exist, the rest is just a method here.
    void handleDrag(InventoryDragEvent event) {
//        final ArrayList<ItemStack> items = new ArrayList<>(event.getNewItems().values());
//
//        boolean blankChanged = false;
//        for (int slot : event.getRawSlots()) {
//            blankChanged = (slot >= 1 && slot <= 4) || (slot >= 9 && slot <= 12) || blankChanged;
//        }
//
//        if (blankChanged) {
//            event.setCancelled(true);
//            return;
//        }
//
//        final ItemStack cursor = event.getCursor();
//
//        Bukkit.broadcastMessage("Drag Event!");
//
//        if (cursor == null) {
//            Bukkit.broadcastMessage("Cursor is null.");
//            return;
//        }
//        else if (cursor.getType().equals(Material.AIR) && items.size() > 0) {
//            // Player has put an item in the inventory
//            Bukkit.broadcastMessage("Player has put an item in the inventory.");
//        }
//        else if (cursor.getType().equals(Material.AIR) && items.size() == 0) {
//            // Player has taken an item
//            Bukkit.broadcastMessage("Player has taken an item.");
//        }
//        else if (!cursor.getType().equals(Material.AIR) && items.size() > 0) {
//            // Player has swapped an item for another
//            Bukkit.broadcastMessage("Player has swapped an item for another.");
//        }
//
//        Bukkit.broadcastMessage("Cursor: " + cursor.getType().toString());
//        ArrayList<String> slottedItems = items.stream().map(item -> item.getItemMeta().getDisplayName()).collect(Collectors.toCollection(ArrayList::new));
//        Bukkit.broadcastMessage("Slot: " + String.join(", ", slottedItems));
    }

    // Delegate for the event handler that has access to an instance of this class.
    // This is here so that only one event handler for moves must exist, the rest is just a method here.
    void handleMove(InventoryMoveItemEvent event) {
        InventoryHolder baseSource = event.getSource().getHolder();
        InventoryHolder baseDestination = event.getDestination().getHolder();
        if (baseSource == null || baseDestination == null) return;

//        if (PluginInventoryHolder.class.isAssignableFrom(baseSource.getClass()))
//            return;
//        else if (PluginInventoryHolder.class.isAssignableFrom(baseDestination.getClass()))
//            if (event.getItem())
    }

    @Override
    public Inventory getInventory() {
        return inventory;
    }
}
