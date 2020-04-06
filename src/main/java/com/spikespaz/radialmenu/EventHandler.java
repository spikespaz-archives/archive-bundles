package com.spikespaz.radialmenu;

import com.spikespaz.radialmenu.gui.GuiRadialMenu;
import com.spikespaz.radialmenu.proxy.ClientProxy;
import net.minecraft.client.Minecraft;
import net.minecraftforge.client.event.RenderGameOverlayEvent;
import net.minecraftforge.common.config.Config;
import net.minecraftforge.common.config.ConfigManager;
import net.minecraftforge.fml.client.event.ConfigChangedEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class EventHandler {
    private static final Minecraft mc = Minecraft.getMinecraft();
    private boolean openGuiKeyPressed = false;

    @SideOnly(Side.CLIENT)
    @SubscribeEvent
    public void onEvent(RenderGameOverlayEvent.Pre event) {
        if (mc.currentScreen instanceof GuiRadialMenu && event.getType() == RenderGameOverlayEvent.ElementType.CROSSHAIRS)
            event.setCanceled(true);
    }

    @SideOnly(Side.CLIENT)
    @SubscribeEvent
    public void onEvent(RenderGameOverlayEvent.Post event) {
        if (this.openGuiKeyPressed && event.getType() == RenderGameOverlayEvent.ElementType.ALL) {
            mc.displayGuiScreen(new GuiRadialMenu(mc));
            this.openGuiKeyPressed = false;
        }
    }

    @SideOnly(Side.CLIENT)
    @SubscribeEvent
    public void onEvent(InputEvent.KeyInputEvent event) {
        this.openGuiKeyPressed = KeyBindings.openMenu0.isPressed();
    }
}
