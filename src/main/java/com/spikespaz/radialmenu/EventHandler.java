package com.spikespaz.radialmenu;

import com.spikespaz.radialmenu.gui.GuiEditRadialMenu;
import com.spikespaz.radialmenu.gui.GuiRadialMenu;
import net.minecraft.client.Minecraft;
import net.minecraftforge.client.event.GuiScreenEvent;
import net.minecraftforge.client.event.RenderGameOverlayEvent;
import net.minecraftforge.common.config.Config;
import net.minecraftforge.common.config.ConfigManager;
import net.minecraftforge.fml.client.event.ConfigChangedEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent;
import org.lwjgl.input.Keyboard;

@Mod.EventBusSubscriber(modid = RadialMenu.MOD_ID)
public class EventHandler {
    private static final Minecraft mc = Minecraft.getMinecraft();

    @SubscribeEvent
    public void onEvent(RenderGameOverlayEvent.Pre event) {
        if (mc.currentScreen instanceof GuiRadialMenu && event.getType() == RenderGameOverlayEvent.ElementType.CROSSHAIRS)
            event.setCanceled(true);
        else if (mc.currentScreen instanceof GuiEditRadialMenu && event.getType() == RenderGameOverlayEvent.ElementType.ALL)
            event.setCanceled(true);
    }

    @SubscribeEvent
    public void onEvent(InputEvent.KeyInputEvent event) {
        if (mc.currentScreen != null) {
            return;
        } else if (KeyBindings.EDIT_MENU_0.isPressed()) {
            Keyboard.enableRepeatEvents(false);
            mc.displayGuiScreen(new GuiEditRadialMenu(mc));
        } else if (KeyBindings.OPEN_MENU_0.isPressed()) {
            Keyboard.enableRepeatEvents(false);
            mc.displayGuiScreen(new GuiRadialMenu(mc));
        }
    }

    @SubscribeEvent
    public void onEvent(GuiScreenEvent.KeyboardInputEvent event) {
        if (Keyboard.isRepeatEvent())
            return;

        if (mc.currentScreen instanceof GuiEditRadialMenu) {
            if (Keyboard.getEventKey() == Keyboard.KEY_ESCAPE) {
                ((GuiRadialMenu) mc.currentScreen).closeGui();
                Keyboard.enableRepeatEvents(true);
            }
        } else if (mc.currentScreen instanceof GuiRadialMenu) {
            boolean openMenu0Released = Keyboard.getEventKey() == KeyBindings.OPEN_MENU_0.getKeyCode() && !Keyboard.getEventKeyState();

            if (ConfigHandler.GENERAL.isToggleModeEnabled() ^ openMenu0Released) {
                ((GuiRadialMenu) mc.currentScreen).closeGui();
                Keyboard.enableRepeatEvents(true);
            }
        }
    }

    @SubscribeEvent
    public void onEvent(ConfigChangedEvent.OnConfigChangedEvent event) {
        if (event.getModID().equals(RadialMenu.MOD_ID)) {
            ConfigManager.sync(RadialMenu.MOD_ID, Config.Type.INSTANCE);

            GuiRadialMenu.clearButtons();
            GuiRadialMenu.initButtons();
        }
    }
}
