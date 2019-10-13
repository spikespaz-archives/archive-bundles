package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.inventory.*;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.ListIterator;
import java.util.Map;
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

    private void showCraftingRecipe(ItemStack item) {
        if (item == null)
            return;

        if (!Utils.getReversedRecipes().containsKey(item))
            return;

        Recipe baseRecipe = Utils.getReversedRecipes().get(item);

        if (ShapedRecipe.class.isAssignableFrom(baseRecipe.getClass())) {
            ShapedRecipe recipe = (ShapedRecipe) baseRecipe;
            Map<Character, ItemStack> ingredientMap = recipe.getIngredientMap();

            int rowNum = 0;
            for (String row : recipe.getShape()) {
                int colNum = 0;
                for (char c : row.toCharArray()) {
                    if (rowNum == 0)
                        setItemSlot(colNum, ingredientMap.get(c));
                    else if (rowNum == 1)
                        setItemSlot(colNum + 3, ingredientMap.get(c));
                    else if (rowNum == 2)
                        setItemSlot(colNum + 6, ingredientMap.get(c));

                    colNum++;
                }
                rowNum++;
            }
        } else if (ShapelessRecipe.class.isAssignableFrom(baseRecipe.getClass())) {
            ShapelessRecipe recipe = (ShapelessRecipe) baseRecipe;

            final ListIterator<ItemStack> itemList = new ArrayList<>(recipe.getIngredientList()).listIterator();

            for (int c = 0; c < 8; c++) {
                if (itemList.hasNext())
                    setItemSlot(c, itemList.next());
                else
                    setItemSlot(c, null);
            }
        }
    }

    public void clearCraftingRecipe() {
        for (int slot = 0; slot < 8; slot++)
            setItemSlot(slot, null);
    }

    // Delegate for the event handler that has access to an instance of this class.
    // This is here so that only one event handler for clicks must exist, the rest is just a method here.
    void handleClick(InventoryClickEvent event) {
        if (event.getClickedInventory() == null)
            return;

        // We only want to handle the events from OUR inventory, so ignore the event if it's the Player's.
        if (PlayerInventory.class.isAssignableFrom(event.getClickedInventory().getClass())) {
            // If the event is within the "crafting grid"
            if (event.isShiftClick())
                event.setCancelled(true);

            return;
        }

        // If the event is within the "crafting grid"
        if (emptySlots.contains(event.getRawSlot())) {
            event.setCancelled(true);
            return;
        }

        switch (event.getAction()) {
            case PLACE_ALL:
            case PLACE_ONE:
            case PLACE_SOME:
            case SWAP_WITH_CURSOR:
                if (event.getRawSlot() == 11 && event.getCursor() != null) {
                    showCraftingRecipe(event.getCursor());
                    Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                    return;
                } else
                    event.setCancelled(true);
                break;
            case PICKUP_ALL:
            case PICKUP_ONE:
            case PICKUP_SOME:
            case PICKUP_HALF:
            case COLLECT_TO_CURSOR:
            case MOVE_TO_OTHER_INVENTORY:
                if (event.getRawSlot() == 11 && event.getCursor() != null) {
                    clearCraftingRecipe();
                    Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                    return;
                } else {
                    if (getInputItem() != null) {
                        setInputItem(null);
                        Utils.updatePlayerInventory(plugin, (Player) event.getWhoClicked());
                    }
                }
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
