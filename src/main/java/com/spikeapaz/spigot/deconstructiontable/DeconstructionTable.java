package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.block.data.BlockData;
import org.bukkit.event.HandlerList;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.java.JavaPlugin;

public final class DeconstructionTable extends JavaPlugin {
    static BlockData customBlockData;

    private PlayerInteractEventListener listener;

    @Override
    public void onEnable() {
        // Tell the console that the plugin is loaded.
        tellConsole("Enabled Deconstruction Table.");

        customBlockData = Bukkit.getServer().createBlockData("minecraft:red_mushroom_block[down=true,east=false,north=true,south=true,up=false,west=true]");

        listener = new PlayerInteractEventListener();
        getServer().getPluginManager().registerEvents(listener, this);
    }

    @Override
    public void onDisable() {
        // Inform on unload.
        tellConsole("Disabled Deconstruction Table.");

        // Unregister the PlayerInteractEventListener
        HandlerList.unregisterAll(listener);
    }

    // Utility function to send a message to the console.
    public void tellConsole(String message){
        Bukkit.getConsoleSender().sendMessage(message);
    }
}
