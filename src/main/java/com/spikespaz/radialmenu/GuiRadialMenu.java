package com.spikespaz.radialmenu;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Gui;
import net.minecraft.client.gui.ScaledResolution;

public class GuiRadialMenu extends Gui {
    private Minecraft mc;
    private int screenWidth;
    private int screenHeight;
    private final int BG_COLOR = 0xCC000000;
    private final int TEXT_COLOR = 0xFFFFFFFF;
    private final int PADDING_X = 4;
    private final int PADDING_Y = 4;

    public GuiRadialMenu(Minecraft mc) {
        this.mc = mc;
        ScaledResolution scaledRes = new ScaledResolution(this.mc);
        this.screenWidth = scaledRes.getScaledWidth();
        this.screenHeight = scaledRes.getScaledHeight();

        this.drawCenteredLabel(new Action("Create Waypoint"));
    }

    private void drawCenteredLabel(final Action action) {
        final int boxWidth = this.mc.fontRenderer.getStringWidth(action.getName()) + this.PADDING_X * 2;
        final int boxHeight = this.mc.fontRenderer.FONT_HEIGHT + this.PADDING_Y * 2;

        drawRect((this.screenWidth - boxWidth) / 2,
                (this.screenHeight - boxHeight) / 2,
                (this.screenWidth + boxWidth) / 2,
                (this.screenHeight + boxHeight) / 2,
                this.BG_COLOR);

        this.drawCenteredString(this.mc.fontRenderer, action.getName(), this.screenWidth / 2, (this.screenHeight - this.mc.fontRenderer.FONT_HEIGHT) / 2, this.TEXT_COLOR);
    }

    public class Action {
        private String name;

        public Action(final String name) {
            this.name = name;
        }

        public String getName() {
            return this.name;
        }
    }
}
