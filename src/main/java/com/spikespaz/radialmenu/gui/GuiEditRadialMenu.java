package com.spikespaz.radialmenu.gui;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.GuiLabel;
import net.minecraft.client.gui.GuiTextField;
import net.minecraft.client.renderer.BufferBuilder;
import net.minecraft.client.renderer.GlStateManager;
import net.minecraft.client.renderer.Tessellator;
import net.minecraft.client.renderer.vertex.DefaultVertexFormats;
import net.minecraft.client.resources.I18n;
import net.minecraft.client.settings.KeyBinding;
import net.minecraft.util.ResourceLocation;
import org.lwjgl.input.Keyboard;

public class GuiEditRadialMenu extends GuiRadialMenu {
    private static final int ADD_BUTTON = 101;
    private static final int DELETE_BUTTON = 102;
    private static final int BTN_W = 150;
    private static final int BTN_H = 20;
    private static final int FLD_W = BTN_W - 2;
    private static final int FLD_H = BTN_H - 2;
    private static final int OH = BTN_H * 2 + 4;
    private static final int CHANGE_KEYBINDING = 103;
    private static final int CHANGE_ICON = 104;
    private static final int CHANGE_NAME = 105;
    protected int editsX;
    private boolean reInitGui;
    private int lastSelectedButtonId;
    private GuiTextField displayNameField;
    private GuiTextField iconResourceField;
    private GuiButton changeKeyBindingBtn;

    public GuiEditRadialMenu(Minecraft mc) {
        super(mc);
    }

    @Override
    protected GuiRadialButton addButton(int id, int circleRadius, int deadZoneRadius, int buttonThickness, int buttonBgColor, int buttonBgHoverColor, float iconOpacity, float hoverIconOpacity) {
        if (circleRadius * 2 + buttonThickness * 2 + 10 > this.width / 2)
            circleRadius = this.width / 4 - buttonThickness - 10;

        GuiRadialButton button = super.addButton(id, circleRadius, deadZoneRadius, buttonThickness, buttonBgColor, buttonBgHoverColor, iconOpacity, hoverIconOpacity);
        button.mouseBoundary = true;
        return button;
    }

    @Override
    public void initGui() {
        super.initGui();

        this.menuX = this.width / 4;
        this.menuY = this.height / 2;
        this.editsX = this.width * 3 / 4;

//        this.addButton(new GuiButton(100, this.editsX - btnW / +2, this.height / 2 - btnH / 2, btnW, btnH, "Add Button"));
        this.addButton(new GuiButton(ADD_BUTTON, this.editsX - BTN_H - 2, this.height - BTN_H - 4, BTN_H, BTN_H, "+"));
        this.addButton(new GuiButton(DELETE_BUTTON, this.editsX + 2, this.height - BTN_H - 4, BTN_H, BTN_H, "-"));

        GuiLabel label;
        int labelWidth;
        String labelString;

        labelString = I18n.format("gui.radialmenu.label.displayname");
        labelWidth = this.fontRenderer.getStringWidth(labelString);
        label = new GuiLabel(this.fontRenderer, 0, this.editsX - labelWidth / 2, this.height / 2 + OH * -2, 0, BTN_H, 0xFFFFFFFF);
        label.addLine(labelString);
        this.labelList.add(label);

        this.displayNameField = new GuiTextField(0, this.fontRenderer, this.editsX - BTN_W / 2 + 2, this.height / 2 + OH * -2 + BTN_H + 2, BTN_W - 4, BTN_H - 4);
        this.displayNameField.setMaxStringLength(32);
        //        this.displayNameField.setFocused(true);

        labelString = I18n.format("gui.radialmenu.label.keybinding");
        labelWidth = this.fontRenderer.getStringWidth(labelString);
        label = new GuiLabel(this.fontRenderer, 1, this.editsX - labelWidth / 2, this.height / 2 + OH * -1, 0, BTN_H, 0xFFFFFFFF);
        label.addLine(labelString);
        this.labelList.add(label);

        this.changeKeyBindingBtn = this.addButton(new GuiButton(CHANGE_KEYBINDING, this.editsX - BTN_W / 2, this.height / 2 + OH * -1 + BTN_H, BTN_W, BTN_H, ""));

        labelString = I18n.format("gui.radialmenu.label.iconresourcelocation");
        labelWidth = this.fontRenderer.getStringWidth(labelString);
        label = new GuiLabel(this.fontRenderer, 2, this.editsX - labelWidth / 2, this.height / 2 + OH * 0, 0, BTN_H, 0xFFFFFFFF);
        label.addLine(labelString);
        this.labelList.add(label);

        this.iconResourceField = new GuiTextField(0, this.fontRenderer, this.editsX - BTN_W / 2 + 2, this.height / 2 + OH * 0 + BTN_H + 2, BTN_W - 4, BTN_H - 4);
        this.iconResourceField.setMaxStringLength(512);

        for (GuiButton button : this.buttonList)
            if (button instanceof GuiRadialButton) {
                if (button.id == this.lastSelectedButtonId) {
                    GuiRadialButton radialButton = (GuiRadialButton) button;

                    this.displayNameField.setText(radialButton.displayString);

                    if (radialButton.imageIcon != null)
                        this.iconResourceField.setText(radialButton.imageIcon.toString());

                    if (radialButton.keyBinding != null)
                        this.changeKeyBindingBtn.displayString = I18n.format(radialButton.keyBinding.getKeyDescription());

                    ((GuiRadialButton) button).setSelected(true);
                }

                ((GuiRadialButton) button).cx = this.menuX;
                ((GuiRadialButton) button).cy = this.menuY;
            }
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        if (this.reInitGui) {
            this.initGui();
            this.reInitGui = false;
        }

        this.drawDefaultBackground();

        super.drawScreen(mouseX, mouseY, partialTicks);

        this.displayNameField.drawTextBox();
        this.iconResourceField.drawTextBox();

        // Uncomment to draw debug lines
//        this.drawDebugLines();
    }

