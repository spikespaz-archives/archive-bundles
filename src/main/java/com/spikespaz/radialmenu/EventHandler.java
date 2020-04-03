package com.spikespaz.radialmenu;

import com.spikespaz.radialmenu.proxy.ClientProxy;
import net.minecraft.client.Minecraft;
import net.minecraftforge.client.event.RenderGameOverlayEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class EventHandler {
    private boolean showGui = false;

    @SideOnly(Side.CLIENT)
    @SubscribeEvent()
    public void onEvent(RenderGameOverlayEvent.Pre event) {
        if (this.showGui && event.getType() == RenderGameOverlayEvent.ElementType.CROSSHAIRS)
            event.setCanceled(true);
    }

    @SideOnly(Side.CLIENT)
    @SubscribeEvent()
    public void onEvent(RenderGameOverlayEvent.Post event) {
        if (this.showGui && event.getType() == RenderGameOverlayEvent.ElementType.ALL)
            new GuiRadialMenu(Minecraft.getMinecraft());
    }

    @SideOnly(Side.CLIENT)
    @SubscribeEvent(receiveCanceled = true)
    public void onEvent(InputEvent.KeyInputEvent event) {
        this.showGui = ClientProxy.keyBindings.get(ClientProxy.GUI_OPEN_KEY).isPressed();
    }
}
