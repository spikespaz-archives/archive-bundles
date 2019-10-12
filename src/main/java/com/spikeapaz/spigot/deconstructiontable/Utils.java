package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.Recipe;
import org.bukkit.inventory.ShapedRecipe;
import org.bukkit.inventory.ShapelessRecipe;

import java.util.*;


public class Utils {
    private static HashMap<ItemStack, ArrayList<ItemStack>> reversedRecipes;

    public static HashMap<ItemStack, ArrayList<ItemStack>> getReversedRecipes() {
        if (reversedRecipes == null) {
            Iterator<Recipe> recipeIterator = Bukkit.recipeIterator();
            Recipe recipeBase;

            while (recipeIterator.hasNext()) {
                recipeBase = recipeIterator.next();

                if (recipeBase.getClass().isInstance(ShapedRecipe.class)) {
                    ShapedRecipe recipe = (ShapedRecipe) recipeBase;
                    ArrayList<ItemStack> ingredients = new ArrayList<>();

                    Map<Character, ItemStack> ingredientMap = recipe.getIngredientMap();

                    String flatRecipe = String.join("", recipe.getShape());
                    for (int i = 0; i < flatRecipe.length(); i++) {
                        char letter = flatRecipe.charAt(0);
                        ingredients.add(ingredientMap.get(letter));
                    }

                    reversedRecipes.put(recipe.getResult(), ingredients);
                } else if (recipeBase.getClass().isInstance(ShapelessRecipe.class)) {
                    ShapelessRecipe recipe = (ShapelessRecipe) recipeBase;

                    reversedRecipes.put(recipe.getResult(), new ArrayList<>(recipe.getIngredientList()));
                }
            }
        }

        return reversedRecipes;
    }

    public static boolean isDeconstructionTableItem(ItemStack item) {
        return item != null && item.getType().equals(Material.FIREWORK_ROCKET) && item.getItemMeta() != null && item.getItemMeta().getCustomModelData() == 10000100;
    }

    public static boolean isDeconstructionTableBlock(Block block) {
        return block != null && block.getBlockData().equals(DeconstructionTable.customBlockData);
    }

    public static String randomString(int size) {
        final Random random = new Random();
        final StringBuilder buffer = new StringBuilder();
        final char[] alphabet = "abcdefghijklmnopqrstuvwxyz0123456789".toCharArray();

        for (int i = 0; i < size; i++)
            buffer.append(alphabet[random.nextInt(alphabet.length - 1)]);

        return buffer.toString();
    }

    // Utility function to send a message to the console.
    public static void tellConsole(String message) {
        Bukkit.getConsoleSender().sendMessage(message);
    }
}
