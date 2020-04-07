package com.spikespaz.radialmenu.gui;

import com.spikespaz.radialmenu.ConfigHandler;
import com.spikespaz.radialmenu.KeyBindings;
import com.spikespaz.radialmenu.RadialMenu;
import com.spikespaz.radialmenu.Utilities;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Gui;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.GuiScreen;
import net.minecraft.client.gui.ScaledResolution;
import net.minecraft.client.resources.I18n;
import net.minecraft.util.ResourceLocation;
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
        GuiRadialButton btn0 = this.addButton(new GuiRadialButton(0, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn0.setIcon(new ResourceLocation("quark:textures/emotes/wave.png"));
        btn0.setKeyBinding(Utilities.getKeyBindByName("quark.emote.wave"));
        GuiRadialButton btn1 = this.addButton(new GuiRadialButton(1, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn1.setIcon(new ResourceLocation("quark:textures/emotes/yes.png"));
        btn1.setKeyBinding(Utilities.getKeyBindByName("quark.emote.yes"));
        GuiRadialButton btn2 = this.addButton(new GuiRadialButton(2, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn2.setIcon(new ResourceLocation("quark:textures/emotes/no.png"));
        btn2.setKeyBinding(Utilities.getKeyBindByName("quark.emote.no"));
        GuiRadialButton btn3 = this.addButton(new GuiRadialButton(3, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn3.setIcon(new ResourceLocation("quark:textures/emotes/clap.png"));
        btn3.setKeyBinding(Utilities.getKeyBindByName("quark.emote.clap"));
        GuiRadialButton btn4 = this.addButton(new GuiRadialButton(4, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn4.setIcon(new ResourceLocation("quark:textures/emotes/cheer.png"));
        btn4.setKeyBinding(Utilities.getKeyBindByName("quark.emote.cheer"));
        GuiRadialButton btn5 = this.addButton(new GuiRadialButton(5, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn5.setIcon(new ResourceLocation("quark:textures/emotes/salute.png"));
        btn5.setKeyBinding(Utilities.getKeyBindByName("quark.emote.salute"));
        GuiRadialButton btn6 = this.addButton(new GuiRadialButton(6, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn6.setIcon(new ResourceLocation("quark:textures/emotes/shrug.png"));
        btn6.setKeyBinding(Utilities.getKeyBindByName("quark.emote.shrug"));
        GuiRadialButton btn7 = this.addButton(new GuiRadialButton(7, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn7.setIcon(new ResourceLocation("quark:textures/emotes/point.png"));
        btn7.setKeyBinding(Utilities.getKeyBindByName("quark.emote.point"));
        GuiRadialButton btn8 = this.addButton(new GuiRadialButton(8, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn8.setIcon(new ResourceLocation("quark:textures/emotes/think.png"));
        btn8.setKeyBinding(Utilities.getKeyBindByName("quark.emote.think"));
        GuiRadialButton btn9 = this.addButton(new GuiRadialButton(9, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn9.setIcon(new ResourceLocation("quark:textures/emotes/facepalm.png"));
        btn9.setKeyBinding(Utilities.getKeyBindByName("quark.emote.facepalm"));
        GuiRadialButton btn10 = this.addButton(new GuiRadialButton(10, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn10.setIcon(new ResourceLocation("quark:textures/emotes/weep.png"));
        btn10.setKeyBinding(Utilities.getKeyBindByName("quark.emote.weep"));
        GuiRadialButton btn11 = this.addButton(new GuiRadialButton(11, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor()));
        btn11.setIcon(new ResourceLocation("quark:textures/emotes/headbang.png"));
        btn11.setKeyBinding(Utilities.getKeyBindByName("quark.emote.headbang"));
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        for (GuiButton button : this.buttonList) {
            button.drawButton(this.mc, mouseX, mouseY, partialTicks);

            if (button.isMouseOver()) {
                if (button.displayString.isEmpty())
                    this.drawCenteredLabel(I18n.format("gui." + RadialMenu.MOD_ID + ".unassigned"), ConfigHandler.getLabelTextEmptyColor());
                else
                    this.drawCenteredLabel(I18n.format(button.displayString), ConfigHandler.getLabelTextColor());
            }
        }

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
    }

    @Override
    public boolean doesGuiPauseGame() {
        return false;
    }

    private void drawCenteredLabel(String label, int color) {
        final int boxWidth = this.fontRenderer.getStringWidth(label) + ConfigHandler.getLabelPaddingX() * 2;
        final int boxHeight = this.fontRenderer.FONT_HEIGHT + ConfigHandler.getLabelPaddingY() * 2;

        Gui.drawRect((this.width - boxWidth) / 2,
                (this.height - boxHeight) / 2,
                (this.width + boxWidth) / 2,
                (this.height + boxHeight) / 2,
                ConfigHandler.getLabelBgColor());

        this.drawCenteredString(this.mc.fontRenderer, label, this.width / 2, (this.height - this.mc.fontRenderer.FONT_HEIGHT) / 2, color);
    }

    @Override
    protected void keyTyped(char typedChar, int keyCode) {
        if (keyCode == Keyboard.KEY_ESCAPE || keyCode == KeyBindings.openMenu0.getKeyCode()) {
            this.mc.displayGuiScreen(null);

            if (this.mc.currentScreen == null)
                this.mc.setIngameFocus();
        }
    }
}
