package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.block.Block;
import org.bukkit.block.BlockFace;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.inventory.ItemStack;

public class PlayerInteractEventListener implements Listener {
    private boolean isCustomItem(ItemStack item) {
        return item.getType().equals(Material.FIREWORK_ROCKET) && item.getItemMeta() != null && item.getItemMeta().getCustomModelData() == 10000100;
    }

    private void interactWithBlock(PlayerInteractEvent event) {
        CustomInventory inventory = new CustomInventory();

        event.getPlayer().openInventory(inventory.getInventory());
    }

    @EventHandler
    public void onPlayerInteractEvent(PlayerInteractEvent event) {
        ItemStack item = event.getItem();
        Block block = event.getClickedBlock();
        Player player = event.getPlayer();

        if (!event.getAction().equals(Action.RIGHT_CLICK_BLOCK))
            return;

        if (block != null && block.getBlockData().equals(DeconstructionTable.customBlockData) && !player.isSneaking()) {
            interactWithBlock(event);
        } else if (block != null && item != null && isCustomItem(item)) {
            // Remove the custom item from the player's inventory
            item.setAmount(item.getAmount() - 1);

            BlockFace clickedBlockFace = event.getBlockFace();
            Location replacementLocation = block.getLocation().add(clickedBlockFace.getModX(), clickedBlockFace.getModY(), clickedBlockFace.getModZ());
            Block replacementBlock = replacementLocation.getBlock();

            replacementBlock.setType(Material.RED_MUSHROOM_BLOCK);
            replacementBlock.setBlockData(DeconstructionTable.customBlockData);

            player.playSound(replacementLocation, Sound.BLOCK_WOOD_PLACE, 1, 1);
        } else
            return;

        event.setCancelled(true);
    }
}
