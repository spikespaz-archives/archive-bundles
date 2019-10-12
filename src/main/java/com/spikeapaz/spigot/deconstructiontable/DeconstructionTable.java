package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.block.data.BlockData;
import org.bukkit.event.HandlerList;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.ArrayList;
import java.util.HashMap;

public final class DeconstructionTable extends JavaPlugin {
    private static DeconstructionTable instance;
    static BlockData customBlockData;
    private HashMap<ItemStack, ArrayList<ItemStack>> reversedRecipes;
    private PluginEventListener listener;
    private PluginInventoryHolder inventoryHolder;

    @Override
    public void onEnable() {
        // Save an instance of this class for reference outside class scope.
        instance = this;

        // Bind the event listeners.
        listener = new PluginEventListener();
        getServer().getPluginManager().registerEvents(listener, this);

        inventoryHolder = new PluginInventoryHolder();

        // Create the BlockData for the mushroom block.
        customBlockData = Bukkit.getServer().createBlockData("minecraft:red_mushroom_block[down=true,east=false,north=true,south=true,up=false,west=true]");
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

    // Utility function to send a message to the console.
    private void tellConsole(String message) {
        Bukkit.getConsoleSender().sendMessage(message);
    }

    public HashMap<ItemStack, ArrayList<ItemStack>> getReversedRecipes() {
        return reversedRecipes;
    }

    public static DeconstructionTable getInstance() {
        return instance;
    }

    public PluginInventoryHolder getInventoryHolder() {
        return inventoryHolder;
    }
}
