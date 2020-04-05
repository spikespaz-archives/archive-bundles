package com.spikespaz.radialmenu;

import com.spikespaz.radialmenu.gui.GuiRadialButton;
import mcp.MethodsReturnNonnullByDefault;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.GuiScreen;
import net.minecraft.client.gui.ScaledResolution;
import org.lwjgl.input.Keyboard;

import javax.annotation.ParametersAreNonnullByDefault;

public class GuiRadialMenu extends GuiScreen {
    private final int CIRCLE_RADIUS = 40;
    private final int DEAD_RADIUS = 10;
    private final int LABEL_BG_COLOR = 0xCC000000;
    private final int LABEL_TEXT_COLOR = 0xFFFFFFFF;
    private final int LABEL_PADDING_X = 4;
    private final int LABEL_PADDING_Y = 4;
    private final int BUTTON_BG_COLOR = 0xCC000000;
    private final int BUTTON_BG_HOVER_COLOR = 0xCC000000;
    private final int BUTTON_THICKNESS = 20;

    public GuiRadialMenu(Minecraft mc) {
        ScaledResolution scaledRes = new ScaledResolution(mc);
        this.setWorldAndResolution(mc, scaledRes.getScaledWidth(), scaledRes.getScaledHeight());
    }

    @Override
    @MethodsReturnNonnullByDefault
    @ParametersAreNonnullByDefault
    protected <T extends GuiButton> T addButton(T newButton) {
        this.buttonList.add(newButton);

        for (int i = 0; i < this.buttonList.size(); i++) {
            GuiRadialButton button = (GuiRadialButton) this.buttonList.get(i);
            button.sliceCount = this.buttonList.size();
            button.sliceNum = i;
        }

        return newButton;
    }

    @Override
    public void initGui() {
        this.addButton(new GuiRadialButton(0, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
        this.addButton(new GuiRadialButton(1, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
//        this.addButton(new GuiRadialButton(2, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
//        this.addButton(new GuiRadialButton(3, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
//        this.addButton(new GuiRadialButton(4, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
//        this.addButton(new GuiRadialButton(5, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
//        this.addButton(new GuiRadialButton(6, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
//        this.addButton(new GuiRadialButton(7, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
//        this.addButton(new GuiRadialButton(8, this.CIRCLE_RADIUS, this.DEAD_RADIUS, this.BUTTON_THICKNESS, this.BUTTON_BG_COLOR, this.BUTTON_BG_HOVER_COLOR));
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        for (GuiButton button : this.buttonList)
            button.drawButton(this.mc, mouseX, mouseY, partialTicks);

//        this.drawCenteredLabel("Radial Menu");
    }

    @Override
    public boolean doesGuiPauseGame()
    {
        return false;
    }

    private void drawCenteredLabel(String label) {
        final int boxWidth = this.fontRenderer.getStringWidth(label) + this.LABEL_PADDING_X * 2;
        final int boxHeight = this.fontRenderer.FONT_HEIGHT + this.LABEL_PADDING_Y * 2;

        drawRect((this.width - boxWidth) / 2,
                (this.height - boxHeight) / 2,
                (this.width + boxWidth) / 2,
                (this.height + boxHeight) / 2,
                this.LABEL_BG_COLOR);

        this.drawCenteredString(this.mc.fontRenderer, label, this.width / 2, (this.height - this.mc.fontRenderer.FONT_HEIGHT) / 2, this.LABEL_TEXT_COLOR);
    }

    @Override
    protected void keyTyped(char typedChar, int keyCode) {
        switch (keyCode) {
            case Keyboard.KEY_ESCAPE:
            case Keyboard.KEY_X:
                this.mc.displayGuiScreen(null);
                if (this.mc.currentScreen == null)
                    this.mc.setIngameFocus();
                break;
            default:
        }
    }
}
