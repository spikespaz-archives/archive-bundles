package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.ShapedRecipe;
import org.bukkit.inventory.ShapelessRecipe;

import java.util.ArrayList;
import java.util.Map;

public class ReversedRecipe {
    private ItemStack input;
    private ArrayList<ItemStack> items;
    private int dividend;

    public ReversedRecipe(ItemStack input, ArrayList<ItemStack> items, int dividend) {
        this.input = input;
        this.items = items;
        this.dividend = dividend;
    }

    public ReversedRecipe(ShapedRecipe recipe) {
        input = recipe.getResult().clone();
        dividend = input.getAmount();
        input.setAmount(1);

        items = new ArrayList<>(9);

        Map<Character, ItemStack> ingredientMap = recipe.getIngredientMap();

        for (int slot = 0; slot < 9; slot++) {
            int rowNum = Math.floorDiv(slot, 3);

            if (recipe.getShape().length < rowNum + 1) {
                items.add(null);
                continue;
            }

            String row = recipe.getShape()[rowNum];

            if (row.length() < slot % 3 + 1)
                items.add(null);
            else
                items.add(ingredientMap.get(row.charAt(slot % 3)));
        }
    }

    public ReversedRecipe(ShapelessRecipe recipe) {
        input = recipe.getResult().clone();
        dividend = input.getAmount();
        input.setAmount(1);

        items = new ArrayList<>(9);

        for (int slot = 0; slot < 9; slot++)
            if (recipe.getIngredientList().size() > slot)
                items.add(recipe.getIngredientList().get(slot));
            else
                items.add(null);
    }

    public ItemStack getInput() {
        return input.clone();
    }

    public ArrayList<ItemStack> getOutput(int amount) {
        ArrayList<ItemStack> adjustedItems = new ArrayList<>();

        for (ItemStack item : items) {
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
