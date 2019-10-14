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
        if (reversedRecipes == null) {
            reversedRecipes = new HashMap<>();
            storeReversedRecipes(reversedRecipes);
        }

        return reversedRecipes;
    }

    public static void storeReversedRecipes(HashMap<ItemStack, ReversedRecipe> store) {
        Iterator<Recipe> recipeIterator = Bukkit.recipeIterator();

        Recipe recipeBase;
        while (recipeIterator.hasNext()) {
            recipeBase = recipeIterator.next();

            if (ShapedRecipe.class.isAssignableFrom(recipeBase.getClass())) {
                Utils.tellConsole("Creating reversed recipe for " + recipeBase.getResult().toString());

                ReversedRecipe recipe = new ReversedRecipe((ShapedRecipe) recipeBase);
                store.put(recipe.getInput(), recipe);
            } else if (ShapelessRecipe.class.isAssignableFrom(recipeBase.getClass())) {
                Utils.tellConsole("Creating reversed recipe for " + recipeBase.getResult().toString());

                ReversedRecipe recipe = new ReversedRecipe((ShapelessRecipe) recipeBase);
                store.put(recipe.getInput(), recipe);
            }
        }
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

    public static void updatePlayerInventory(Plugin plugin, Player player) {
        new BukkitRunnable() {
            @Override
            public void run() {
                player.updateInventory();
            }
        }.runTaskLater(plugin, 0);
    }

    public static void doNothing() {
    }
}
