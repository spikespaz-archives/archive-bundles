package com.spikespaz.radialmenu;

import com.spikespaz.radialmenu.gui.GuiRadialMenu;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;

@Mod(modid = RadialMenu.MOD_ID, name = RadialMenu.MOD_NAME, version = RadialMenu.MOD_VERSION, clientSideOnly = true, canBeDeactivated = true)
public class RadialMenu {
    public static final String MOD_ID = "radialmenu";
    public static final String MOD_NAME = "@MOD_NAME@";
    public static final String MOD_VERSION = "@MOD_VERSION@";

    @Mod.Instance(MOD_ID)
    public static RadialMenu INSTANCE;

    @Mod.EventHandler
    public void preInit(FMLPreInitializationEvent event) {
    }

    @Mod.EventHandler
    public void init(FMLInitializationEvent event) {
        KeyBindings.registerAll();
    }

    @Mod.EventHandler
    public void postInit(FMLPostInitializationEvent event) {
        MinecraftForge.EVENT_BUS.register(new EventHandler());

        GuiRadialMenu.clearButtons();
        GuiRadialMenu.initButtons();
    }
}