    private void drawDebugLines() {
        RenderHelper.drawLine(this.width * 3 / 4, 0, this.width * 3 / 4, this.height, 0xFF00FF00);
        RenderHelper.drawLine(this.width * 3 / 4 - BTN_W / 2, 0, this.width * 3 / 4 - BTN_W / 2, this.height, 0xFFFFFF00);
        RenderHelper.drawLine(this.width * 3 / 4 + BTN_W / 2, 0, this.width * 3 / 4 + BTN_W / 2, this.height, 0xFFFFFF00);

        for (int i = -3; i <= 3; i++) {
            RenderHelper.drawLine(this.width / 2, this.height / 2 + OH * i, this.width, this.height / 2 + OH * i, 0xFFFF00FF);
            RenderHelper.drawLine(this.width / 2, this.height / 2 + OH * i - 4, this.width, this.height / 2 + OH * i - 4, 0xFFFFFF00);
        }
    }

    @Override
    public boolean doesGuiPauseGame() {
        return true;
    }

    @Override
    protected void actionPerformed(GuiButton guiButton) {
        if (guiButton instanceof GuiRadialButton) {
            GuiRadialButton button = (GuiRadialButton) guiButton;

//        if (ConfigHandler.SOUND.isButtonSoundEnabled())
//            button.playPressSound(this.mc.getSoundHandler());

            button.setSelected(true);
            this.lastSelectedButtonId = button.id;

            for (GuiButton guiButton1 : this.buttonList)
                if ((guiButton1 instanceof GuiRadialButton) && !guiButton.equals(guiButton1))
                    ((GuiRadialButton) guiButton1).setSelected(false);

            this.displayNameField.setText(button.displayString);

            if (button.imageIcon != null)
                this.iconResourceField.setText(button.imageIcon.toString());

            if (button.keyBinding != null)
                this.changeKeyBindingBtn.displayString = I18n.format(button.keyBinding.getKeyDescription());
        } else {
            GuiRadialButton radialBtn = this.getSelectedButton();

            this.lastSelectedButtonId = (radialBtn == null) ? 0 : radialBtn.id;

            switch (guiButton.id) {
                case ADD_BUTTON: // Should I impose hard limit?
                    keyBindings.add(this.lastSelectedButtonId, null);
                    buttonIcons.add(this.lastSelectedButtonId, null);
                    displayStrings.add(this.lastSelectedButtonId, "");
                    this.reInitGui = true;
                    break;
                case DELETE_BUTTON:
                    if (this.getBtnIdCount() <= 4)
                        break;

                    keyBindings.remove(this.lastSelectedButtonId);
                    buttonIcons.remove(this.lastSelectedButtonId);
                    displayStrings.remove(this.lastSelectedButtonId);
                    this.reInitGui = true;
                    break;
                case CHANGE_KEYBINDING:
                    GuiControlSelect guiControlSelect = new GuiControlSelect(mc, this, result -> {
                        KeyBinding binding = (KeyBinding) result;
                        keyBindings.set(this.lastSelectedButtonId, binding);
                        displayStrings.set(this.lastSelectedButtonId, I18n.format(binding.getKeyDescription()));
                        this.reInitGui = true;
                    });
                    mc.displayGuiScreen(guiControlSelect);
                    break;
            }
        }
    }

