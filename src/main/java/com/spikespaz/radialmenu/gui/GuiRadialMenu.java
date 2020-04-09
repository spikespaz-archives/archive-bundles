package com.spikespaz.radialmenu.gui;

import com.google.common.collect.Lists;
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
import net.minecraft.client.settings.KeyBinding;
import net.minecraft.item.Item;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.client.event.GuiScreenEvent;
import net.minecraftforge.common.MinecraftForge;
import org.lwjgl.input.Keyboard;

import javax.annotation.Nonnull;
import javax.annotation.ParametersAreNonnullByDefault;
import java.util.List;

public class GuiRadialMenu extends GuiScreen {
    public static List<KeyBinding> keyBindings = Lists.newArrayList();
    public static List<Object> buttonIcons = Lists.newArrayList();

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

    public static void initButtons() {
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/wave.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.wave"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/yes.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.yes"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/no.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.no"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/clap.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.clap"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/cheer.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.cheer"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/salute.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.salute"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/shrug.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.shrug"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/point.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.point"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/think.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.think"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/facepalm.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.facepalm"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/weep.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.weep"));
        buttonIcons.add(new ResourceLocation("quark:textures/emotes/headbang.png"));
        keyBindings.add(Utilities.getKeyBindByName("quark.emote.headbang"));
    }

    public static void clearButtons() {
        buttonIcons.clear();
        keyBindings.clear();
    }

    private GuiRadialButton addButton(int id, int circleRadius, int deadZoneRadius, int buttonThickness, int buttonBgColor, int buttonBgHoverColor) {
        GuiRadialButton button = this.addButton(new GuiRadialButton(id, circleRadius, deadZoneRadius, buttonThickness, buttonBgColor, buttonBgHoverColor));

        button.setKeyBinding(keyBindings.get(id));

        if (Item.class.isAssignableFrom(buttonIcons.get(id).getClass()))
            button.setIcon((Item) buttonIcons.get(id));
        else
            button.setIcon((ResourceLocation) buttonIcons.get(id));

        return button;
    }

    @Override
    public void initGui() {
        GuiRadialButton btn0 = this.addButton(0, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn1 = this.addButton(1, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn2 = this.addButton(2, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn3 = this.addButton(3, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn4 = this.addButton(4, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn5 = this.addButton(5, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn6 = this.addButton(6, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn7 = this.addButton(7, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn8 = this.addButton(8, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn9 = this.addButton(9, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn10 = this.addButton(10, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
        GuiRadialButton btn11 = this.addButton(11, ConfigHandler.getCircleRadius(), ConfigHandler.getDeadZoneRadius(), ConfigHandler.getButtonThickness(), ConfigHandler.getButtonBgColor(), ConfigHandler.getButtonBgHoverColor());
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
        if (keyCode == Keyboard.KEY_ESCAPE || keyCode == KeyBindings.openMenu0.getKeyCode())
            Utilities.focusGame();
    }

    @Override
    protected void actionPerformed(GuiButton guiButton) {
        GuiRadialButton button = (GuiRadialButton) guiButton;

        if (button.keyBinding == null || Keyboard.isKeyDown(Keyboard.KEY_LMENU)) {
            GuiControlSelect selectGui = new GuiControlSelect(this.mc, this);
            this.mc.displayGuiScreen(selectGui);
        } else if (button.keyBinding != null) {
            Utilities.focusGame();
            Utilities.emitKeyBindEvent(button.keyBinding);
        }
    }
}
