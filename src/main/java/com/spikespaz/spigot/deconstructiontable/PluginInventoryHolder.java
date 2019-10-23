package com.spikespaz.spigot.deconstructiontable;

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


class PluginInventoryHolder implements InventoryHolder {
    private final DeconstructionTable plugin = JavaPlugin.getPlugin(DeconstructionTable.class);
    private Inventory inventory;
    private int recipeIndex;
    private ReversedRecipe currentRecipe;

    // Here is an example grid. The slot number is the X coordinate plus the Y offset.
    //      0 1 2 3 4 5 6 7 8
    //
    // +0   X X X X X 0 0 0 X
    // +8   X X 0 X X 0 0 0 X
    // +18  X X X X X 0 0 0 X

    // These are the empty slots to be filled with glass panes
    private final ArrayList<Integer> emptySlots = new ArrayList<>(Arrays.asList(
            0 + 0,
            0 + 1,
            0 + 2,
            0 + 3,
            0 + 4,
            9 + 0,
            9 + 1,
            9 + 3,
            9 + 4,
            9 + 8,
            18 + 0,
            18 + 1,
            18 + 2,
            18 + 3,
            18 + 4
    ));
    // The 9x9 grid used to show the result of the reversed recipe
    private final ArrayList<Integer> outputSlots = new ArrayList<>(Arrays.asList(
            5 + 0,
            5 + 1,
            5 + 2,
            14 + 0,
            14 + 1,
            14 + 2,
            23 + 0,
            23 + 1,
            23 + 2
    ));
    private final int greenSlot = 8;
    private final int redSlot = 26;
    // Number of the input item slot
    private final int inputSlotNum = 11;

    PluginInventoryHolder() {
        inventory = Bukkit.createInventory(this, 27, "Deconstruction");
        recipeIndex = 0;

        populateItems();
    }

    // Populate blank slots with glass panes with no name
    private void populateItems() {
        ItemStack glassPane = new ItemStack(Material.BLACK_STAINED_GLASS_PANE);
        ItemMeta glassPaneMeta = glassPane.getItemMeta();
        assert glassPaneMeta != null;
        glassPaneMeta.setDisplayName("\u00A0");
        glassPane.setItemMeta(glassPaneMeta);

        for (int slot : emptySlots)
            inventory.setItem(slot, glassPane);

        glassPane = new ItemStack(Material.GREEN_STAINED_GLASS_PANE);
        glassPaneMeta = glassPane.getItemMeta();
        assert glassPaneMeta != null;
        glassPaneMeta.setDisplayName("FORWARD");
        glassPane.setItemMeta(glassPaneMeta);

        inventory.setItem(greenSlot, glassPane);

        glassPane = new ItemStack(Material.RED_STAINED_GLASS_PANE);
        glassPaneMeta = glassPane.getItemMeta();
        assert glassPaneMeta != null;
        glassPaneMeta.setDisplayName("BACKWARD");
        glassPane.setItemMeta(glassPaneMeta);

        inventory.setItem(redSlot, glassPane);
    }

    // Set one of the output/crafting slots (index 0-8) to an item
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

    // Get the current item in the input slot
    public ItemStack getInputItem() {
        return inventory.getItem(inputSlotNum);
    }

    // Sets the input slot's item (slot 11)
    public void setInputItem(ItemStack item) {
        inventory.setItem(inputSlotNum, item);
    }

    // Checks if any of the output slots have items in them
    public boolean outputIsShown() {
        for (int slot : outputSlots)
            if (inventory.getItem(slot) != null || (inventory.getItem(slot) != null && inventory.getItem(slot).getType().equals(Material.AIR)))
                return true;

        return false;
    }

    // Checks if any of the output slots have items in them
    public boolean outputHasItem(ItemStack item) {
        for (int slot : outputSlots) {
            ItemStack slotItem = inventory.getItem(slot);

            if (slotItem == null)
                continue;

            if (slotItem.isSimilar(item))
                return true;
        }

        return false;
    }

