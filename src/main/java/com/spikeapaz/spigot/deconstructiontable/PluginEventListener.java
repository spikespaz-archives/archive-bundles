package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.block.Block;
import org.bukkit.block.BlockFace;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.ArrayList;

public class PluginEventListener implements Listener {
    private DeconstructionTable plugin = JavaPlugin.getPlugin(DeconstructionTable.class);

    @EventHandler
    public void onInventoryClickEvent(InventoryClickEvent event) {
        InventoryHolder baseHolder = event.getInventory().getHolder();
        if (baseHolder == null) return;

        if (PluginInventoryHolder.class.isAssignableFrom(baseHolder.getClass()))
            ((PluginInventoryHolder) baseHolder).handleClick(event);
    }

    @EventHandler
    void onInventoryDragEvent(InventoryDragEvent event) {
        InventoryHolder baseHolder = event.getInventory().getHolder();
        if (baseHolder == null) return;

        if (PluginInventoryHolder.class.isAssignableFrom(baseHolder.getClass()))
            ((PluginInventoryHolder) baseHolder).handleDrag(event);
    }

    @EventHandler
    public void onPlayerInteractEvent(PlayerInteractEvent event) {
        final Player player = event.getPlayer();
        final ItemStack heldItem = event.getItem();
        final Block clickedBlock = event.getClickedBlock();

        if (!event.getAction().equals(Action.RIGHT_CLICK_BLOCK))
            return;

        if (heldItem != null && heldItem.getType().isBlock() && player.isSneaking())
            return;

        if (Utils.isDeconstructionTableBlock(clickedBlock)) {
            player.openInventory(plugin.getInventoryHolder().getInventory());

            event.setCancelled(true);
        } else if (Utils.isDeconstructionTableItem(event.getItem())) {
            if (clickedBlock == null)
                return;

            // Prevent any vanilla default behavior.
            event.setCancelled(true);

            // Add the direction of the clicked face to the clock position.
            final Location placeLocation = clickedBlock.getLocation();
            placeLocation.add(event.getBlockFace().getDirection());

            final Block placedBlock = placeLocation.getBlock();

            // Get block locations on all six sides
            final ArrayList<Location> adjacentLocations = new ArrayList<Location>();
            adjacentLocations.add(placeLocation.clone().add(BlockFace.UP.getDirection()));
            adjacentLocations.add(placeLocation.clone().add(BlockFace.DOWN.getDirection()));
            adjacentLocations.add(placeLocation.clone().add(BlockFace.NORTH.getDirection()));
            adjacentLocations.add(placeLocation.clone().add(BlockFace.SOUTH.getDirection()));
            adjacentLocations.add(placeLocation.clone().add(BlockFace.EAST.getDirection()));
            adjacentLocations.add(placeLocation.clone().add(BlockFace.WEST.getDirection()));

            // Prevent the block from being placed to not mess up the mushroom textures
            for (Location location : adjacentLocations)
                if (location.getBlock().getType().equals(Material.RED_MUSHROOM_BLOCK))
                    return;

            // Update block data to the unused red mushroom block.
            placedBlock.setType(Material.RED_MUSHROOM_BLOCK);
            placedBlock.setBlockData(DeconstructionTable.customBlockData);

            // Play the default wood placing sound when setting the block.
            player.playSound(placeLocation, Sound.BLOCK_WOOD_PLACE, 1, 1);

            // Remove the custom firework from the player's inventory/
            assert heldItem != null;
            heldItem.setAmount(heldItem.getAmount() - 1);
        }
    }
}
