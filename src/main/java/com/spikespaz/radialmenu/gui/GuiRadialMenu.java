package com.spikespaz.radialmenu.gui;

import com.spikespaz.radialmenu.ConfigHandler;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.GuiScreen;
import net.minecraft.client.gui.ScaledResolution;
import org.lwjgl.input.Keyboard;

import javax.annotation.Nonnull;
import javax.annotation.ParametersAreNonnullByDefault;

public class GuiRadialMenu extends GuiScreen {
    public GuiRadialMenu(Minecraft mc) {
        ScaledResolution scaledRes = new ScaledResolution(mc);
        this.setWorldAndResolution(mc, scaledRes.getScaledWidth(), scaledRes.getScaledHeight());
    }

    @Override
    @Nonnull
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
        this.addButton(new GuiRadialButton(0, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        this.addButton(new GuiRadialButton(1, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        this.addButton(new GuiRadialButton(2, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        this.addButton(new GuiRadialButton(3, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        this.addButton(new GuiRadialButton(4, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        this.addButton(new GuiRadialButton(5, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        this.addButton(new GuiRadialButton(6, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        this.addButton(new GuiRadialButton(7, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        this.addButton(new GuiRadialButton(8, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        for (GuiButton button : this.buttonList)
            button.drawButton(this.mc, mouseX, mouseY, partialTicks);

//        final ScaledResolution scaledRes = new ScaledResolution(mc);

//        final double cx = scaledRes.getScaledWidth_double() / 2;
//        final double cy = scaledRes.getScaledHeight_double() / 2;
//
//        final double sa = Math.PI * 2 / this.buttonList.size(); // Slice angle

        // Uncomment to draw lines at angles
//        for (int i = 0; i < this.buttonList.size(); i++) {
//            final double lx = Math.sin(Math.PI * 2 * i / this.buttonList.size() - sa / 2) * 2000;
//            final double ly = Math.cos(Math.PI * 2 * i / this.buttonList.size() - sa / 2) * 2000;
//
//            RenderHelper.drawLine(cx, cy, cx + lx, cy + ly, 0xFFFF0000);
//        }

        // Uncomment to draw a line to the mouse
//        final double mouseAngle = MathHelper.normAngle(Math.atan2(mouseX - cx, mouseY - cy));
//        RenderHelper.drawLine(cx, cy, cx + Math.sin(mouseAngle) * 2000, cy + Math.cos(mouseAngle) * 2000, 0xFF00FF00);

//        this.drawCenteredLabel("Radial Menu");
    }

//    @Override
//    public boolean doesGuiPauseGame() {
//        return false;
//    }

    private void drawCenteredLabel(String label) {
        final int boxWidth = this.fontRenderer.getStringWidth(label) + ConfigHandler.getLabelPaddingX() * 2;
        final int boxHeight = this.fontRenderer.FONT_HEIGHT + ConfigHandler.getLabelPaddingY() * 2;

        drawRect((this.width - boxWidth) / 2,
                (this.height - boxHeight) / 2,
                (this.width + boxWidth) / 2,
                (this.height + boxHeight) / 2,
                ConfigHandler.getLabelBgColor());

        this.drawCenteredString(this.mc.fontRenderer, label, this.width / 2, (this.height - this.mc.fontRenderer.FONT_HEIGHT) / 2, ConfigHandler.getLabelTextColor());
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
