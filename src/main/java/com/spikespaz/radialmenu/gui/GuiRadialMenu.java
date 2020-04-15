package com.spikespaz.radialmenu.gui;

import com.google.common.collect.Lists;
import com.spikespaz.radialmenu.ConfigHandler;
import com.spikespaz.radialmenu.RadialButtonData;
import com.spikespaz.radialmenu.RadialMenu;
import com.spikespaz.radialmenu.Utilities;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.*;
import net.minecraft.client.resources.I18n;
import net.minecraft.item.Item;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.client.event.GuiScreenEvent;
import net.minecraftforge.common.MinecraftForge;

import javax.annotation.Nonnull;
import javax.annotation.ParametersAreNonnullByDefault;
import java.util.List;

public class GuiRadialMenu extends GuiScreen {
    public static List<RadialButtonData> radialMenuData = Lists.newArrayList();
    protected int menuX;
    protected int menuY;

    public GuiRadialMenu(Minecraft mc) {
        ScaledResolution scaledRes = new ScaledResolution(mc);
        this.setWorldAndResolution(mc, scaledRes.getScaledWidth(), scaledRes.getScaledHeight());
    }

    @Override
    @Nonnull
    @ParametersAreNonnullByDefault
    protected <T extends GuiButton> T addButton(T newButton) {
        this.buttonList.add(newButton);

        if (newButton instanceof GuiRadialButton)
            for (int i = 0; i < this.buttonList.size(); i++) {
                GuiRadialButton button = (GuiRadialButton) this.buttonList.get(i);
                button.sliceCount = this.buttonList.size();
                button.sliceNum = i;
            }

        return newButton;
    }

