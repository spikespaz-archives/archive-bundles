package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.Recipe;
import org.bukkit.inventory.ShapedRecipe;
import org.bukkit.inventory.ShapelessRecipe;
import org.bukkit.plugin.Plugin;
import org.bukkit.scheduler.BukkitRunnable;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;


class Utils {
    private static Map<ItemStack, List<ReversedRecipe>> reversedRecipes;

    static void clearReversedRecipes() {
        reversedRecipes = null;
    }

    static Map<ItemStack, List<ReversedRecipe>> getReversedRecipes() {
        // If the reverses aren't already, generate them
        if (reversedRecipes == null || reversedRecipes.size() == 0) {
            reversedRecipes = new HashMap<>();

            // Get all of the recipes in the game
            final Iterator<Recipe> recipeIterator = Bukkit.recipeIterator();

            // Iterate through all of the recipes, setting them to recipeBase
            Recipe recipeBase;
            while (recipeIterator.hasNext()) {
                recipeBase = recipeIterator.next();

                ReversedRecipe recipe;

                // Create the reversed recipe and add it to the HashMap
                if (ShapedRecipe.class.isAssignableFrom(recipeBase.getClass())) // It is a Shaped Recipe
                    recipe = new ReversedRecipe((ShapedRecipe) recipeBase);
                else if (ShapelessRecipe.class.isAssignableFrom(recipeBase.getClass())) // It is a Shapeless Recipe
                    recipe = new ReversedRecipe((ShapelessRecipe) recipeBase);
                else
                    continue;

                // Add it to the recipe list
                if (reversedRecipes.containsKey(recipe.getKeyItem()))
                    reversedRecipes.get(recipe.getKeyItem()).add(recipe);
                else
                    reversedRecipes.put(recipe.getKeyItem(), Stream.of(recipe).collect(Collectors.toList()));
            }
        }

        // If it is generated return it otherwise we just did generate it
        return reversedRecipes.entrySet().stream().collect(Collectors.toMap(Map.Entry::getKey, entry -> new ArrayList<>(entry.getValue())));
    }

    // Check if the ItemStack passed is our custom firework with model data
    static boolean isDeconstructionTableItem(ItemStack item) {
        return item != null && item.getType().equals(Material.FIREWORK_ROCKET) && item.getItemMeta() != null && item.getItemMeta().getCustomModelData() == 10000100;
    }

    // Is the Block passed our special mushroom block?
    static boolean isDeconstructionTableBlock(Block block) {
        return block != null && block.getBlockData().equals(DeconstructionTable.customBlockData);
    }

    // Generate a random string the specified length.
    static String randomString(int size) {
        final Random random = new Random();
        final StringBuilder buffer = new StringBuilder();
        final char[] alphabet = "abcdefghijklmnopqrstuvwxyz0123456789".toCharArray();

        for (int i = 0; i < size; i++)
            buffer.append(alphabet[random.nextInt(alphabet.length - 1)]);

        return buffer.toString();
    }

    // Utility function to send a message to the console.
    static void tellConsole(String message) {
        Bukkit.getConsoleSender().sendMessage(message);
    }

    // Instant "delayed" update to the player inventory. Fixes some bugginess with the inventory not updating in time to see slot changes.
    static void updatePlayerInventory(Plugin plugin, Player player) {
        new BukkitRunnable() {
            @Override
            public void run() {
                player.updateInventory();
            }
        }.runTaskLater(plugin, 0);
    }

    // Rounds the location provided down to a block position
    static Location locToBlock(Location location) {
        return new Location(location.getWorld(), location.getBlockX(), location.getBlockY(), location.getBlockZ());
    }

    // Get a key from the first occurrence of a value in a Map
    static <K, V> K keyFromValue(Map<K, V> map, V value) {
        for (Map.Entry<K, V> entry : map.entrySet())
            if ((entry.getValue() == null && value == null) || (entry.getValue() != null && entry.getValue().equals(value)))
                return entry.getKey();

        return null;
    }
}
