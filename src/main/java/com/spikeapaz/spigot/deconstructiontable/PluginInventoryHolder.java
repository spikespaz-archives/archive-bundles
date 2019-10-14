package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.PlayerInventory;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.stream.Collectors;


class PluginInventoryHolder implements InventoryHolder {
    private DeconstructionTable plugin = JavaPlugin.getPlugin(DeconstructionTable.class);
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

    public ItemStack getInputItem() {
        return inventory.getItem(11);
    }

    public boolean gridIsPopulated() {
        for (int slot = 0; slot < 27; slot++) {
            if (emptySlots.contains(slot))
                continue;

            if (inventory.getItem(slot) != null)
                return true;
        }

        return false;
    }

    private void showRecipe(ItemStack item) {
        if (item == null) {
            for (int slot = 0; slot < 9; slot++)
                setItemSlot(slot, null);

            return;
        }

        final ItemStack singleItem = item.clone();
        singleItem.setAmount(1);

        if (!Utils.getReversedRecipes().containsKey(singleItem)) {
            showRecipe(null);
            return;
        }

        final ReversedRecipe recipe = Utils.getReversedRecipes().get(singleItem);
        final ArrayList<ItemStack> ingredients = recipe.getOutput(item.getAmount());

        for (int slot = 0; slot < 9; slot++)
            setItemSlot(slot, ingredients.get(slot));
    }

    // Delegate for the event handler that has access to an instance of this class.
    // This is here so that only one event handler for clicks must exist, the rest is just a method here.
    void handleClick(InventoryClickEvent event) {
        if (event.getClickedInventory() == null)
            return;

        final boolean playerInventory = PlayerInventory.class.isAssignableFrom(event.getClickedInventory().getClass());

        ItemStack slotItem = event.getCurrentItem();
        ItemStack cursorItem = event.getCursor();

        if (playerInventory && emptySlots.contains(event.getRawSlot())) {
            event.setCancelled(true);
            return;
        }

        if (event.getRawSlot() == 11) {
            switch (event.getAction()) {
                case PLACE_ALL:
                    if (gridIsPopulated() && slotItem != null && !slotItem.isSimilar(cursorItem)) {
                        event.setCancelled(true);
                        return;
                    }

                    if (slotItem != null && cursorItem != null) {
                        slotItem = slotItem.clone();
                        slotItem.setAmount(slotItem.getAmount() + cursorItem.getAmount());
                    } else if (slotItem == null && cursorItem != null)
                        slotItem = cursorItem.clone();

                    break;
                case PLACE_ONE:
                    if (gridIsPopulated() && slotItem != null && !slotItem.isSimilar(cursorItem)) {
                        event.setCancelled(true);
                        return;
                    }

                    if (slotItem != null && cursorItem != null) {
                        slotItem = slotItem.clone();
                        slotItem.setAmount(slotItem.getAmount() + 1);
                    } else if (slotItem == null && cursorItem != null) {
                        slotItem = cursorItem.clone();
                        slotItem.setAmount(1);
                    }

                    break;
                case SWAP_WITH_CURSOR:
                    if (cursorItem != null)
                        slotItem = cursorItem.clone();

                    break;
                case PICKUP_ALL:
                case COLLECT_TO_CURSOR:
                    slotItem = null;
                    break;
                case PICKUP_ONE:
                case PICKUP_HALF:
                    if (slotItem != null) {
                        slotItem = slotItem.clone();
                        slotItem.setAmount(Math.floorDiv(slotItem.getAmount(), 2));
                    }

                    break;
                default:
                    event.setCancelled(true);
                    Utils.tellConsole("Unsupported inventory action: " + event.getAction().toString());
            }

            showRecipe(slotItem);
            Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
        } else if (playerInventory) {
            switch (event.getAction()) {
                case PLACE_ALL:
                case PLACE_ONE:
                case PLACE_SOME:
                case SWAP_WITH_CURSOR:
                case PICKUP_ALL:
                case PICKUP_ONE:
                case PICKUP_HALF:
                case PICKUP_SOME:
                    break;
                case COLLECT_TO_CURSOR:
                    if (getInputItem() != null && getInputItem().isSimilar(event.getCursor())) {
                        setInputItem(null);
                        Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                    } else {
                        if (cursorItem == null)
                            break;

                        HashMap<ItemStack, ReversedRecipe> reversedRecipes = Utils.getReversedRecipes();
                        ItemStack recipeKey = getInputItem();
                        if (recipeKey == null) break;
                        recipeKey = recipeKey.clone();
                        recipeKey.setAmount(1);

                        if (!reversedRecipes.containsKey(recipeKey))
                            break;

                        ItemStack cursorKey = cursorItem.clone();
                        cursorKey.setAmount(1);

                        if (reversedRecipes.get(recipeKey).getOutput(1).contains(cursorKey)) {
                            setInputItem(null);
                            Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                        }
                    }

                    break;
                case MOVE_TO_OTHER_INVENTORY:
                default:
                    event.setCancelled(true);
                    Utils.tellConsole("Unsupported inventory action: " + event.getAction().toString());
            }
        } else {
            switch (event.getAction()) {
                case PLACE_ALL:
                case PLACE_ONE:
                case PLACE_SOME:
                case SWAP_WITH_CURSOR:
                    event.setCancelled(true);
                    break;
                case PICKUP_ALL:
                case PICKUP_ONE:
                case PICKUP_HALF:
                case PICKUP_SOME:
                case COLLECT_TO_CURSOR:
                case MOVE_TO_OTHER_INVENTORY:
                    setInputItem(null);
                    Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                    break;
                default:
                    event.setCancelled(true);
                    Utils.tellConsole("Unsupported inventory action: " + event.getAction().toString());
            }
        }
    }

    // Delegate for the event handler that has access to an instance of this class.
    // This is here so that only one event handler for drags must exist, the rest is just a method here.
    void handleDrag(InventoryDragEvent event) {
        // We only want to handle the events from OUR inventory, so ignore the event if it's the Player's.
        for (int slot : event.getRawSlots()) {
            Inventory inventory1 = event.getView().getInventory(slot);
            if (inventory1 == null || PlayerInventory.class.isAssignableFrom(inventory1.getClass()))
                return;
        }

        if (event.getRawSlots().size() == 1 && event.getRawSlots().iterator().next() == 11) {
            showCraftingRecipe(event.getNewItems().get(11));
            Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
            return;
        }

        // If the event is within the "crafting grid"
        for (int slot : event.getRawSlots()) {
            if (!emptySlots.contains(slot))
                event.setCancelled(true);
        }
    }

    @Override
    public Inventory getInventory() {
        return inventory;
    }
}