    // Show the reversed recipe in the output slots for an item
    private void showRecipe(ItemStack item) {
        if (item == null) {
            for (int slot = 0; slot < 9; slot++)
                setItemSlot(slot, null);

            recipeIndex = 0;
            currentRecipe = null;
            return;
        }


        // The current recipe isn't populated. Should probably make sure the input
        // items are the same but not for now because I want to catch bugs.
        if (currentRecipe == null) {
            Utils.tellConsole("Looking up recipe for item: " + item.getType());

            ItemStack keyItem = item.clone();
            keyItem.setAmount(1);

            if (!Utils.getReversedRecipes().containsKey(keyItem))
                return;

            currentRecipe = Utils.getReversedRecipes().get(keyItem);
        }

        ArrayList<ItemStack> ingredients = currentRecipe.getOutput(recipeIndex, item.getAmount());

        int slot = 0;
        for (ItemStack ingredient : ingredients) {
            setItemSlot(slot, ingredient);
            slot++;
        }
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

        if (event.getRawSlot() == inputSlotNum) {
            // This is the input slot branch for inventory actions
            switch (event.getAction()) {
                case CLONE_STACK: // Creative mode only, let the default happen
                    break;
                case PLACE_ALL:
                    // Prevent the player from updating the input slot if the crafting output is partially removed
                    if (outputIsShown() && slotItem != null && !slotItem.isSimilar(cursorItem)) {
                        event.setCancelled(true);
                        return;
                    }

                    // All of the items on the cursor match the input item and were placed in that slot
                    if (slotItem != null && cursorItem != null) {
                        slotItem = slotItem.clone();
                        slotItem.setAmount(slotItem.getAmount() + cursorItem.getAmount());
                    } else if (slotItem == null && cursorItem != null)
                        // There was nothing in the input slot before.
                        slotItem = cursorItem.clone();

                    break;
                case PLACE_ONE:
                    // Prevent the player from updating the input slot if the crafting output is partially removed
                    if (outputIsShown() && slotItem != null && !slotItem.isSimilar(cursorItem)) {
                        event.setCancelled(true);
                        return;
                    }

                    // A single item of the same type has been placed
                    if (slotItem != null && cursorItem != null) {
                        slotItem = slotItem.clone();
                        slotItem.setAmount(slotItem.getAmount() + 1);
                    } else if (slotItem == null && cursorItem != null) {
                        // A single item has been placed where there wasn't anything before
                        slotItem = cursorItem.clone();
                        slotItem.setAmount(1);
                    }

                    break;
                case SWAP_WITH_CURSOR:
                    // The cursor item should never be null if this action is called. Update the grid according to the cursor item
                    if (cursorItem != null)
                        slotItem = cursorItem.clone();

                    break;
                case PICKUP_ALL:
                case COLLECT_TO_CURSOR:
                    // Clear the crafting grid by setting the slot's item to null
                    slotItem = null;
                    break;
                case PICKUP_ONE:
                    // Update the slot item to be one less than the previous amount
                    if (slotItem != null) {
                        slotItem = slotItem.clone();
                        slotItem.setAmount(slotItem.getAmount() - 1);
                    }

                    break;
                case PICKUP_HALF:
                    // Update the slot item to be half of the previous amount
                    if (slotItem != null) {
                        slotItem = slotItem.clone();
                        slotItem.setAmount(Math.floorDiv(slotItem.getAmount(), 2));
                    }

                    break;
                default:
                    // We don't know what happened so to prevent item duping, go nuclear
                    event.setCancelled(true);
                    Utils.tellConsole("Unsupported inventory action: " + event.getAction().toString());
            }

            showRecipe(slotItem);
            Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
        } else if (playerInventory) {
            switch (event.getAction()) {
                case CLONE_STACK:
                case PLACE_ALL:
                case PLACE_ONE:
                case PLACE_SOME:
                case SWAP_WITH_CURSOR:
                case PICKUP_ALL:
                case PICKUP_ONE:
                case PICKUP_HALF:
                case PICKUP_SOME:
                    break; // We don't want to change very much in the player's inventory so just use the default for these actions.
                case COLLECT_TO_CURSOR:
                    // If this happens within the player inventory we want to clear
                    // the grid if the item picked up matches the input item
                    if (getInputItem() != null && getInputItem().isSimilar(event.getCursor())) {
                        showRecipe(null);
                        Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                    } else {
                        // Otherwise we need to remove the input item if the shown recipe in the grid includes the item collected
                        // If the cursor item doesn't exist I don't know what the hell happened so just return
                        if (cursorItem == null)
                            break;

                        // If the output has an item that matches according to ItemStack.isSimilar,
                        // it will be picked up so clear the input slot.
                        if (outputHasItem(cursorItem)) {
                            setInputItem(null);
                            Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                        }
                    }

                    break;
                case MOVE_TO_OTHER_INVENTORY:
                    // Disallow because items could be transferred to the output slots
                default:
                    // We don't know what happened so to prevent item duping, go nuclear
                    event.setCancelled(true);
                    Utils.tellConsole("Unsupported inventory action: " + event.getAction().toString());
            }
        } else {
            switch (event.getAction()) {
                case CLONE_STACK:
                    break;
                case PLACE_ALL:
                case PLACE_ONE:
                case PLACE_SOME:
                case SWAP_WITH_CURSOR:
                    // Any valid place actions are already handled by the first switch. Now it's guaranteed to be within the blank slots
                    event.setCancelled(true);
                    break;
                case PICKUP_ALL:
                case PICKUP_ONE:
                case PICKUP_HALF:
                case PICKUP_SOME:
                case COLLECT_TO_CURSOR:
                case MOVE_TO_OTHER_INVENTORY:
                    // Stop the glass panes in the empty slots from being picked up
                    if (emptySlots.contains(event.getRawSlot())) {
                        event.setCancelled(true);
                        Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                        break;
                    } else if (event.getRawSlot() == greenSlot) {
                        event.setCancelled(true);
                        if (currentRecipe != null)
                            if (recipeIndex + 1 > currentRecipe.choiceCount() - 1)
                                recipeIndex = 0;
                            else
                                recipeIndex++;
                        showRecipe(getInputItem());
                        Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                        break;
                    } else if (event.getRawSlot() == redSlot) {
                        event.setCancelled(true);
                        if (currentRecipe != null)
                            if (recipeIndex - 1 < 0)
                                recipeIndex = currentRecipe.choiceCount() - 1;
                            else
                                recipeIndex--;
                        showRecipe(getInputItem());
                        Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                        break;
                    }

                    // If it isn't an empty slot it's something in the crafting grid. Hide the input item.
                    setInputItem(null);
                    Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                    break;
                default:
                    // We don't know what happened so to prevent item duping, go nuclear
                    event.setCancelled(true);
                    Utils.tellConsole("Unsupported inventory action: " + event.getAction().toString());
            }
        }
    }

