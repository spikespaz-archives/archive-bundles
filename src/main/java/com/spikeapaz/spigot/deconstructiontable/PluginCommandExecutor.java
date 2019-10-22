package com.spikeapaz.spigot.deconstructiontable;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;

public class PluginCommandExecutor implements CommandExecutor {
    @Override
    public boolean onCommand(final CommandSender sender, final Command command, final String label, final String[] args) {
        assert sender != null && label != null && args != null;

        if (!command.getName().equalsIgnoreCase("dct"))
            return false;

        switch (args[0]) {
            case "regenrecipes":
                Utils.clearReversedRecipes();
                Utils.getReversedRecipes();
                sender.sendMessage("Regenerated reversed recipes.");
                break;
            default:
                return false;
        }

        return true;
    }
}
