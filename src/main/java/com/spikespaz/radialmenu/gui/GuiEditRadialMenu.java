package com.spikespaz.radialmenu.gui;

import com.spikespaz.radialmenu.ConfigHandler;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiButton;

public class GuiEditRadialMenu extends GuiRadialMenu {
    protected int editsX;

    public GuiEditRadialMenu(Minecraft mc) {
        super(mc);

        this.menuX = Math.max(ConfigHandler.GENERAL.getCircleRadius() + ConfigHandler.BUTTON.getThickness() + 10, this.width / 4);
        this.editsX = Math.min(this.width - 210, this.width / 4);
    }

    @Override
    protected GuiRadialButton addButton(int id, int circleRadius, int deadZoneRadius, int buttonThickness, int buttonBgColor, int buttonBgHoverColor, float iconOpacity, float hoverIconOpacity) {
        GuiRadialButton button = super.addButton(id, circleRadius, deadZoneRadius, buttonThickness, buttonBgColor, buttonBgHoverColor, iconOpacity, hoverIconOpacity);
        button.mouseBoundary = true;
        return button;
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        this.drawDefaultBackground();

        super.drawScreen(mouseX, mouseY, partialTicks);
    }

    @Override
    public boolean doesGuiPauseGame() {
        return true;
    }

    @Override
    protected void actionPerformed(GuiButton guiButton) {
        GuiRadialButton button = (GuiRadialButton) guiButton;

//        if (ConfigHandler.SOUND.isButtonSoundEnabled())
//            button.playPressSound(this.mc.getSoundHandler());

        button.setSelected(true);

        for (GuiButton guiButton1 : this.buttonList)
            if (!guiButton.equals(guiButton1))
                ((GuiRadialButton) guiButton1).setSelected(false);
    }
}
