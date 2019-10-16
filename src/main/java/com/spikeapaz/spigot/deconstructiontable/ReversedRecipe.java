package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.Recipe;
import org.bukkit.inventory.ShapedRecipe;
import org.bukkit.inventory.ShapelessRecipe;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ReversedRecipe {
    private ItemStack input;
    private ArrayList<ItemStack> ingredients;
    private int dividend;
    private Recipe originalRecipe;

    // Construct from a shaped recipe (recipe grid)
    public ReversedRecipe(ShapedRecipe recipe) {
        originalRecipe = recipe;

        input = recipe.getResult().clone();
        dividend = input.getAmount();
        input.setAmount(1); // The recipe is looked for by an ItemStack with a count of 1

        ingredients = new ArrayList<>(9);

        Map<Character, ItemStack> ingredientMap = recipe.getIngredientMap();

        int rowNum, colNum;

        // Loop through each slot index
        for (int slot = 0; slot < 9; slot++) {
            // Row and column numbers. Y and X in a 9x9 grid
            rowNum = Math.floorDiv(slot, 3);
            colNum = slot % 3;

            // If the recipe doesn't have a current row, add a null item and continue to next slot
            if (recipe.getShape().length < rowNum + 1) {
                ingredients.add(null);
                continue;
            }

            String row = recipe.getShape()[rowNum];

            // If the row is shorter than the requested index, add a null item
            if (row.length() < colNum + 1)
                ingredients.add(null);
            else // There is an item so check the ingredient map and add it
                ingredients.add(ingredientMap.get(row.charAt(colNum)));
        }
    }

    // Construct the recipe from shapeless recipe (ingredient list, not grid)
    public ReversedRecipe(ShapelessRecipe recipe) {
        originalRecipe = recipe;

        input = recipe.getResult().clone();
        dividend = input.getAmount();
        input.setAmount(1); // The recipe is looked for by an ItemStack with a count of 1

        ingredients = new ArrayList<>(9);
        final List<ItemStack> ingredients = recipe.getIngredientList();

        for (int slot = 0; slot < 9; slot++)
            if (ingredients.size() > slot) // There are more ingredients than the index of the current slot
                this.ingredients.add(recipe.getIngredientList().get(slot)); // Add it accordingly
            else
                this.ingredients.add(null); // The ingredients list does not have enough items so just add null for the rest of the slots
    }

    // Returns the original Recipe object that this is made from
    public Recipe getOriginalRecipe() {
        return originalRecipe;
    }

    // Returns a copy of the input item (or the result from the crafting recipe) as an ItemStack with an amount of 1
    public ItemStack getInput() {
        return input.clone();
    }

    public ItemStack getKetItem() {
        final ItemStack cloned = input.clone();
        cloned.setAmount(1);
        return cloned;
    }

    // Get an ArrayList of 9 items, each a slot in the crafting area, some of them null.
    // Each ItemStack amount will be adjusted in accordance to amount and dividend.
    public ArrayList<ItemStack> getOutput(int amount) {
        ArrayList<ItemStack> adjustedItems = new ArrayList<>();

        for (ItemStack item : ingredients) {
            if (item != null) {
                ItemStack adjustedItem = item.clone();

                int itemAmount = item.getAmount() * Math.floorDiv(amount, dividend);

                if (itemAmount > 0)
                    adjustedItem.setAmount(item.getAmount() * Math.floorDiv(amount, dividend));
                else
                    return new ArrayList<>();

                adjustedItems.add(adjustedItem);
            } else
                adjustedItems.add(null);
        }

        return adjustedItems;
    }
}