    public static void initButtons() {
        radialMenuData.clear();

        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.wave"),
                new ResourceLocation("quark:textures/emotes/wave.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.yes"),
                new ResourceLocation("quark:textures/emotes/yes.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.no"),
                new ResourceLocation("quark:textures/emotes/no.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.clap"),
                new ResourceLocation("quark:textures/emotes/clap.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.cheer"),
                new ResourceLocation("quark:textures/emotes/cheer.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.salute"),
                new ResourceLocation("quark:textures/emotes/salute.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.shrug"),
                new ResourceLocation("quark:textures/emotes/shrug.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.point"),
                new ResourceLocation("quark:textures/emotes/point.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.think"),
                new ResourceLocation("quark:textures/emotes/think.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.facepalm"),
                new ResourceLocation("quark:textures/emotes/facepalm.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.weep"),
                new ResourceLocation("quark:textures/emotes/weep.png"),
                false,
                null
        ));
        radialMenuData.add(new RadialButtonData(
                Utilities.getKeyBindByName("quark.emote.headbang"),
                new ResourceLocation("quark:textures/emotes/headbang.png"),
                false,
                null
        ));
    }

    protected GuiRadialButton addButton(int id, int circleRadius, int deadZoneRadius, int buttonThickness, int buttonBgColor, int buttonBgHoverColor, float iconOpacity, float hoverIconOpacity) {
        GuiRadialButton button = this.addButton(new GuiRadialButton(id, circleRadius, deadZoneRadius, buttonThickness, buttonBgColor, buttonBgHoverColor, iconOpacity, hoverIconOpacity));

        button.setPressSound(ConfigHandler.SOUND.getButtonSoundEvent(), (float) ConfigHandler.SOUND.getButtonSoundPitch());
        button.setKeyBinding(radialMenuData.get(id).getKeyBinding());
        button.displayString = radialMenuData.get(id).getName();

        Object buttonIcon = radialMenuData.get(id).getButtonIcon();
        if (buttonIcon != null)
            if (Item.class.isAssignableFrom(buttonIcon.getClass()))
                button.setIcon((Item) buttonIcon);
            else
                button.setIcon((ResourceLocation) buttonIcon);

        button.cx = this.menuX;
        button.cy = this.menuY;

        return button;
    }

    @Override
    public void initGui() {
        this.buttonList.clear();
        this.labelList.clear();

        for (int i = 0; i < radialMenuData.size(); i++)
            this.addButton(i, ConfigHandler.GENERAL.getCircleRadius(), ConfigHandler.GENERAL.getDeadZoneRadius(), ConfigHandler.BUTTON.getThickness(), ConfigHandler.BUTTON.getBgColor(), ConfigHandler.BUTTON.getBgHoverColor(), (float) ConfigHandler.BUTTON.getIconOpacity(), (float) ConfigHandler.BUTTON.getIconHoverOpacity());

        if (this.getClass().equals(GuiRadialMenu.class)) {
            this.menuX = this.width / 2;
            this.menuY = this.height / 2;

            for (GuiButton button : this.buttonList)
                if (button instanceof GuiRadialButton) {
                    ((GuiRadialButton) button).cx = this.menuX;
                    ((GuiRadialButton) button).cy = this.menuY;
                }
        }
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        for (GuiLabel label : this.labelList)
            label.drawLabel(this.mc, mouseX, mouseY);

        GuiRadialButton hoveredButton = null, selectedButton = null;

        for (GuiButton button : this.buttonList) {
            button.drawButton(this.mc, mouseX, mouseY, partialTicks);

            if (button instanceof GuiRadialButton) {
                if (button.isMouseOver())
                    hoveredButton = (GuiRadialButton) button;
                else if (((GuiRadialButton) button).isSelected())
                    selectedButton = (GuiRadialButton) button;
            }
        }

        if (hoveredButton != null)
            if (hoveredButton.displayString.isEmpty())
                this.drawCenteredLabel(I18n.format("gui." + RadialMenu.MOD_ID + ".label.unassigned"), ConfigHandler.LABEL.getTextEmptyColor());
            else
                this.drawCenteredLabel(I18n.format(hoveredButton.displayString), ConfigHandler.LABEL.getTextColor());
        else if (selectedButton != null)
            if (selectedButton.displayString.isEmpty())
                this.drawCenteredLabel(I18n.format("gui." + RadialMenu.MOD_ID + ".label.unassigned"), ConfigHandler.LABEL.getTextEmptyColor());
            else
                this.drawCenteredLabel(I18n.format(selectedButton.displayString), ConfigHandler.LABEL.getTextColor());

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
        final int boxWidth = this.fontRenderer.getStringWidth(label) + ConfigHandler.LABEL.getPaddingX() * 2;
        final int boxHeight = this.fontRenderer.FONT_HEIGHT + ConfigHandler.LABEL.getPaddingY() * 2;

        Gui.drawRect(this.menuX - boxWidth / 2,
                this.menuY - boxHeight / 2,
                this.menuX + boxWidth / 2,
                this.menuY + boxHeight / 2,
                ConfigHandler.LABEL.getBgColor());

        this.drawCenteredString(this.mc.fontRenderer, label, this.menuX, this.menuY - this.mc.fontRenderer.FONT_HEIGHT / 2, color);
    }

    @Override
    protected void keyTyped(char typedChar, int keyCode) {
    }

    @Override // Pure vanilla code except play sound
    protected void mouseClicked(int mouseX, int mouseY, int mouseButton) {
        if (mouseButton != 0)
            return;

        for (GuiButton guibutton : this.buttonList)
            if (guibutton.mousePressed(this.mc, mouseX, mouseY)) {
                GuiScreenEvent.ActionPerformedEvent.Pre event = new GuiScreenEvent.ActionPerformedEvent.Pre(this, guibutton, this.buttonList);
                if (MinecraftForge.EVENT_BUS.post(event))
                    break;
                guibutton = event.getButton();
                this.selectedButton = guibutton;
                this.actionPerformed(guibutton);
                if (this.equals(this.mc.currentScreen))
                    MinecraftForge.EVENT_BUS.post(new GuiScreenEvent.ActionPerformedEvent.Post(this, event.getButton(), this.buttonList));
            }
    }

    @Override
    protected void actionPerformed(GuiButton guiButton) {
        if (!(guiButton instanceof GuiRadialButton))
            return;

        GuiRadialButton button = (GuiRadialButton) guiButton;

        if (ConfigHandler.SOUND.isButtonSoundEnabled())
            button.playPressSound(this.mc.getSoundHandler());

        if (button.keyBinding != null) {
            Utilities.focusGame();

            if (radialMenuData.get(guiButton.id).isToggleMode())
                Utilities.toggleKey(button.keyBinding);
            else
                Utilities.fireKey(button.keyBinding);
        }
    }

    protected GuiRadialButton getSelectedButton() {
        for (GuiButton guiButton : this.buttonList)
            if (guiButton instanceof GuiRadialButton) {
                GuiRadialButton button = (GuiRadialButton) guiButton;

                if (button.isSelected())
                    return button;
            }

        return null;
    }

    public void closeGui() {
        if (!ConfigHandler.GENERAL.isToggleModeEnabled())
            for (GuiButton button : this.buttonList)
                if (button.isMouseOver()) {
                    this.actionPerformed(button);
                    break;
                }

        Utilities.focusGame();
    }
}