    // Delegate for the event handler that has access to an instance of this class.
    // This is here so that only one event handler for drags must exist, the rest is just a method here.
    void handleDrag(InventoryDragEvent event) {
        boolean inputSlotChanged = false;
        boolean playerSlotsChanged = false;
        boolean outputSlotsChanged = false;
        boolean ownSlotsChanged = false;

        // Run a check for every item slot in the event, setting the flags above accordingly
        for (int slot : event.getRawSlots()) {
            Inventory inventory1 = event.getView().getInventory(slot);

            if (inventory1 == null)
                return;

            inputSlotChanged = inputSlotChanged || slot == inputSlotNum;
            playerSlotsChanged = playerSlotsChanged || PlayerInventory.class.isAssignableFrom(inventory1.getClass());
            ownSlotsChanged = ownSlotsChanged || !PlayerInventory.class.isAssignableFrom(inventory1.getClass());
            outputSlotsChanged = outputSlotsChanged || outputSlots.contains(slot);
        }

        ItemStack inputItem = getInputItem();

        if (outputSlotsChanged) // Don't allow changing the output slots
            event.setCancelled(true);
        else if (inputSlotChanged && playerSlotsChanged && inputItem == null) {
            // The original ItemStack is divided among player slots and the input slot, and the input slot was empty, update the recipe to the new amount
            showRecipe(event.getNewItems().get(inputSlotNum).clone());
            Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
        } else if (inputSlotChanged && playerSlotsChanged) {
            // Divided among player slots and the input slot, but there was something in the input before. Update recipe for new amount.
            inputItem = inputItem.clone();
            inputItem.setAmount(event.getNewItems().get(inputSlotNum).getAmount());
            showRecipe(inputItem);
            Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
        } else if (inputSlotChanged) {
            showRecipe(event.getNewItems().get(inputSlotNum));
            Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
        }
    }

    // Get the inventory that  the handler is responsible for
    @Override
    public Inventory getInventory() {
        return inventory;
    }
}
