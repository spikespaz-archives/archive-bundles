package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.ClickType;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.plugin.Plugin;

public class EventListener implements Listener {
    private Plugin plugin = DeconstructionTable.getPlugin(DeconstructionTable.class);

    @EventHandler
    public void onInventoryClickEvent(InventoryClickEvent event) {
        Player player = (Player) event.getWhoClicked();

        ClickType click = event.getClick();

        Inventory open = event.getClickedInventory();

        assert open != null && open.getHolder() != null;
        if (!open.getHolder().getClass().isInstance(CustomInventory.class))
            return;
    }
}
