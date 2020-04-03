package com.spikespaz.radialmenu;

import com.spikespaz.radialmenu.proxy.IProxy;
import net.minecraft.client.Minecraft;
import net.minecraftforge.client.event.RenderGameOverlayEvent;
import net.minecraftforge.fml.common.SidedProxy;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod(
    modid = RadialMenu.MOD_ID,
    name = RadialMenu.MOD_NAME,
    version = RadialMenu.VERSION
)
public class RadialMenu {
    public static final String MOD_ID = "radialmenu";
    public static final String MOD_NAME = "Radial Menu";
    public static final String VERSION = "0.1.0";

    @SidedProxy(clientSide = "com.spikespaz.radialmenu.proxy.ClientProxy")
    private static IProxy proxy;

    @Mod.Instance(MOD_ID)
    public static RadialMenu INSTANCE;

    @Mod.EventHandler
    public void preInit(FMLPreInitializationEvent event) {
        proxy.preInit(event);
    }

    @Mod.EventHandler
    public void init(FMLInitializationEvent event) {
        proxy.init(event);
    }

    @Mod.EventHandler
    public void postInit(FMLPostInitializationEvent event) {
        proxy.postInit(event);
    }

    public IProxy getProxy() {
        return proxy;
    }
}
