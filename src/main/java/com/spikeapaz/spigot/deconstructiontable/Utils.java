package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.Recipe;
import org.bukkit.inventory.ShapedRecipe;
import org.bukkit.inventory.ShapelessRecipe;
import org.bukkit.plugin.Plugin;
import org.bukkit.scheduler.BukkitRunnable;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Random;


public class Utils {
    private static HashMap<ItemStack, ReversedRecipe> reversedRecipes;

    public static HashMap<ItemStack, ReversedRecipe> getReversedRecipes() {
        // If the reverses aren't already, generate them
        if (reversedRecipes == null) {
            reversedRecipes = new HashMap<>();

            // Get all of the recipes in the game
            final Iterator<Recipe> recipeIterator = Bukkit.recipeIterator();

            // Iterate through all of the recipes, setting them to recipeBase
            Recipe recipeBase;
            while (recipeIterator.hasNext()) {
                recipeBase = recipeIterator.next();

                // Create the reversed recipe and add it to the HashMap
                if (ShapedRecipe.class.isAssignableFrom(recipeBase.getClass())) { // It is a Shaped Recipe
                    final ReversedRecipe recipe = new ReversedRecipe((ShapedRecipe) recipeBase);

                    if (recipe.getOutput(1).size() == 0) {
                        Utils.tellConsole("Failed to generate recipe with zero ingredients: " + recipe.getInput().getType());

                        continue;
                    }

                    reversedRecipes.put(recipe.getInput(), recipe);
                } else if (ShapelessRecipe.class.isAssignableFrom(recipeBase.getClass())) { // It is a Shapeless Recipe
                    final ReversedRecipe recipe = new ReversedRecipe((ShapelessRecipe) recipeBase);
                    reversedRecipes.put(recipe.getInput(), recipe);
                }
            }
        }

        // If it is generated return it otherwise we just did generate it
        return reversedRecipes;
    }

    // Check if the ItemStack passed is our custom firework with model data
    public static boolean isDeconstructionTableItem(ItemStack item) {
        return item != null && item.getType().equals(Material.FIREWORK_ROCKET) && item.getItemMeta() != null && item.getItemMeta().getCustomModelData() == 10000100;
    }

    // Is the Block passed our special mushroom block?
    public static boolean isDeconstructionTableBlock(Block block) {
        return block != null && block.getBlockData().equals(DeconstructionTable.customBlockData);
    }

    // Generate a random string the specified length.
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

    // Instant "delayed" update to the player inventory. Fixes some bugginess with the inventory not updating in time to see slot changes.
    public static void updatePlayerInventory(Plugin plugin, Player player) {
        new BukkitRunnable() {
            @Override
            public void run() {
                player.updateInventory();
            }
        }.runTaskLater(plugin, 0);
    }
}
