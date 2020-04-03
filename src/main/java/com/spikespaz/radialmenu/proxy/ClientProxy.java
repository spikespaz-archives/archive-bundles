package com.spikespaz.radialmenu.proxy;

import com.spikespaz.radialmenu.EventHandler;
import com.spikespaz.radialmenu.RadialMenu;
import com.spikespaz.radialmenu.proxy.IProxy;
import net.minecraft.client.settings.KeyBinding;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.client.registry.ClientRegistry;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import org.lwjgl.input.Keyboard;

import java.util.HashMap;

public class ClientProxy implements IProxy {
    public static final String KEYBIND_CATEGORY = "key." + RadialMenu.MOD_ID + ".category";
    public static final String GUI_OPEN_KEY = "key.radialmenu.open";

    public static HashMap<String, KeyBinding> keyBindings = new HashMap<>();

    @Override
    public void preInit(FMLPreInitializationEvent event) {}

    @Override
    public void init(FMLInitializationEvent event) {
        keyBindings.put(GUI_OPEN_KEY, new KeyBinding(GUI_OPEN_KEY, Keyboard.KEY_X, KEYBIND_CATEGORY));

        for (KeyBinding keyBinding : keyBindings.values())
            ClientRegistry.registerKeyBinding(keyBinding);
    }

    @Override
    public void postInit(FMLPostInitializationEvent event) {
        MinecraftForge.EVENT_BUS.register(new EventHandler());
    }
}