    @Override
    public void updateScreen() {
        this.displayNameField.updateCursorCounter();
        this.iconResourceField.updateCursorCounter();
    }

    @Override
    protected void keyTyped(char typedChar, int keyCode) {
        this.displayNameField.textboxKeyTyped(typedChar, keyCode);
        this.iconResourceField.textboxKeyTyped(typedChar, keyCode);

        if (keyCode == Keyboard.KEY_TAB) {
            this.displayNameField.setFocused(!this.displayNameField.isFocused());
            this.iconResourceField.setFocused(!this.iconResourceField.isFocused());
        }

        GuiRadialButton button = this.getSelectedButton();

        if (this.displayNameField.isFocused())
            displayStrings.set(this.lastSelectedButtonId, button.displayString = this.displayNameField.getText());

        if (this.iconResourceField.isFocused()) {
            if (this.iconResourceField.getText().isEmpty())
                buttonIcons.set(this.lastSelectedButtonId, button.imageIcon = null);
            else
                buttonIcons.set(this.lastSelectedButtonId, button.imageIcon = new ResourceLocation(this.iconResourceField.getText()));
        }
    }

    @Override
    protected void mouseClicked(int mouseX, int mouseY, int mouseButton) {
        super.mouseClicked(mouseX, mouseY, mouseButton);

        this.displayNameField.mouseClicked(mouseX, mouseY, mouseButton);
        this.iconResourceField.mouseClicked(mouseX, mouseY, mouseButton);
    }

    @Override
    public void drawWorldBackground(int tint) {
        if (this.mc.world != null) {
            this.drawGradientRect(0, 0, this.width, this.height, -1072689136, -804253680);
            this.drawBackground(this.width / 2, 0, this.width, this.height, tint);
        } else {
            this.drawBackground(0, 0, this.width, this.height, tint);
        }
    }

    private void drawBackground(int x0, int y0, int x1, int y1, int tint) {
        GlStateManager.disableLighting();
        GlStateManager.disableFog();
        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferbuilder = tessellator.getBuffer();
        this.mc.getTextureManager().bindTexture(OPTIONS_BACKGROUND);
        GlStateManager.color(1.0F, 1.0F, 1.0F, 1.0F);
        float f = 32.0F;
        bufferbuilder.begin(7, DefaultVertexFormats.POSITION_TEX_COLOR);
        int width = x1 - x0, height = y1 - y0;
        bufferbuilder.pos(x0, y1, 0.0D).tex(0, height / 32f).color(64, 64, 64, 255).endVertex();
        bufferbuilder.pos(x1, y1, 0.0D).tex(width / 32f, height / 32f).color(64, 64, 64, 255).endVertex();
        bufferbuilder.pos(x1, y0, 0.0D).tex(width / 32f, 0).color(64, 64, 64, 255).endVertex();
        bufferbuilder.pos(x0, y0, 0.0D).tex(0, 0).color(64, 64, 64, 255).endVertex();
        tessellator.draw();
    }
}
