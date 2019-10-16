package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.block.data.BlockData;
import org.bukkit.event.HandlerList;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.ShapedRecipe;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.java.JavaPlugin;

import static com.spikeapaz.spigot.deconstructiontable.Utils.tellConsole;


public final class DeconstructionTable extends JavaPlugin {
    private static DeconstructionTable instance;
    static BlockData customBlockData;
    private PluginEventListener listener;
    private PluginInventoryHolder inventoryHolder;

    @Override
    public void onEnable() {
        // Save an instance of this class for reference outside class scope.
        instance = this;

        // Bind the event listeners.
        listener = new PluginEventListener();
        Bukkit.getPluginManager().registerEvents(listener, this);

        // Make the ItemStack and ItemMeta for the custom mushroom block
        final ItemStack blockItem = new ItemStack(Material.FIREWORK_ROCKET);
        final ItemMeta itemMeta = blockItem.getItemMeta();
        assert itemMeta != null;
        itemMeta.setDisplayName("Deconstruction Table");
        itemMeta.setCustomModelData(10000100);
        blockItem.setItemMeta(itemMeta);

        // Create the crafting recipe for the mushroom block
        final NamespacedKey namespacedKey = new NamespacedKey(this, "deconstruction_table_" + Utils.randomString(6));
        final ShapedRecipe blockRecipe = new ShapedRecipe(namespacedKey, blockItem);
        blockRecipe.shape("III", "ICI", "III");
        blockRecipe.setIngredient('I', Material.IRON_INGOT);
        blockRecipe.setIngredient('C', Material.CRAFTING_TABLE);
        Bukkit.addRecipe(blockRecipe);

        tellConsole("deconstruction_table namespace: " + namespacedKey.getNamespace() + "." + namespacedKey.getKey());

        // Pre-generate the reversed recipes
        Utils.getReversedRecipes();

        inventoryHolder = new PluginInventoryHolder();

        // Create the BlockData for the mushroom block.
        customBlockData = Bukkit.createBlockData("minecraft:red_mushroom_block[down=true,east=false,north=true,south=true,up=false,west=true]");

        // Tell the console that the plugin is loaded.
        tellConsole("Enabled Deconstruction Table.");
    }

    @Override
    public void onDisable() {
        // Inform on unload.
        tellConsole("Disabled Deconstruction Table.");

        // Unregister the PlayerInteractEventListener
        HandlerList.unregisterAll(listener);
    }

    public static DeconstructionTable getInstance() {
        return instance;
    }

    public PluginInventoryHolder getInventoryHolder() {
        return inventoryHolder;
    }
}
