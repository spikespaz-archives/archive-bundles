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
        final ItemStack glassPane = new ItemStack(Material.BLACK_STAINED_GLASS_PANE);
        final ItemMeta glassPaneMeta = glassPane.getItemMeta();
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
        assert event.getClickedInventory() != null;

        // We only want to handle the events from OUR inventory, so ignore the event if it's the Player's.
        if (PlayerInventory.class.isAssignableFrom(event.getClickedInventory().getClass()))
            return;

        // If the event is within the "crafting grid"
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

        // We only want to handle the events from OUR inventory, so ignore the event if it's the Player's.
        for (int slot : event.getRawSlots()) {
            Inventory inventory1 = event.getView().getInventory(slot);
            if (inventory1 == null || PlayerInventory.class.isAssignableFrom(inventory1.getClass()))
                return;
        }

        if (event.getRawSlots().size() == 1 && event.getRawSlots().iterator().next() == 11)
            return;

        Bukkit.broadcastMessage("It's our event!");

        // If the event is within the "crafting grid"
        for (int slot : event.getRawSlots()) {
            if (!emptySlots.contains(slot)) {
                event.setCancelled(true);
                Bukkit.broadcastMessage("It's our in the grid!");
            }
        }
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
