package com.spikespaz.radialmenu;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.common.Loader;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.ModContainer;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;

@Mod(modid = RadialMenu.MOD_ID, clientSideOnly = true, canBeDeactivated = true, useMetadata = true)
public class RadialMenu {
    public static final String MOD_ID = "radialmenu";
    public static String MOD_NAME;
    public static String MOD_VERSION;

    static {
        for (ModContainer mod : Loader.instance().getModList())
            if (mod.getModId().equals(MOD_ID)) {
                MOD_NAME = mod.getName();
                MOD_VERSION = mod.getVersion();

                break;
            }
    }

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
    }
}
