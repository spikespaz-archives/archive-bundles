package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.block.Block;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;

public class PluginEventListener implements Listener {
    private DeconstructionTable plugin = (DeconstructionTable) JavaPlugin.getPlugin(DeconstructionTable.class);

    @EventHandler
    public void onInventoryClickEvent(InventoryClickEvent event) {
        org.bukkit.inventory.InventoryHolder baseHolder = event.getInventory().getHolder();

        if (baseHolder == null)
            return;

        if (baseHolder.getClass().isInstance(PluginInventoryHolder.class)) {
            PluginInventoryHolder holder = (PluginInventoryHolder) baseHolder;

            holder.handleClick(event);
        }
    }

    @EventHandler
    public void onPlayerInteractEvent(PlayerInteractEvent event) {
        Player player = event.getPlayer();
        ItemStack heldItem = event.getItem();
        Block clickedBlock = event.getClickedBlock();

        if (Utils.isDeconstructionTableBlock(clickedBlock)) {
            player.openInventory(plugin.getInventoryHolder().getInventory());
        } else if (Utils.isDeconstructionTableItem(event.getItem())) {
            if (clickedBlock == null)
                return;

            // Prevent any vanilla default behavior.
            event.setCancelled(true);

            // Add the direction of the clicked face to the clock position.
            Location placeLocation = event.getClickedBlock().getLocation();
            placeLocation.add(event.getBlockFace().getDirection());

            Block placedBlock = placeLocation.getBlock();

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
