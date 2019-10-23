package com.spikespaz.spigot.deconstructiontable;

import com.google.common.collect.Sets;
import org.bukkit.Material;
import org.bukkit.inventory.*;

import java.util.*;

class ReversedRecipe {
    private ItemStack input;
    private List<List<ItemStack>> itemLists;
    private int dividend;
    private Recipe originalRecipe;

    // Construct from a shaped recipe (recipe grid)
    ReversedRecipe(ShapedRecipe recipe) {
        originalRecipe = recipe;

        input = recipe.getResult().clone();
        dividend = input.getAmount();
        input.setAmount(1); // The recipe is looked for by an ItemStack with a count of 1

        itemLists = new ArrayList<>();
        // Create a copy of the recipe shape within which redundant keys will be removed
        String[] shape = recipe.getShape();

        Utils.tellConsole("Creating reversed recipe for: " + recipe.getResult().toString());

        // Represents a list of all map entries. This is a list of sets so that it can be processed by Guava.
        List<Set<Map.Entry<Character, ItemStack>>> valuePairs = new ArrayList<>();
        // Create a new choice map that will have unique entries. No value may map to multiple keys.
        Map<Character, RecipeChoice> dedupMap = new HashMap<>();

        // Iterate all entries in the recipe's choice map, removing duplicate keys from dedupMap and shape
        for (Map.Entry<Character, RecipeChoice> entry : recipe.getChoiceMap().entrySet()) {
            Character altKey = Utils.keyFromValue(dedupMap, entry.getValue());

            if (altKey != null) {
                int rowNum = 0;
                for (String row : shape) {
                    shape[rowNum] = row.replace(entry.getKey(), altKey);
                    rowNum++;
                }
            } else
                dedupMap.put(entry.getKey(), entry.getValue());
        }

        // Loop through all character and material choice pairs in the recipe
        for (Map.Entry<Character, RecipeChoice> entry : dedupMap.entrySet()) {
            RecipeChoice.MaterialChoice choice = (RecipeChoice.MaterialChoice) entry.getValue();
            // Represents the current set of map entries to be added to valuePairs
            Set<Map.Entry<Character, ItemStack>> mapSet = new HashSet<>();


            if (choice == null) // The slots corresponding to this key will be empty
                mapSet.add(new AbstractMap.SimpleEntry<>(entry.getKey(), null));
            else
                for (Material material : choice.getChoices())
                    // Get an item from the material choice
                    mapSet.add(new AbstractMap.SimpleEntry<>(entry.getKey(), new ItemStack(material)));

            // Add the entries to the valuePairs list. Each set is a map.
            valuePairs.add(mapSet);
        }

        // Combinations of all unique map entries
        Set<List<Map.Entry<Character, ItemStack>>> cartesianMaps = Sets.cartesianProduct(valuePairs);
        // Prepare a new list of maps to be created from the lists within the cartesian product set
        List<Map<Character, ItemStack>> recipeMaps = new ArrayList<>();

        // Reassemble the recipe maps with individual ItemStacks as ingredients
        for (List<Map.Entry<Character, ItemStack>> entryList : cartesianMaps) {
            Map<Character, ItemStack> recipeMap = new HashMap<>();

            for (Map.Entry<Character, ItemStack> entry : entryList)
                recipeMap.put(entry.getKey(), entry.getValue());

            recipeMaps.add(recipeMap);
        }

        for (Map<Character, ItemStack> recipeMap : recipeMaps) {
            List<ItemStack> ingredients = new ArrayList<>();

            // Loop through each slot index
            for (int slot = 0; slot < 9; slot++) {
                // Row and column numbers. Y and X in a 9x9 grid
                int rowNum = Math.floorDiv(slot, 3);
                int colNum = slot % 3;

                // If the recipe doesn't have a current row, add a null item and continue to next slot
                if (shape.length < rowNum + 1) {
                    ingredients.add(null);
                    continue;
                }

                String row = shape[rowNum];

                // If the row is shorter than the requested index, add a null item
                if (row.length() < colNum + 1)
                    ingredients.add(null);
                else // There is an item so check the ingredient map and add it
                    ingredients.add(recipeMap.get(row.charAt(colNum)));
            }

            itemLists.add(ingredients);
        }

        Utils.tellConsole(itemLists.size() + " recipes for " + recipe.getResult());
    }

    // Construct the recipe from shapeless recipe (ingredient list, not grid)
    ReversedRecipe(ShapelessRecipe recipe) {
        originalRecipe = recipe;

        input = recipe.getResult().clone();
        dividend = input.getAmount();
        input.setAmount(1); // The recipe is looked for by an ItemStack with a count of 1

        itemLists = new ArrayList<>();

        List<Set<ItemStack>> materialChoices = new ArrayList<>();

        for (RecipeChoice recipeChoice : recipe.getChoiceList()) {
            RecipeChoice.MaterialChoice choice = (RecipeChoice.MaterialChoice) recipeChoice;
            Set<ItemStack> items = new HashSet<>();

            for (Material material : choice.getChoices())
                items.add(new ItemStack(material));

            materialChoices.add(items);
        }

        itemLists.addAll(Sets.cartesianProduct(materialChoices));
    }

    // Returns the original Recipe object that this is made from
    Recipe getOriginalRecipe() {
        return originalRecipe;
    }

    // Returns a copy of the input item (or the result from the crafting recipe) as an ItemStack with an amount of 1
    ItemStack getInput() {
        return input.clone();
    }

    ItemStack getKeyItem() {
        final ItemStack cloned = input.clone();
        cloned.setAmount(1);
        return cloned;
    }

    // Get an ArrayList of 9 items, each a slot in the crafting area, some of them null.
    // Each ItemStack amount will be adjusted in accordance to amount and dividend.
    // The index parameter is specifically for recipes with multiple combinations. It is an index in an array of cartesian products.
    ArrayList<ItemStack> getOutput(int index, int amount) {
        ArrayList<ItemStack> adjustedItems = new ArrayList<>(9);

        for (ItemStack item : itemLists.get(index)) {
            if (item != null) {
                ItemStack adjustedItem = item.clone();

                int itemAmount = item.getAmount() * Math.floorDiv(amount, dividend);

                if (itemAmount > 0)
                    adjustedItem.setAmount(item.getAmount() * Math.floorDiv(amount, dividend));
                else
                    return new ArrayList<>(9);

                adjustedItems.add(adjustedItem);
            } else
                adjustedItems.add(null);
        }

        return adjustedItems;
    }

    int getChoiceCount() {
        return itemLists.size();
    }
}
